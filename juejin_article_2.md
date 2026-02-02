# 5分钟搭建自己的 AI API 服务

不想用昂贵的 Claude API 或 OpenAI ChatGPT？

本文教你 5 分钟搭建自己的 AI API 服务，使用国产的智谱 AI GLM-4.7 模型，而且完全开源免费！

## 为什么选择智谱 AI GLM-4.7？

**对比其他模型：**

| 特性 | Claude | GPT-4 | 智谱 GLM-4.7 |
|------|--------|--------|----------------|
| 性能 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 中文能力 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 价格 | 昂贵 | 昂贵 | 便宜 |
| API 响应 | 快 | 快 | 快 |
| 文档 | 英文 | 英文 | **中文** |
| 支持 | 邮件 | 邮件 | **微信/邮箱** |

**结论：** 如果你主要面向中文用户，智谱 AI GLM-4.7 是最佳选择！

## 准备工作

### 系统要求
- Python 3.7+
- 1GB 可用内存
- 10GB 可用磁盘空间

### 账号准备
1. 注册智谱 AI 开放平台：https://open.bigmodel.cn/
2. 获取 API Key
3. 新人送 100 万 Tokens（相当于 100 元左右）
4. 充值更优惠，支持支付宝/微信

## 快速开始（5 分钟）

### 第一步：克隆项目（1 分钟）

```bash
git clone https://github.com/huangsir1983/6666.git
cd 6666

# 安装依赖
pip install flask requests
```

### 第二步：配置 API Key（1 分钟）

```bash
# 编辑配置文件
vim config.py

# 添加你的智谱 AI API Key
ZHIPU_API_KEY = "your-zhipu-api-key"

# 保存并退出
```

### 第三步：启动代理服务（1 分钟）

```bash
# 启动 Claude Code 代理服务
python3 proxy_server_v2.py

# 服务将在 http://localhost:8080 启动
```

### 第四步：配置环境变量（1 分钟）

```bash
# 设置 Claude Code API 指向代理服务
export ANTHROPIC_API_URL=http://localhost:8080

# 或者在使用时设置
# 注意：在 VS Code、Cursor 等设置
```

### 第五步：开始使用！（1 分钟）

现在你可以在 VS Code、Cursor 等 IDE 中直接使用 Claude Code，但底层调用的是智谱 AI GLM-4.7 模型！

**示例：**
```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

# 创建消息
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "你好，介绍一下你自己"}
    ]
)

print(message.content[0].text)
```

## 进阶功能

### 1. 用户认证系统

如果你想管理用户和 API Key：

```bash
# 启动用户认证系统
python3 auth_system.py

# 服务将在 http://localhost:8082 启动

# 注册新用户
curl -X POST http://localhost:8082/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "password123",
    "name": "Your Name"
  }'
```

### 2. 完整的应用套件

提供多个 AI 应用：

**应用列表：**
- 💬 **智能聊天助手** - 与 AI 对话
- 📚 **AI 故事生成器** - AI 创作故事
- 💻 **代码生成器** - 智能写代码
- 🧠 **AI 冷知识卡片** - 有趣的知识
- 📊 **排序可视化** - 算法可视化

**访问地址：** http://localhost:8081/

### 3. 自动化监控

```bash
# 启动调度器
python3 daily_scheduler.py

# 服务会每小时自动汇报项目进度
# 报告保存在 reports/ 目录
```

## 性能优化

### 1. 负载均衡

使用多端口部署，提高并发能力：

```bash
# 启动多个代理服务实例
python3 proxy_server_v2.py --port 8080 &
python3 proxy_server_v2.py --port 8081 &
python3 proxy_server_v2.py --port 8082 &

# 使用 Nginx 进行负载均衡
```

### 2. 缓存优化

缓存常用的请求和响应：

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_request(prompt, model):
    # 检查缓存
    # 如果命中，直接返回
    # 否则，调用 API
    return result
```

### 3. 异步处理

使用异步编程提高并发性能：

```python
import asyncio

async def async_request(prompt, model):
    # 异步调用 API
    return result
```

## 成本对比

### 使用智谱 AI vs Claude API

| 对比项 | Claude API | 智谱 AI |
|--------|-----------|---------|
| 价格 | $0.15/1000 tokens | ¥0.05/1000 tokens |
| 性能 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 中文能力 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 支付方式 | 信用卡 | 支付宝/微信 |
| 文档 | 英文 | **中文** |
| 开发友好 | 一般 | **非常友好** |

**结论：** 智谱 AI 性价比更高，特别是面向中文用户！

## 常见问题

### 1. 端口被占用怎么办？

```bash
# 查看端口占用
netstat -tuln | grep 8080

# 杀死占用端口的进程
kill $(lsof -t -i:8080 | awk '{print $2}')

# 或者修改端口号
python3 proxy_server_v2.py --port 8085
```

### 2. API Key 失效怎么办？

```bash
# 检查 API Key 是否有效
curl https://open.bigmodel.cn/api/paas/v4/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY"

# 如果失败，重新获取 API Key
```

### 3. 如何部署到服务器？

```bash
# 使用 Docker 部署（推荐）
docker build -t ai-toolkit .
docker run -d -p 8080:8080 ai-toolkit

# 或者使用 Systemd 服务
# 参考项目文档
```

## 项目地址

**GitHub 仓库：** https://github.com/huangsir1983/6666
**项目文档：** https://github.com/huangsir1983/6666/blob/main/README.md
**Issues：** https://github.com/huangsir1983/6666/issues

## 总结

通过 AI 工具箱，你只需要 5 分钟就可以搭建自己的 AI API 服务，使用智谱 AI GLM-4.7 模型，而且完全开源免费！

优势：
- ⚡ **快速搭建** - 5 分钟完成
- 💰 **成本更低** - 智谱 AI 比 Claude 便宜
- 🇨🇳 **中文优化** - 专门优化中文能力
- 🛠️ **开源免费** - 完全开源，可以自由修改
- 📚 **中文文档** - 详细的中文文档和示例

开始使用吧！让我们一起用 AI 创造更多可能性！

---

**作者：** AI 工具箱团队
**项目地址：** https://github.com/huangsir1983/6666
**版本：** v1.0.0
