#!/usr/bin/env python3
"""
优化的 Claude Code 代理服务 v3
添加了性能优化、更多错误处理、缓存支持等
"""

import requests
from flask import Flask, request, jsonify, Response
from functools import lru_cache
from datetime import datetime
import hashlib
import json
import logging
from concurrent.futures import ThreadPoolExecutor
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('proxy_v3.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

# 线程池
executor = ThreadPoolExecutor(max_workers=10)

# 智谱 API 配置
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
ZHIPU_API_KEY = "your-zhipu-api-key"

# 模型映射
MODEL_MAPPING = {
    "claude-haiku-4-5-20251001": "glm-4.7",
    "claude-sonnet-4-5-20250929": "glm-4.7",
    "claude-opus-4-5-20250929": "glm-4.7"
}

# 缓存配置
CACHE_TTL = 3600  # 1小时

# 简单的内存缓存
cache = {}

def cache_get(key):
    """获取缓存"""
    if key in cache:
        item = cache[key]
        if time.time() - item['time'] < CACHE_TTL:
            return item['value']
        else:
            del cache[key]
    return None

def cache_set(key, value):
    """设置缓存"""
    cache[key] = {
        'value': value,
        'time': time.time()
    }

def generate_cache_key(model, messages, max_tokens):
    """生成缓存键"""
    content = f"{model}_{json.dumps(messages, sort_keys=True)}_{max_tokens}"
    return hashlib.md5(content.encode()).hexdigest()


def validate_api_key(api_key):
    """验证 API Key（简化版）"""
    if not api_key or len(api_key) < 10:
        return False
    return True


def transform_request(data):
    """转换请求格式"""
    original_model = data.get('model', 'claude-sonnet-4-5-20250929')
    mapped_model = MODEL_MAPPING.get(original_model, 'glm-4.7')

    # 系统提示词处理
    system_message = None
    messages = data.get('messages', [])
    if messages and messages[0].get('role') == 'system':
        system_message = messages[0]
        messages = messages[1:]

    zhipu_data = {
        "model": mapped_model,
        "messages": messages,
        "stream": data.get('stream', False),
        "max_tokens": data.get('max_tokens', 200),
        "temperature": data.get('temperature', 0.7)
    }

    # 添加系统提示词
    if system_message:
        # 智谱 API 不支持 system 角色，可以将其添加到第一个 user 消息
        if zhipu_data['messages']:
            zhipu_data['messages'][0]['content'] = f"{system_message['content']}\n\n{zhipu_data['messages'][0]['content']}"
        else:
            zhipu_data['messages'].append({
                "role": "user",
                "content": system_message['content']
            })

    return zhipu_data, original_model


def transform_response(zhipu_response, original_model):
    """转换响应格式"""
    try:
        choices = zhipu_response.get('choices', [])
        if not choices:
            raise ValueError("No choices in response")

        choice = choices[0]
        finish_reason = choice.get('finish_reason', 'stop')
        message = choice.get('message', {})
        content = message.get('content', '')

        # 处理空内容
        if not content and 'reasoning_content' in message:
            content = message['reasoning_content']

        # 生成响应 ID
        response_id = f"msg_{hashlib.md5(content.encode()).hexdigest()[:12]}"

        response = {
            "id": response_id,
            "type": "message",
            "role": "assistant",
            "content": [{"type": "text", "text": content}],
            "model": original_model,
            "stop_reason": finish_reason
        }

        # 添加使用情况
        if 'usage' in zhipu_response:
            response['usage'] = zhipu_response['usage']

        return response

    except Exception as e:
        logger.error(f"转换响应失败: {e}")
        raise


def call_zhipu_api(zhipu_data, retry=3):
    """调用智谱 API"""
    for attempt in range(retry):
        try:
            logger.info(f"尝试调用智谱 API（第 {attempt + 1} 次）")

            headers = {
                "Authorization": f"Bearer {ZHIPU_API_KEY}",
                "Content-Type": "application/json"
            }

            start_time = time.time()
            response = requests.post(
                ZHIPU_API_URL,
                json=zhipu_data,
                headers=headers,
                timeout=30
            )
            elapsed_time = time.time() - start_time

            logger.info(f"智谱 API 响应时间: {elapsed_time:.2f}秒")

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                logger.warning(f"API 限流，等待后重试")
                time.sleep(2 ** attempt)  # 指数退避
                continue
            else:
                error_msg = f"智谱 API 错误: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)

        except requests.exceptions.Timeout:
            logger.warning(f"请求超时，第 {attempt + 1} 次重试")
            if attempt < retry - 1:
                time.sleep(2 ** attempt)
                continue
            raise

    raise Exception("智谱 API 调用失败，已达到最大重试次数")


@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "version": "3.0",
        "zhipu_base": ZHIPU_API_URL,
        "model_mapping": MODEL_MAPPING,
        "cache_size": len(cache)
    }), 200


@app.route('/v1/messages', methods=['POST', 'OPTIONS'])
def proxy_messages():
    """代理 API 请求"""
    if request.method == 'OPTIONS':
        # 处理 CORS 预检请求
        response = Response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-API-Key'
        return response, 200

    try:
        # 获取请求数据
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # 验证 API Key
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "Missing API Key"}), 401

        if not validate_api_key(api_key):
            return jsonify({"error": "Invalid API Key"}), 401

        # 记录请求
        logger.info(f"收到 API 请求 - 模型: {data.get('model', 'unknown')}, 消息数: {len(data.get('messages', []))}")

        # 检查缓存
        cache_key = generate_cache_key(
            data.get('model', ''),
            data.get('messages', []),
            data.get('max_tokens', 200)
        )

        cached_response = cache_get(cache_key)
        if cached_response:
            logger.info("返回缓存响应")
            response = jsonify(cached_response)
            response.headers['X-Cache'] = 'HIT'
            return response

        # 转换请求
        logger.info("转换请求格式")
        zhipu_data, original_model = transform_request(data)

        # 记录转换后的请求（截断）
        request_str = json.dumps(zhipu_data, ensure_ascii=False)
        logger.info(f"转换后的请求: {request_str[:200]}...")

        # 调用智谱 API
        logger.info("发送到智谱 API")
        zhipu_response = call_zhipu_api(zhipu_data)

        # 记录响应（截断）
        response_str = json.dumps(zhipu_response, ensure_ascii=False)
        logger.info(f"智谱响应: {response_str[:200]}...")

        # 转换响应格式
        logger.info("转换响应格式")
        response = transform_response(zhipu_response, original_model)

        # 缓存响应
        cache_set(cache_key, response)

        # 设置 CORS 头
        response_obj = jsonify(response)
        response_obj.headers['Access-Control-Allow-Origin'] = '*'
        response_obj.headers['X-Cache'] = 'MISS'

        logger.info("请求成功完成")
        return response_obj, 200

    except Exception as e:
        logger.error(f"请求处理失败: {e}", exc_info=True)
        return jsonify({
            "error": str(e),
            "type": type(e).__name__
        }), 500


@app.route('/stats', methods=['GET'])
def stats():
    """统计信息"""
    return jsonify({
        "cache_size": len(cache),
        "cache_ttl": CACHE_TTL,
        "model_mapping": MODEL_MAPPING,
        "uptime": time.time()
    }), 200


@app.route('/cache/clear', methods=['POST'])
def clear_cache():
    """清空缓存"""
    cache.clear()
    return jsonify({"message": "缓存已清空"}), 200


if __name__ == '__main__':
    print("=" * 60)
    print("Claude Code ↔ 智谱 API 代理服务器 v3 启动中...")
    print("=" * 60)
    print(f"智谱 API 端点: {ZHIPU_API_URL}")
    print(f"监听端口: 8080")
    print(f"缓存 TTL: {CACHE_TTL}秒")
    print("=" * 60)

    # 运行 Flask 应用
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
