# Flask + 智谱 AI GLM-4 API 开发实战

## 前言

在日常开发中，我们经常需要集成大语言模型（LLM）API 到我们的应用中。本文将详细介绍如何使用 Flask 框架和智谱 AI GLM-4 模型，从零开始构建一个企业级的 API 服务。

## 为什么选择智谱 AI GLM-4？

### 性能对比

| 特性 | Claude | GPT-4 | 智谱 GLM-4.7 |
|------|--------|--------|----------------|
| 中文能力 | 85/100 | 90/100 | 95/100 |
| 性能 | 1500 tokens/s | 1800 tokens/s | 2000+ tokens/s |
| API 延迟 | 200ms | 150ms | 100ms |
| 价格 | $15/1M tokens | $10/1M tokens | ¥8/1M tokens |

### 技术选型理由

从技术角度来看，智谱 AI GLM-4.7 具有以下优势：

1. **性能优秀** - 响应延迟低，并发处理能力强
2. **成本更低** - 相比 Claude API 成本降低 80%+
3. **中文优化** - 专门优化中文理解和生成
4. **技术文档完善** - 详细的中文技术文档和示例
5. **稳定性高** - 提供 99.9% 的可用性承诺

## 核心技术实现

### 1. Flask 框架基础

```python
from flask import Flask, request, jsonify
import logging
import time
from typing import Dict, Any, Optional

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

def request_logging(f):
    """请求日志中间件"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        response = f(*args, **kwargs)
        duration = (time.time() - start_time) * 1000
        logging.info(f"{request.method} {request.path} - {response.status_code} - {duration:.2f}ms")
        return response
    return decorated_function

app.before_request(request_logging)
```

### 3. 智谱 AI API 客户端

```python
import requests
import json

class ZhipuAIClient:
    """智谱 AI API 客户端"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        self.session = requests.Session()
    
    def chat_completion(self, messages: list, model: str = "glm-4", 
                        max_tokens: int = 1024, stream: bool = False):
        """调用智谱 AI 对话完成接口"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": stream
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
                logging.error(f"智谱 AI API 调用失败：{response.status_code}")
                return {
                    "success": False,
                    "error": f"API 调用失败：{response.status_code}"
                }
                
        except Exception as e:
            logging.error(f"智谱 AI API 调用异常：{str(e)}")
            return {
                "success": False,
                "error": f"API 调用异常：{str(e)}"
            }
```

### 4. 消息格式转换器

```python
class MessageConverter:
    """消息格式转换器"""
    
    @staticmethod
    def convert_to_zhipu_format(messages: list) -> list:
        """将通用消息格式转换为智谱 AI 格式"""
        
        zhipu_messages = []
        
        for message in messages:
            if message["role"] == "system":
                zhipu_messages.append({
                    "role": "system",
                    "content": message["content"]
                })
            elif message["role"] == "user":
                zhipu_messages.append({
                    "role": "user",
                    "content": message["content"]
                })
        
        return zhipu_messages
```

### 5. Flask 路由实现

```python
# 实例化转换器和客户端
converter = MessageConverter()
zhipu_client = ZhipuAIClient(api_key="your-zhipu-api-key")

@app.route('/api/chat/completions', methods=['POST'])
def chat_completions():
    """对话完成接口"""
    
    try:
        # 获取请求数据
        request_data = request.get_json()
        
        # 记录请求日志
        logging.info(f"收到对话请求，模型：{request_data.get('model')}")
        
        # 转换消息格式
        zhipu_messages = converter.convert_to_zhipu_format(
            request_data.get("messages", [])
        )
        
        # 调用智谱 AI API
        api_response = zhipu_client.chat_completion(
            messages=zhipu_messages,
            model=request_data.get("model", "glm-4"),
            max_tokens=request_data.get("max_tokens", 1024)
        )
        
        if api_response.get("success", True):
            # 提取响应数据
            choice = api_response.get("choices", [{}])[0]
            
            response_data = {
                "id": f"msg-{int(time.time())}",
                "type": "message",
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": choice.get("message", {}).get("content", "")
                    }
                ],
                "model": request_data.get("model"),
                "stop_reason": choice.get("finish_reason", "stop")
            }
            
            return jsonify({
                "success": True,
                "data": response_data
            })
        else:
            return jsonify({
                "success": False,
                "error": api_response.get("error", "Unknown error")
            }), 500
            
    except Exception as e:
        logging.error(f"对话完成失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500
```

### 6. 错误处理

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

## 实际应用案例

### 案例 1：智能客服对话

```python
@app.route('/api/customer-service', methods=['POST'])
def customer_service():
    """智能客服对话"""
    
    try:
        # 获取用户问题
        user_question = request.json.get("question")
        
        # 构建上下文
        system_message = "你是一个专业的客服助手，回答用户关于 API 使用的问题。"
        
        # 调用智谱 AI
        response = zhipu_client.chat_completion(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_question}
            ]
        )
        
        if response.get("success", True):
            choice = response.get("choices", [{}])[0]
            assistant_message = choice.get("message", {}).get("content", "")
            
            return jsonify({
                "success": True,
                "assistant_message": assistant_message
            })
        else:
            return jsonify({
                "success": False,
                "error": response.get("error", "Unknown error")
            })
            
    except Exception as e:
        logging.error(f"客服对话失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
```

### 案例 2：文本摘要生成

```python
@app.route('/api/text-summarization', methods=['POST'])
def text_summarization():
    """文本摘要生成"""
    
    try:
        # 获取需要摘要的文本
        text_to_summarize = request.json.get("text")
        summary_length = request.json.get("length", 200)
        
        # 构建提示词
        prompt = f"""
        请为以下文本生成简洁的摘要，长度控制在 {summary_length} 字以内：
        
        文本：{text_to_summarize}
        
        要求：
        1. 提取关键信息
        2. 保持原文的主要意思
        3. 语言简洁明了
        """
        
        # 调用智谱 AI
        response = zhipu_client.chat_completion(
            messages=[{"role": "user", "content": prompt}]
        )
        
        if response.get("success", True):
            choice = response.get("choices", [{}])[0]
            summary = choice.get("message", {}).get("content", "")
            
            return jsonify({
                "success": True,
                "summary": summary
            })
        else:
            return jsonify({
                "success": False,
                "error": response.get("error", "Unknown error")
            })
            
    except Exception as e:
        logging.error(f"文本摘要生成失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
```

### 案例 3：代码生成

```python
@app.route('/api/code-generation', methods=['POST'])
def code_generation():
    """代码生成"""
    
    try:
        # 获取编程语言和需求
        programming_language = request.json.get("language", "Python")
        requirement = request.json.get("requirement")
        
        # 构建提示词
        prompt = f"""
        请用 {programming_language} 编写代码，实现以下功能：
        
        需求：{requirement}
        
        要求：
        1. 代码要有注释
        2. 代码要规范
        3. 要有错误处理
        4. 要有使用示例
        """
        
        # 调用智谱 AI
        response = zhipu_client.chat_completion(
            messages=[{"role": "user", "content": prompt}]
        )
        
        if response.get("success", True):
            choice = response.get("choices", [{}])[0]
            code = choice.get("message", {}).get("content", "")
            
            return jsonify({
                "success": True,
                "language": programming_language,
                "code": code
            })
        else:
            return jsonify({
                "success": False,
                "error": response.get("error", "Unknown error")
            })
            
    except Exception as e:
        logging.error(f"代码生成失败：{str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
```

## 性能优化

### 1. 连接池优化

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 配置重试策略
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)

# 配置连接池
adapter = HTTPAdapter(max_retries=retry_strategy)
zhipu_client.session.mount('https://', adapter)
```

### 2. 缓存优化

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=128)
def get_cached_response(prompt_hash: str):
    """获取缓存响应"""
    # 实现缓存逻辑
    pass

def generate_prompt_hash(prompt: str) -> str:
    """生成提示词的哈希值"""
    return hashlib.md5(prompt.encode()).hexdigest()
```

### 3. 异步处理

```python
import asyncio
import aiohttp

async def async_chat_completion(messages: list):
    """异步调用智谱 AI API"""
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {zhipu_client.api_key}",
            "Content-Type": "application/json"
        }
        
        async with session.post(
            zhipu_client.api_url,
            headers=headers,
            json={"model": "glm-4", "messages": messages}
        ) as response:
            return await response.json()
```

## 安全加固

### 1. 输入验证

```python
from cerberus import Schema, ValidationError

request_schema = Schema({
    'model': str,
    'max_tokens': int,
    'messages': list
})

@app.route('/api/chat/completions', methods=['POST'])
def create_message_with_validation():
    """带输入验证的接口"""
    
    try:
        # 验证请求数据
        request_data = request_schema.validate(request.get_json())
        
        # 限制 max_tokens
        if request_data['max_tokens'] > 4096:
            return jsonify({
                "success": False,
                "error": "max_tokens too large",
                "message": "max_tokens 不能超过 4096"
            }), 400
            
        # 限制消息数量
        if len(request_data['messages']) > 10:
            return jsonify({
                "success": False,
                "error": "too many messages",
                "message": "消息数量不能超过 10 条"
            }), 400
            
    except ValidationError as e:
        return jsonify({
            "success": False,
            "error": "validation error",
            "message": str(e)
        }), 400
```

### 2. 速率限制

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour", "1000 per day"]
)

@app.route('/api/chat/completions', methods=['POST'])
@limiter.limit("10 per minute")
def create_message_with_rate_limit():
    """带速率限制的接口"""
    # 实现逻辑
    pass
```

## 部署方案

### 1. Docker 部署

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
CMD ["python", "app.py"]
```

### 2. Systemd 服务

```ini
[Unit]
Description=AI API Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/app
ExecStart=/usr/bin/python3 /path/to/app/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Nginx 反向代理

```nginx
upstream ai_api {
    server 127.0.0.1:8080;
    keepalive 64;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://ai_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 测试方法

### 单元测试

```python
import unittest

class TestMessageConverter(unittest.TestCase):
    """测试消息转换器"""
    
    def setUp(self):
        self.converter = MessageConverter()
    
    def test_convert_to_zhipu_format(self):
        """测试格式转换"""
        
        messages = [
            {"role": "system", "content": "你是一个有用的助手"},
            {"role": "user", "content": "你好"}
        ]
        
        zhipu_messages = self.converter.convert_to_zhipu_format(messages)
        
        # 验证结果
        self.assertEqual(len(zhipu_messages), 2)
        self.assertEqual(zhipu_messages[0]["role"], "system")
        self.assertEqual(zhipu_messages[1]["role"], "user")
```

### 集成测试

```python
def test_api_endpoint():
    """测试 API 端点"""
    
    url = "http://localhost:8080/api/chat/completions"
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
    assert "assistant_message" in data or "error" in data
```

## 最佳实践

### 1. 代码组织

```
project/
├── app.py              # 主应用
├── models/             # 数据模型
├── services/            # 业务逻辑
│   ├── message_converter.py
│   ├── zhipu_client.py
│   └── rate_limiter.py
├── utils/               # 工具函数
│   ├── logger.py
│   ├── validator.py
│   └── cache.py
├── tests/               # 测试文件
└── requirements.txt      # 依赖文件
```

### 2. 配置管理

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """配置类"""
    
    # 智谱 AI 配置
    ZHIPU_API_KEY = os.getenv('ZHIPU_API_KEY')
    ZHIPU_API_URL = os.getenv('ZHIPU_API_URL', 'https://open.bigmodel.cn/api/paas/v4/chat/completions')
    
    # Flask 配置
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    
    # 速率限制配置
    RATE_LIMIT = os.getenv('RATE_LIMIT', '1000 per day')
```

### 3. 日志管理

```python
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 文件日志
file_handler = RotatingFileHandler(
    'logs/api.log',
    maxBytes=1024*1024,
    backupCount=5
)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# 控制台日志
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)
```

## 总结

本文详细介绍了基于 Flask 和智谱 AI GLM-4 的 API 服务开发实战，包括：

1. **架构设计** - 完整的技术架构和组件设计
2. **核心组件** - 消息转换器、API 客户端、Flask 路由
3. **实际应用** - 智能客服、文本摘要、代码生成等案例
4. **性能优化** - 连接池、缓存、异步处理
5. **安全加固** - 输入验证、速率限制
6. **部署方案** - Docker、Systemd、Nginx 部署
7. **测试方法** - 单元测试和集成测试
8. **最佳实践** - 代码组织、配置管理、日志管理

通过本文的介绍，你应该能够构建一个稳定、高效的 AI API 服务。

如果本文对你有帮助，欢迎点赞、收藏和评论！

---

**技术栈：** Python 3.11, Flask 2.0+, 智谱 AI GLM-4.7
**难度：** 中等
**预计时间：** 4-6 小时完成基础版本，1-2 周完善版本
**适用场景：** AI 应用开发、API 服务搭建、企业级应用
