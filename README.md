# 🚀 AI 工具箱 - 智谱 API 服务平台

<div align="center">

![AI Toolkit](https://img.shields.io/badge/AI-Toolkit-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.7+-yellow)
![Flask](https://img.shields.io/badge/flask-2.0+-red)

**完整的 AI API 服务解决方案**

[立即体验](#快速开始) • [功能特性](#功能特性) • [API 文档](#api-文档) • [贡献指南](#贡献指南)

</div>

---

## 📖 项目简介

AI 工具箱是一个完整的 AI API 服务解决方案，提供：

- **Claude Code 代理服务** - 将 Anthropic API 转换为智谱 AI 格式
- **用户认证系统** - API Key 管理和用量统计
- **完整的应用套件** - 聊天、故事生成、代码生成等
- **自动化监控** - 服务状态自动汇报

**核心价值：** 让开发者可以无缝使用智谱 AI 的强大能力，同时兼容 Claude Code 等工具。

---

## ✨ 功能特性

### 🔌 API 服务

- ✅ Claude Code 完美兼容
- ✅ 智谱 AI GLM-4.7 模型支持
- ✅ 系统提示词支持
- ✅ 流式响应支持
- ✅ 完整的错误处理

### 👤 用户系统

- ✅ 用户注册/登录
- ✅ API Key 管理
- ✅ 用量统计
- ✅ 套餐升级
- ✅ 使用历史查询

### 🛠️ 应用工具

- ✅ 智能聊天助手
- ✅ AI 故事生成器
- ✅ 代码生成器
- ✅ 冷知识卡片
- ✅ 排序可视化

### 📊 监控系统

- ✅ 服务状态监控
- ✅ 自动健康检查
- ✅ 定时任务调度
- ✅ 日志记录

---

## 🚀 快速开始

### 环境要求

- Python 3.7+
- Flask 2.0+
- requests 库

### 安装依赖

```bash
pip install flask requests
```

### 启动服务

#### 1. 启动代理服务器

```bash
python3 proxy_server_v2.py
```

服务将在 `http://localhost:8080` 启动

#### 2. 启动认证系统

```bash
python3 auth_system.py
```

服务将在 `http://localhost:8082` 启动

#### 3. 启动 HTTP 文件服务器

```bash
python3 -m http.server 8081
```

服务将在 `http://localhost:8081` 启动

#### 4. 启动自动调度器（可选）

```bash
python3 scheduler.py
```

### 注册用户

```bash
curl -X POST http://localhost:8082/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "password123",
    "name": "Your Name"
  }'
```

返回示例：
```json
{
  "message": "注册成功",
  "user_id": "uuid",
  "api_key": "your-api-key",
  "plan": "free"
}
```

---

## 📚 API 文档

### 1. 消息发送接口

**端点：** `POST /v1/messages`

**请求头：**
```
Content-Type: application/json
X-API-Key: YOUR_API_KEY
```

**请求体：**
```json
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 200,
  "messages": [
    {
      "role": "user",
      "content": "你好"
    }
  ]
}
```

**响应：**
```json
{
  "id": "msg-123",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "你好！有什么可以帮助你的吗？"
    }
  ],
  "model": "claude-sonnet-4-5-20250929",
  "stop_reason": "end_turn"
}
```

### 2. 用户认证接口

#### 注册
**端点：** `POST /auth/register`

#### 登录
**端点：** `POST /auth/login`

#### 获取用量
**端点：** `GET /auth/usage`

#### 升级套餐
**端点：** `POST /auth/upgrade`

### 3. 健康检查

**代理服务：** `GET /health`
**认证服务：** `GET /auth/health`

---

## 💰 定价方案

| 套餐 | 价格 | 日调用 | 月调用 | 特性 |
|------|------|--------|--------|------|
| 免费版 | ¥0 | 100 | 1,000 | 基础功能 |
| 基础版 | ¥99/月 | 500 | 10,000 | 优先响应 |
| 专业版 | ¥299/月 | 2,000 | 100,000 | 专属支持 |
| 企业版 | ¥999/月 | 无限制 | 无限制 | SLA保证 |

---

## 🎯 使用场景

1. **开发集成** - 快速集成 AI 能力到应用中
2. **内容创作** - 自动生成文章、故事、代码
3. **智能客服** - 构建 AI 聊天机器人
4. **数据分析** - AI 辅助数据分析和报告
5. **教育学习** - AI 辅助学习和答疑

---

## 🏗️ 项目结构

```
.
├── proxy_server_v2.py    # 代理服务器
├── auth_system.py        # 认证系统
├── scheduler.py          # 自动调度器
├── index.html            # 主页
├── status.html           # 状态监控
├── glm_chat.html         # 聊天助手
├── ai_story.html         # 故事生成
├── code_generator.html   # 代码生成
├── ai_facts.html         # 冷知识
├── bubble_sort.html      # 排序可视化
├── users.json            # 用户数据库
├── *.log                 # 日志文件
└── README.md             # 本文件
```

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📝 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

---

## 📮 联系方式

- **Email:** contact@example.com
- **微信:** AI_Toolbox_Official
- **GitHub:** [@your-github](https://github.com/your-github)

---

## ⭐ Star History

如果这个项目对你有帮助，请给个 Star ⭐

---

<div align="center">

**Made with ❤️ by AI Toolkit Team**

[回到顶部](#-ai-工具箱---智谱-api-服务平台)

</div>
