#!/usr/bin/env python3
"""
Claude Code ↔ 智谱 GLM API 代理服务器 v2
简化版本，专注于稳定性
"""

from flask import Flask, request, Response
import requests
import json
import sys
from datetime import datetime

app = Flask(__name__)

# 智谱 API 配置
ZHIPU_API_KEY = "30e5211d21884f8fb20d2f583203b57c.Ace0jfxMn5EkRMLh"
ZHIPU_BASE_URL = "https://open.bigmodel.cn/api/paas"

# 日志函数
def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")
    sys.stdout.flush()

# 模型名称映射
MODEL_MAPPING = {
    "claude-haiku-4-5-20251001": "glm-4.7",
    "claude-sonnet-4-5-20250929": "glm-4.7",
    "claude-opus-4-5-20250929": "glm-4.7",
}

def convert_to_openai_format(anthropic_request):
    """转换 Anthropic 格式到 OpenAI 兼容格式"""
    log(f"原始请求模型: {anthropic_request.get('model', 'unknown')}")

    # 提取模型名称
    model = anthropic_request.get("model", "claude-sonnet-4-5-20250929")
    if ":" in model:
        model = model.split(":")[-1]

    # 映射到智谱模型
    zhipu_model = MODEL_MAPPING.get(model, "glm-4.7")
    log(f"映射后模型: {zhipu_model}")

    # 构建消息列表
    messages = []

    # 添加系统提示词
    system = anthropic_request.get("system", "")
    if system:
        if isinstance(system, str):
            messages.append({"role": "system", "content": system})
        elif isinstance(system, list) and len(system) > 0:
            # 从列表中提取文本
            for item in system:
                if item.get("type") == "text":
                    messages.append({"role": "system", "content": item.get("text", "")})
                    break

    # 转换用户消息
    for msg in anthropic_request.get("messages", []):
        role = msg.get("role", "user")
        content = msg.get("content", "")

        if isinstance(content, str):
            messages.append({"role": role, "content": content})
        elif isinstance(content, list) and len(content) > 0:
            # 处理内容块
            text_parts = []
            for item in content:
                if item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            if text_parts:
                messages.append({"role": role, "content": "".join(text_parts)})

    # 构建 OpenAI 兼容请求
    openai_request = {
        "model": zhipu_model,
        "messages": messages,
        "stream": False  # 暂时禁用流式，简化处理
    }

    # 复制其他参数
    if "max_tokens" in anthropic_request:
        openai_request["max_tokens"] = anthropic_request["max_tokens"]
    if "temperature" in anthropic_request:
        openai_request["temperature"] = anthropic_request["temperature"]
    if "top_p" in anthropic_request:
        openai_request["top_p"] = anthropic_request["top_p"]

    log(f"转换后的请求: {json.dumps(openai_request, ensure_ascii=False)[:300]}...")
    return openai_request

def convert_to_anthropic_format(zhipu_response):
    """转换智谱响应格式到 Anthropic 格式"""
    log(f"智谱原始响应: {json.dumps(zhipu_response, ensure_ascii=False)[:200]}...")

    # 提取消息内容 - 优先使用 reasoning_content，然后是 content
    content_text = ""
    if 'choices' in zhipu_response and len(zhipu_response['choices']) > 0:
        message = zhipu_response['choices'][0].get('message', {})
        # 智谱 GLM-4.7 可能使用 reasoning_content
        content_text = message.get('reasoning_content') or message.get('content', '')

    log(f"提取的文本: {content_text[:100] if content_text else '(空)'}...")

    # 构建 Anthropic 格式响应
    anthropic_response = {
        "id": f"msg_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "type": "message",
        "role": "assistant",
        "model": zhipu_response.get("model", "glm-4.7"),
        "content": [
            {
                "type": "text",
                "text": content_text
            }
        ],
        "stop_reason": "end_turn",
        "usage": zhipu_response.get("usage", {})
    }

    return anthropic_response

@app.route('/v1/messages', methods=['POST'])
@app.route('/api/anthropic/v1/messages', methods=['POST'])
def create_message():
    """处理 Messages API 请求"""
    log("=" * 50)
    log("收到 API 请求")

    try:
        # 解析请求
        anthropic_request = request.json
        log(f"请求头: {dict(request.headers)}")

        # 转换格式
        openai_request = convert_to_openai_format(anthropic_request)

        # 发送到智谱
        headers = {
            "Authorization": f"Bearer {ZHIPU_API_KEY}",
            "Content-Type": "application/json"
        }

        url = f"{ZHIPU_BASE_URL}/v4/chat/completions"
        log(f"发送到: {url}")

        try:
            response = requests.post(
                url,
                headers=headers,
                json=openai_request,
                timeout=60
            )
            log(f"智谱响应状态码: {response.status_code}")

            if response.status_code != 200:
                log(f"智谱错误响应: {response.text}")
                return Response(
                    json.dumps({"error": f"智谱 API 错误: {response.text}"}),
                    status=response.status_code,
                    content_type='application/json'
                )

            zhipu_response = response.json()

            # 转换回 Anthropic 格式
            anthropic_response = convert_to_anthropic_format(zhipu_response)

            log("请求成功完成")

            return Response(
                json.dumps(anthropic_response),
                content_type='application/json'
            )

        except requests.exceptions.Timeout:
            log("请求超时")
            return Response(
                json.dumps({"error": "请求超时"}),
                status=504,
                content_type='application/json'
            )
        except requests.exceptions.RequestException as e:
            log(f"请求错误: {e}")
            return Response(
                json.dumps({"error": f"请求失败: {str(e)}"}),
                status=500,
                content_type='application/json'
            )

    except Exception as e:
        log(f"服务器错误: {e}")
        import traceback
        traceback.print_exc()
        return Response(
            json.dumps({"error": f"内部错误: {str(e)}"}),
            status=500,
            content_type='application/json'
        )

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return Response(
        json.dumps({
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "zhipu_base": ZHIPU_BASE_URL,
            "model_mapping": MODEL_MAPPING
        }),
        content_type='application/json'
    )

@app.route('/', methods=['GET'])
def index():
    """首页"""
    return Response("""
    <html>
    <head>
        <title>Claude Code ↔ 智谱 API 代理 v2</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>🤖 Claude Code ↔ 智谱 API 代理服务器 v2</h1>
        <p><strong>运行中...</strong></p>
        <p><a href="/health">健康检查</a></p>
        <h2>端点：</h2>
        <ul>
            <li>/v1/messages</li>
            <li>/api/anthropic/v1/messages</li>
        </ul>
        <h2>功能：</h2>
        <ul>
            <li>Anthropic 格式 ←→ 智谱 OpenAI 格式转换</li>
            <li>模型映射: Claude 模型 → glm-4.7</li>
            <li>系统提示词支持</li>
        </ul>
    </body>
    </html>
    """, content_type='text/html')

if __name__ == '__main__':
    log("=" * 60)
    log("Claude Code ↔ 智谱 API 代理服务器 v2 启动中...")
    log(f"智谱 API 端点: {ZHIPU_BASE_URL}")
    log(f"监听端口: 8080")
    log("=" * 60)

    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
