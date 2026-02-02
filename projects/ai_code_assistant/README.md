# OpenClaw Code Assistant (OCA)

<div align="center">

**一个强大、灵活、价格实惠的 AI 代码助手**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-blue)](https://www.typescriptlang.org/)
[![Node.js](https://img.shields.io/badge/Node.js-22-green)](https://nodejs.org/)
[![Claude](https://img.shields.io/badge/Claude-3.5-purple)](https://www.anthropic.com/)

[English](#english) | [中文](#中文)

</div>

---

## 📖 中文

### 简介

OpenClaw Code Assistant (OCA) 是一个基于 Claude API 的 AI 代码助手，帮助开发者提高编码效率。它提供了代码生成、代码解释、代码优化、错误诊断等功能，是开发者的得力助手。

### 核心功能

- ✨ **代码生成** - 根据需求描述生成代码
- 📖 **代码解释** - 解释复杂代码的功能
- ⚡ **代码优化** - 优化代码性能和可读性
- 🔍 **错误诊断** - 诊断和修复代码错误
- 🎓 **学习助手** - 帮助学习新技术（开发中）

### 为什么选择 OCA？

| 功能 | GitHub Copilot | CodeGeeX | OCA |
|------|---------------|----------|-----|
| 代码补全 | ✅ | ✅ | ✅ |
| 代码生成 | ❌ | ❌ | ✅ |
| 代码解释 | ❌ | ❌ | ✅ |
| 代码优化 | ❌ | ❌ | ✅ |
| 错误诊断 | ❌ | ❌ | ✅ |
| 学习助手 | ❌ | ❌ | ✅（开发中）|
| 价格 | $10/月 | 免费 | $9.9/月 - $19.9/月 |
| 集成 | IDE 插件 | Web/IDE 插件 | Web/API/OpenClaw |

### 快速开始

#### 安装

```bash
# 克隆项目
git clone https://github.com/xiaozhi/ai-code-assistant.git
cd ai-code-assistant/backend

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写必要的配置
```

#### 配置

编辑 `.env` 文件：

```env
# Claude API 配置
CLAUDE_API_KEY=your_claude_api_key_here
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# 服务器配置
NODE_ENV=development
PORT=3000

# 数据库配置（可选，用于持久化）
DATABASE_URL=postgresql://username:password@localhost:5432/oca_db

# Redis 配置（可选，用于限流）
REDIS_URL=redis://localhost:6379
```

#### 运行

```bash
# 开发模式
npm run dev

# 生产模式
npm run build
npm start
```

#### 使用

**代码生成：**

```bash
curl -X POST http://localhost:3000/api/v1/code/generate \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "用 Python 实现一个冒泡排序",
    "language": "python"
  }'
```

**代码解释：**

```bash
curl -X POST http://localhost:3000/api/v1/code/explain \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"Hello World\")",
    "language": "python"
  }'
```

**代码优化：**

```bash
curl -X POST http://localhost:3000/api/v1/code/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "code": "// 你的代码",
    "language": "javascript",
    "optimizationGoals": ["性能", "可读性"]
  }'
```

**错误诊断：**

```bash
curl -X POST http://localhost:3000/api/v1/code/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "code": "// 你的代码",
    "errorMessage": "SyntaxError: Unexpected token",
    "language": "javascript"
  }'
```

### 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | $0 | 5 次/天，基础功能 |
| 基础版 | $9.9/月 | 50 次/天，全部功能 |
| 专业版 | $19.9/月 | 无限制，全部功能 + 高级特性 |

### 技术栈

- **后端：** Node.js + Express.js + TypeScript
- **AI：** Anthropic Claude API
- **数据库：** PostgreSQL + Redis
- **安全：** JWT + Helmet + Bcrypt

### 开发路线图

- [x] 代码生成
- [x] 代码解释
- [x] 代码优化
- [x] 错误诊断
- [ ] 学习助手
- [ ] 代码审查
- [ ] 项目生成
- [ ] 多语言支持
- [ ] 用户认证
- [ ] 订阅管理

### 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献。

### 许可证

[MIT License](LICENSE)

### 联系方式

- 作者：huangsir1983
- Email：huangsir1983@example.com
- GitHub：@huangsir1983

---

## English

### Introduction

OpenClaw Code Assistant (OCA) is an AI-powered code assistant based on Claude API that helps developers improve their coding efficiency. It provides features like code generation, code explanation, code optimization, and error diagnosis, making it an indispensable tool for developers.

### Core Features

- ✨ **Code Generation** - Generate code based on requirement descriptions
- 📖 **Code Explanation** - Explain complex code functionality
- ⚡ **Code Optimization** - Optimize code performance and readability
- 🔍 **Error Diagnosis** - Diagnose and fix code errors
- 🎓 **Learning Assistant** - Help learn new technologies (in development)

### Why Choose OCA?

| Feature | GitHub Copilot | CodeGeeX | OCA |
|---------|---------------|----------|-----|
| Code Completion | ✅ | ✅ | ✅ |
| Code Generation | ❌ | ❌ | ✅ |
| Code Explanation | ❌ | ❌ | ✅ |
| Code Optimization | ❌ | ❌ | ✅ |
| Error Diagnosis | ❌ | ❌ | ✅ |
| Learning Assistant | ❌ | ❌ | ✅ (in development) |
| Price | $10/month | Free | $9.9/month - $19.9/month |
| Integration | IDE Plugin | Web/IDE Plugin | Web/API/OpenClaw |

### Quick Start

#### Installation

```bash
# Clone the project
git clone https://github.com/huangsir1983/ai-code-assistant.git
cd ai-code-assistant/backend

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env
# Edit .env file and fill in necessary configurations
```

#### Configuration

Edit `.env` file:

```env
# Claude API Configuration
CLAUDE_API_KEY=your_claude_api_key_here
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# Server Configuration
NODE_ENV=development
PORT=3000

# Database Configuration (optional, for persistence)
DATABASE_URL=postgresql://username:password@localhost:5432/oca_db

# Redis Configuration (optional, for rate limiting)
REDIS_URL=redis://localhost:6379
```

#### Running

```bash
# Development mode
npm run dev

# Production mode
npm run build
npm start
```

#### Usage

**Code Generation:**

```bash
curl -X POST http://localhost:3000/api/v1/code/generate \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "Implement bubble sort in Python",
    "language": "python"
  }'
```

**Code Explanation:**

```bash
curl -X POST http://localhost:3000/api/v1/code/explain \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"Hello World\")",
    "language": "python"
  }'
```

**Code Optimization:**

```bash
curl -X POST http://localhost:3000/api/v1/code/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "code": "// your code",
    "language": "javascript",
    "optimizationGoals": ["performance", "readability"]
  }'
```

**Error Diagnosis:**

```bash
curl -X POST http://localhost:3000/api/v1/code/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "code": "// your code",
    "errorMessage": "SyntaxError: Unexpected token",
    "language": "javascript"
  }'
```

### Pricing

| Plan | Price | Features |
|-------|-------|----------|
| Free | $0 | 5 requests/day, basic features |
| Basic | $9.9/month | 50 requests/day, all features |
| Pro | $19.9/month | Unlimited, all features + advanced |

### Tech Stack

- **Backend:** Node.js + Express.js + TypeScript
- **AI:** Anthropic Claude API
- **Database:** PostgreSQL + Redis
- **Security:** JWT + Helmet + Bcrypt

### Roadmap

- [x] Code generation
- [x] Code explanation
- [x] Code optimization
- [x] Error diagnosis
- [ ] Learning assistant
- [ ] Code review
- [ ] Project generation
- [ ] Multi-language support
- [ ] User authentication
- [ ] Subscription management

### Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

### License

[MIT License](LICENSE)

### Contact

- Author: huangsir1983
- Email: huangsir1983@example.com
- GitHub: @huangsir1983

---

<div align="center">

**⭐ If you like this project, please give it a star! ⭐**

Made with ❤️ by 小智

</div>
