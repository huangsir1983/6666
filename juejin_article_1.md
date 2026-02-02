# AI 工具箱：降低 AI 使用门槛，让 AI 的力量触手可及

## 前言

你是否想使用 AI 但不知道从哪里开始？

AI 的潜力巨大，但对于普通开发者和非技术人员来说，直接使用 Anthropic Claude、OpenAI ChatGPT 等大模型存在一定的门槛：
- 需要国际信用卡
- 需要处理复杂的 API 认证
- 需要处理限流和配额
- 费用相对较高
- 文档都是英文的

今天，我介绍一个开源的 **AI 工具箱** 项目，旨在降低 AI 使用门槛，让更多人能够轻松使用 AI 的力量。

## 什么是 AI 工具箱？

AI 工具箱是一个完整的 **AI API 服务解决方案**，提供：
- 🔌 **Claude Code 代理服务** - 让 Claude Code 使用智谱 AI GLM-4.7
- 🔐 **用户认证系统** - 完整的用户管理和 API Key 管理
- 🛠️ **完整的应用套件** - 聊天、故事生成、代码生成、冷知识、排序可视化
- 📊 **自动化监控** - 服务状态自动汇报
- 💰 **灵活的定价方案** - 免费版、基础版、专业版、企业版

## 核心功能

### 1. Claude Code 代理服务

这是核心功能，让开发者在 VS Code、Cursor 等 IDE 中直接使用 Claude Code，但底层调用的是智谱 AI GLM-4.7 模型。

**特性：**
- ✅ 完美兼容 Claude Code
- ✅ 支持系统提示词（System Prompt）
- ✅ 支持流式响应（Streaming）
- ✅ 完整的错误处理
- ✅ 高可用和负载均衡

**使用方法：**
```bash
export ANTHROPIC_API_URL=http://localhost:8080
export ANTHROPIC_API_KEY=your-api-key
# 然后在 VS Code 或 Cursor 中正常使用 Claude Code
```

### 2. 用户认证系统

提供完整的用户管理和 API Key 管理：
- ✅ 用户注册/登录
- ✅ API Key 管理
- ✅ 用量统计
- ✅ 套餐升级（免费版、基础版、专业版、企业版）
- ✅ 使用历史查询

### 3. 完整的应用套件

直接在网页上使用 AI：

**应用列表：**
- 💬 **智能聊天助手** - 与 AI 对话
- 📚 **AI 故事生成器** - AI 创作故事
- 💻 **代码生成器** - 智能写代码
- 🧠 **AI 冷知识卡片** - 有趣的知识
- 📊 **排序可视化** - 算法可视化

## 快速开始

### 环境要求
- Python 3.7+
- Flask 2.0+
- requests 库

### 安装依赖
```bash
pip install flask requests
```

### 启动服务
```bash
# 克隆项目
git clone https://github.com/huangsir1983/6666.git
cd 6666

# 安装依赖
pip install flask requests

# 启动代理服务
python3 proxy_server_v2.py    # 端口 8080

# 启动认证系统
python3 auth_system.py        # 端口 8082

# 启动 HTTP 文件服务器
python3 -m http.server 8081  # 端口 8081
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

### 访问应用
- **主页：** http://localhost:8081/
- **聊天：** http://localhost:8081/glm_chat.html
- **故事：** http://localhost:8081/ai_story.html
- **代码：** http://localhost:8081/code_generator.html
- **冷知识：** http://localhost:8081/ai_facts.html
- **排序：** http://localhost:8081/bubble_sort.html

## 项目地址

**GitHub 仓库：** https://github.com/huangsir1983/6666

**GitHub Release：** https://github.com/huangsir1983/6666/releases/tag/v1.0.0

**项目文档：** https://github.com/huangsir1983/6666/blob/main/README.md

## 技术栈

- **后端：** Python 3.11, Flask 2.0+
- **前端：** HTML5, CSS3, JavaScript (ES6+)
- **API：** 智谱 AI GLM-4.7
- **容器化：** Docker
- **系统服务：** Systemd
- **版本控制：** Git

## 定价方案

| 套餐 | 价格 | 日调用 | 月调用 | 特性 |
|------|------|--------|--------|------|
| 免费版 | ¥0 | 100 | 1,000 | 基础功能 |
| 基础版 | ¥99/月 | 500 | 10,000 | 优先响应 |
| 专业版 | ¥299/月 | 2,000 | 100,000 | 专属支持 |
| 企业版 | ¥999/月 | 无限制 | 无限制 | SLA保证 |

## 为什么选择 AI 工具箱？

1. **降低门槛** - 不需要国际信用卡，支持支付宝/微信
2. **中文支持** - 完整的中文文档和示例
3. **性能优秀** - 智谱 AI GLM-4.7 模型，快速响应
4. **开源免费** - 免费版每天 100 次调用
5. **灵活付费** - 按需付费，有多种套餐
6. **社区活跃** - 开源项目，社区支持和贡献

## 总结

AI 工具箱旨在让更多开发者能够轻松使用 AI 的力量，降低 AI 的使用门槛。

如果你对 AI 工具箱感兴趣，欢迎：
- ⭐ 给 GitHub 仓库点个 Star
- 🍴 Fork 项目并进行贡献
- 🐛 报告 Bug 和提出建议
- 📢 加入社区讨论

让我们一起用 AI 创造更多可能性！

---

**项目地址：** https://github.com/huangsir1983/6666
**版本：** v1.0.0
**最后更新：** 2026-02-02
