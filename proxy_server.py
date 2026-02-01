#!/usr/bin/env python3
"""
Claude Code ↔ 智谱 GLM API 代理服务器
Anthropic 格式 ←→ 智谱 OpenAI 兼容格式
"""

from flask import Flask, request, Response, stream_with_context
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
    "claude-sonnet-4-5-20250929-anthropic-v1:claude-sonnet-4-5-20250929": "glm-4.7",
}

def convert_anthropic_to_zhipu(anthropic_request):
    """转换 Anthropic 格式到智谱格式"""
    log(f"转换请求: {anthropic_request.get('model', 'unknown')}")

    # 提取模型名称
    model = anthropic_request.get("model", "claude-sonnet-4-5-20250929")
    # 处理带前缀的模型名称
    if ":" in model:
        model = model.split(":")[-1]

    # 映射到智谱模型
    zhipu_model = MODEL_MAPPING.get(model, "glm-4.7")
    log(f"映射模型: {model} -> {zhipu_model}")

    # 提取系统提示词和消息
    system = anthropic_request.get("system", "")
    messages = anthropic_request.get("messages", [])

    # 构建 OpenAI 兼容格式
    zhipu_request = {
        "model": zhipu_model,
        "messages": [],
        "stream": anthropic_request.get("stream", True)
    }

    # 添加系统提示词（如果有）
    if system:
        if isinstance(system, str):
            zhipu_request["messages"].append({
                "role": "system",
                "content": system
            })
        elif isinstance(system, list):
            # 处理系统提示词中的内容块
            for item in system:
                if item.get("type") == "text":
                    zhipu_request["messages"].append({
                        "role": "system",
                        "content": item.get("text", "")
                    })

    # 转换消息格式
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")

        if isinstance(content, str):
            zhipu_request["messages"].append({
                "role": role,
                "content": content
            })
        elif isinstance(content, list):
            # 处理内容块（多模态、工具调用等）
            msg_content = []
            for item in content:
                if item.get("type") == "text":
                    msg_content.append({
                        "type": "text",
                        "text": item.get("text", "")
                    })
                elif item.get("type") == "image":
                    # 简单处理：忽略图片
                    log("警告：暂不支持图片输入")
                elif item.get("type") == "tool_use":
                    # 工具调用 - 转换为 function_call
                    tool_name = item.get("name")
                    tool_input = item.get("input", {})
                    msg_content.append({
                        "type": "function_call",
                        "name": tool_name,
                        "arguments": json.dumps(tool_input)
                    })
                elif item.get("type") == "tool_result":
                    # 工具结果
                    msg_content.append({
                        "type": "function",
                        "name": item.get("tool_use_id"),
                        "content": item.get("content", "")
                    })

            zhipu_request["messages"].append({
                "role": role,
                "content": msg_content
            })

    # 复制其他参数
    if "max_tokens" in anthropic_request:
        zhipu_request["max_tokens"] = anthropic_request["max_tokens"]
    if "temperature" in anthropic_request:
        zhipu_request["temperature"] = anthropic_request["temperature"]
    if "top_p" in anthropic_request:
        zhipu_request["top_p"] = anthropic_request["top_p"]

    log(f"智谱请求: {json.dumps(zhipu_request, ensure_ascii=False)[:200]}...")
    return zhipu_request

@app.route('/v1/messages', methods=['POST'])
@app.route('/api/anthropic/v1/messages', methods=['POST'])
def create_message():
    """处理 Anthropic Messages API 请求"""
    log("收到 Anthropic 请求")

    try:
        # 解析 Anthropic 请求
        anthropic_request = request.json

        # 转换为智谱格式
        zhipu_request = convert_anthropic_to_zhipu(anthropic_request)

        # 发送到智谱 API
        headers = {
            "Authorization": f"Bearer {ZHIPU_API_KEY}",
            "Content-Type": "application/json"
        }

        url = f"{ZHIPU_BASE_URL}/v4/chat/completions"

        if zhipu_request.get("stream", True):
            # 流式响应
            def generate():
                log("开始流式请求")
                try:
                    response = requests.post(
                        url,
                        headers=headers,
                        json=zhipu_request,
                        stream=True,
                        timeout=60
                    )
                    response.raise_for_status()

                    for line in response.iter_lines():
                        if line:
                            line = line.decode('utf-8')
                            if line.startswith('data: '):
                                data_str = line[6:]
                                if data_str == '[DONE]':
                                    break
                                try:
                                    data = json.loads(data_str)
                                    # 转换回 Anthropic 格式
                                    if 'choices' in data and len(data['choices']) > 0:
                                        delta = data['choices'][0].get('delta', {})
                                        content = delta.get('content', '')

                                        if content:
                                            # Anthropic SSE 格式
                                            sse_data = {
                                                "type": "content_block_delta",
                                                "index": 0,
                                                "delta": {"type": "text_delta", "text": content}
                                            }
                                            yield f"event: message_delta\ndata: {json.dumps(sse_data)}\n\n"

                                except json.JSONDecodeError:
                                    pass

                    log("流式请求完成")

                except Exception as e:
                    log(f"流式请求错误: {e}")
                    yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

            return Response(stream_with_context(generate()),
                          content_type='text/event-stream')

        else:
            # 非流式响应
            log("开始非流式请求")
            response = requests.post(
                url,
                headers=headers,
                json=zhipu_request,
                timeout=60
            )
            response.raise_for_status()

            result = response.json()

            log("非流式请求完成")

            # 转换回 Anthropic 格式
            anthropic_response = {
                "id": f"msg_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                "type": "message",
                "role": "assistant",
                "model": zhipu_request["model"],
                "content": [],
                "stop_reason": "end_turn",
                "usage": result.get("usage", {})
            }

            if 'choices' in result and len(result['choices']) > 0:
                content_text = result['choices'][0].get('message', {}).get('content', '')
                anthropic_response["content"].append({
                    "type": "text",
                    "text": content_text
                })

            return Response(json.dumps(anthropic_response),
                          content_type='application/json')

    except Exception as e:
        log(f"错误: {e}")
        return Response(json.dumps({"error": str(e)}),
                      status=500,
                      content_type='application/json')

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return Response(json.dumps({"status": "ok", "timestamp": datetime.now().isoformat()}),
                  content_type='application/json')

@app.route('/', methods=['GET'])
def index():
    """首页"""
    html = """
    <html>
    <head><title>Claude Code ↔ 智谱 API 代理</title></head>
    <body>
        <h1>🤖 Claude Code ↔ 智谱 API 代理服务器</h1>
        <p>运行中...</p>
        <p><a href="/health">健康检查</a></p>
        <h2>配置：</h2>
        <ul>
            <li>端点: /v1/messages 或 /api/anthropic/v1/messages</li>
            <li>模型映射: Claude 模型 → glm-4.7</li>
        </ul>
    </body>
    </html>
    """
    return Response(html, content_type='text/html')

if __name__ == '__main__':
    log("=" * 60)
    log("Claude Code ↔ 智谱 API 代理服务器启动中...")
    log(f"智谱 API 端点: {ZHIPU_BASE_URL}")
    log(f"监听端口: 8080")
    log("=" * 60)

    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
