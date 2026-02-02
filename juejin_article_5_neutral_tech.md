# Flask + 智谱 AI GLM-4 API 接入完整指南

## 前言

本文将详细介绍如何使用 Flask 框架接入智谱 AI GLM-4 模型，从零开始构建一个对话完成 API 服务。

## 模型概述

### 智谱 AI GLM-4 模型介绍

GLM-4 是智谱 AI 发布的对话大语言模型，支持中英文对话，具有以下特性：

- **上下文理解** - 理解长对话历史
- **多轮对话** - 支持多轮连续对话
- **代码生成** - 支持代码生成和补全
- **多模态** - 支持图片、音频等多模态输入

### API 基本信息

| 特性 | 说明 |
|------|------|
| **API 端点** | https://open.bigmodel.cn/api/paas/v4/chat/completions |
| **认证方式** | Bearer Token |
| **请求方法** | POST |
| **响应格式** | JSON |

## 技术实现

### 1. Flask 基础框架

```python
from flask import Flask, request, jsonify
import logging

# 创建 Flask 应用
app = Flask(__name__)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 2. 请求处理中间件

```python
from functools import wraps
import time

def log_request(f):
    """请求日志中间件"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        response = f(*args, **kwargs)
        duration = (time.time() - start_time) * 1000
        logging.info(f"{request.method} {request.path} - {response.status_code} - {duration:.2f}ms")
        return response
    return decorated_function

app.before_request(log_request)
```

### 3. 智谱 AI API 客户端

```python
import requests

class GLMClient:
    """智谱 AI GLM-4 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        self.session = requests.Session()
    
    def chat_completion(self, messages: list, model: str = "glm-4", 
                        max_tokens: int = 1024, stream: bool = False,
                        temperature: float = 0.7, top_p: float = 0.9):
        """
        调用智谱 AI 对话完成接口
        
        Args:
            messages: 对话历史
            model: 模型名称 (glm-4, glm-4-flash, glm-4-0520)
            max_tokens: 最大生成 tokens
            stream: 是否流式输出
            temperature: 温度参数
            top_p: Top-P 采样参数
        
        Returns:
            API 响应数据
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": stream,
            "temperature": temperature,
            "top_p": top_p
        }
        
        try:
            response = self.session.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"GLM API 调用失败：{response.status_code}")
                return {
                    "success": False,
                    "error": f"API 调用失败：{response.status_code}"
                }
                
        except Exception as e:
            logging.error(f"GLM API 调用异常：{str(e)}")
            return {
                "success": False,
                "error": f"API 调用异常：{str(e)}"
            }
```

### 4. Flask 路由实现

```python
# 初始化客户端
# 注意：请在实际使用时替换为你的 API Key
glm_client = GLMClient(api_key="your-glm-api-key")

@app.route('/api/chat', methods=['POST'])
def chat():
    """对话接口"""
    
    try:
        # 获取请求数据
        request_data = request.get_json()
        
        # 提取参数
        messages = request_data.get("messages", [])
        model = request_data.get("model", "glm-4")
        max_tokens = request_data.get("max_tokens", 1024)
        temperature = request_data.get("temperature", 0.7)
        top_p = request_data.get("top_p", 0.9)
        
        # 记录请求日志
        logging.info(f"收到对话请求，模型：{model}，消息数：{len(messages)}")
        
        # 调用 GLM API
        response = glm_client.chat_completion(
            messages=messages,
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )
        
        if response.get("success", True):
            choices = response.get("choices", [])
            if choices:
                choice = choices[0]
                message = choice.get("message", {}).get("content", "")
                
                return jsonify({
                    "success": True,
                    "data": {
                        "id": f"chat-{int(time.time())}",
                        "object": "chat.completion",
                        "created": int(time.time()),
                        "model": model,
                        "choices": [{
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": message
                            },
                            "finish_reason": choice.get("finish_reason", "stop")
                        }]
                    }
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "API 返回数据格式错误"
                }), 500
        else:
            return jsonify({
                "success": False,
                "error": response.get("error", "Unknown error")
            }), 500
            
    except Exception as e:
        logging.error(f"对话接口失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500
```

### 5. 错误处理

```python
@app.errorhandler(400)
def bad_request(error):
    """400 错误处理"""
    return jsonify({
        "success": False,
        "error": "Bad request",
        "message": str(error)
    }), 400

@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({
        "success": False,
        "error": "Not found",
        "message": str(error)
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "message": str(error)
    }), 500
```

### 6. 流式输出实现

```python
from flask import Response

@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """流式对话接口"""
    
    try:
        # 获取请求数据
        request_data = request.get_json()
        
        messages = request_data.get("messages", [])
        model = request_data.get("model", "glm-4")
        max_tokens = request_data.get("max_tokens", 1024)
        temperature = request_data.get("temperature", 0.7)
        top_p = request_data.get("top_p", 0.9)
        
        # 调用 GLM API（流式）
        headers = {
            "Authorization": f"Bearer {glm_client.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": True,
            "temperature": temperature,
            "top_p": top_p
        }
        
        response = glm_client.session.post(
            glm_client.api_url,
            headers=headers,
            json=payload,
            stream=True,
            timeout=60
        )
        
        def generate():
            for line in response.iter_lines():
                if line:
                    yield line + "\n"
        
        return Response(
            generate(),
            mimetype="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
            }
        )
        
    except Exception as e:
        logging.error(f"流式对话接口失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500
```

### 7. 多轮对话实现

```python
@app.route('/api/chat/multi-turn', methods=['POST'])
def chat_multi_turn():
    """多轮对话接口"""
    
    try:
        # 获取请求数据
        request_data = request.get_json()
        
        # 多轮对话历史
        messages = request_data.get("messages", [])
        system_prompt = request_data.get("system_prompt", "")
        
        # 如果有系统提示词，添加到第一条
        if system_prompt and len(messages) > 0:
            messages[0] = {
                "role": "system",
                "content": system_prompt
            }
        
        # 调用 GLM API
        response = glm_client.chat_completion(messages=messages)
        
        if response.get("success", True):
            choices = response.get("choices", [])
            if choices:
                choice = choices[0]
                message = choice.get("message", {}).get("content", "")
                
                # 将助手回复添加到历史
                messages.append({
                    "role": "assistant",
                    "content": message
                })
                
                return jsonify({
                    "success": True,
                    "data": {
                        "message": message,
                        "messages": messages,
                        "finish_reason": choice.get("finish_reason", "stop")
                    }
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "API 返回数据格式错误"
                }), 500
        else:
            return jsonify({
                "success": False,
                "error": response.get("error", "Unknown error")
            }), 500
            
    except Exception as e:
        logging.error(f"多轮对话接口失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500
```

### 8. 输入验证

```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """对话请求模型"""
    
    model: str = Field(..., description="模型名称")
    max_tokens: int = Field(1, 8192, description="最大 tokens")
    temperature: float = Field(0.0, 2.0, description="温度参数")
    top_p: float = Field(0.0, 1.0, description="Top-P 采样参数")
    messages: list = Field(..., min_items=1, description="对话历史")
    system_prompt: str = Field("", description="系统提示词")

@app.route('/api/chat/validated', methods=['POST'])
def chat_validated():
    """带输入验证的对话接口"""
    
    try:
        # 解析和验证请求
        request_data = request.get_json()
        validated_data = ChatRequest(**request_data)
        
        # 验证消息数量
        if len(validated_data.messages) > 10:
            return jsonify({
                "success": False,
                "error": "Too many messages",
                "message": "消息数量不能超过 10 条"
            }), 400
        
        # 验证 tokens 限制
        if validated_data.max_tokens > 8192:
            return jsonify({
                "success": False,
                "error": "Max tokens too large",
                "message": "Max tokens 不能超过 8192"
            }), 400
        
        # 调用 GLM API
        response = glm_client.chat_completion(
            messages=validated_data.messages,
            model=validated_data.model,
            max_tokens=validated_data.max_tokens,
            temperature=validated_data.temperature,
            top_p=validated_data.top_p
        )
        
        if response.get("success", True):
            choices = response.get("choices", [])
            if choices:
                choice = choices[0]
                message = choice.get("message", {}).get("content", "")
                
                return jsonify({
                    "success": True,
                    "data": {
                        "message": message,
                        "model": validated_data.model,
                        "max_tokens": validated_data.max_tokens
                    }
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "API 返回数据格式错误"
                }), 500
        else:
            return jsonify({
                "success": False,
                "error": response.get("error", "Unknown error")
            }), 500
            
    except Exception as e:
        logging.error(f"验证对话接口失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500
```

### 9. 会话管理

```python
from collections import defaultdict
import uuid

# 会话存储
sessions = defaultdict(dict)

@app.route('/api/chat/session/create', methods=['POST'])
def create_session():
    """创建对话会话"""
    
    try:
        # 生成会话 ID
        session_id = str(uuid.uuid4())
        
        # 获取系统提示词
        request_data = request.get_json()
        system_prompt = request_data.get("system_prompt", "")
        
        # 初始化会话
        sessions[session_id] = {
            "messages": [],
            "system_prompt": system_prompt,
            "created_at": int(time.time())
        }
        
        return jsonify({
            "success": True,
            "data": {
                "session_id": session_id,
                "created_at": sessions[session_id]["created_at"]
            }
        })
        
    except Exception as e:
        logging.error(f"创建会话失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/api/chat/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """获取对话会话"""
    
    try:
        if session_id not in sessions:
            return jsonify({
                "success": False,
                "error": "Session not found"
            }), 404
        
        session = sessions[session_id]
        
        return jsonify({
            "success": True,
            "data": {
                "session_id": session_id,
                "system_prompt": session.get("system_prompt", ""),
                "messages": session.get("messages", []),
                "message_count": len(session.get("messages", [])),
                "created_at": session.get("created_at")
            }
        })
        
    except Exception as e:
        logging.error(f"获取会话失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500
```

### 10. 速率限制

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# 创建限流器
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per hour", "1000 per day"]
)

@app.route('/api/chat/limited', methods=['POST'])
@limiter.limit("10 per minute")
def chat_limited():
    """带速率限制的对话接口"""
    
    try:
        # 限制：每分钟 10 次
        # 获取请求数据
        request_data = request.get_json()
        messages = request_data.get("messages", [])
        
        # 调用 GLM API
        response = glm_client.chat_completion(messages=messages)
        
        if response.get("success", True):
            choices = response.get("choices", [])
            if choices:
                choice = choices[0]
                message = choice.get("message", {}).get("content", "")
                
                return jsonify({
                    "success": True,
                    "data": {
                        "message": message,
                        "remaining_requests": 60  # 示例值
                    }
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "API 返回数据格式错误"
                }), 500
        else:
            return jsonify({
                "success": False,
                "error": response.get("error", "Unknown error")
            }), 500
            
    except Exception as e:
        logging.error(f"限流对话接口失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500
```

## 测试方法

### 1. 单元测试

```python
import unittest

class TestGLMClient(unittest.TestCase):
    """测试 GLM 客户端"""
    
    def setUp(self):
        self.client = GLMClient(api_key="test-api-key")
    
    def test_chat_completion(self):
        """测试对话完成"""
        
        messages = [
            {"role": "user", "content": "你好"}
        ]
        
        response = self.client.chat_completion(messages=messages)
        
        # 验证响应结构
        self.assertIn("success", response)
        self.assertIn("choices", response.get("data", {}))
```

### 2. 集成测试

```python
def test_chat_endpoint():
    """测试对话接口"""
    
    url = "http://localhost:8080/api/chat"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "model": "glm-4",
        "max_tokens": 200,
        "messages": [
            {"role": "user", "content": "你好，介绍一下你自己"}
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
```

## 部署说明

### 1. 环境变量

```bash
# 智谱 AI API Key
export GLM_API_KEY="your-glm-api-key"

# Flask 配置
export FLASK_ENV="production"
export FLASK_DEBUG="False"
```

### 2. 启动应用

```bash
# 开发模式
python app.py

# 生产模式（使用 Gunicorn）
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

### 3. 使用 Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8080

# 启动应用
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
```

### 4. 使用 Systemd

```ini
[Unit]
Description=GLM API Service
After=network.target

[Service]
Type=simple
User=root
Environment="GLM_API_KEY=your-glm-api-key"
WorkingDirectory=/path/to/app
ExecStart=/usr/bin/python3 /path/to/app/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 总结

本文详细介绍了 Flask + 智谱 AI GLM-4 API 接入的完整实现，包括：

1. **技术实现** - Flask 框架、GLM API 客户端、路由实现
2. **流式输出** - 支持流式对话响应
3. **多轮对话** - 支持多轮连续对话
4. **会话管理** - 支持对话会话存储和检索
5. **速率限制** - 防止 API 滥用
6. **错误处理** - 统一的错误处理机制
7. **部署方案** - Docker 和 Systemd 部署
8. **测试方法** - 单元测试和集成测试

通过本文的介绍，你应该能够成功接入智谱 AI GLM-4 模型。

如果本文对你有帮助，欢迎点赞、收藏和评论！

---

**技术栈：** Python 3.11, Flask 2.0+, 智谱 AI GLM-4
**难度：** 中等
**预计时间：** 4-6 小时完成基础版本，1-2 周完善版本
**适用场景：** AI 应用开发、API 接入、对话系统开发

---

**作者：** AI 开发者
**发布时间：** 2026-02-02
