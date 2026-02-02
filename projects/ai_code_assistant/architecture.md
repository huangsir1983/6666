# 🏗️ AI 代码助手 - 产品架构设计

**设计时间：** 2026-02-03 14:40
**项目名称：** OpenClaw Code Assistant (OCA)
**版本：** v1.0

---

## 📐 系统架构

### 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户界面 (UI)                        │
│         Web 界面 | API 接口 | OpenClaw 集成           │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   API 层 (API Layer)                   │
│      REST API | GraphQL | WebSocket (实时通信)          │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                 业务逻辑层 (Business Layer)               │
│   代码生成 | 代码解释 | 代码优化 | 错误诊断 | 学习助手   │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   AI 引擎层 (AI Layer)                   │
│              Claude API | OpenCl Agent                  │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                   数据层 (Data Layer)                   │
│   PostgreSQL | Redis | 用户数据 | 代码缓存 | 使用日志     │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 技术栈

### 后端技术

**核心框架：**
- **Node.js** - 运行时环境
- **Express.js** - Web 框架
- **TypeScript** - 类型安全

**数据库：**
- **PostgreSQL** - 主数据库（用户、代码历史、使用记录）
- **Redis** - 缓存层（API 限制、临时数据）

**AI 集成：**
- **Anthropic Claude API** - AI 模型
- **OpenClaw** - 任务调度和多智能体

**其他：**
- **JWT** - 用户认证
- **Docker** - 容器化部署
- **Nginx** - 反向代理

### 前端技术

**核心框架：**
- **React** - UI 框架
- **TypeScript** - 类型安全
- **Vite** - 构建工具

**UI 组件：**
- **Tailwind CSS** - 样式框架
- **shadcn/ui** - UI 组件库

**其他：**
- **Axios** - HTTP 客户端
- **Monaco Editor** - 代码编辑器
- **Zustand** - 状态管理

---

## 📦 项目结构

### 后端目录结构

```
backend/
├── src/
│   ├── controllers/          # 控制器层
│   │   ├── auth.controller.ts
│   │   ├── code.controller.ts
│   │   └── user.controller.ts
│   ├── services/            # 业务逻辑层
│   │   ├── ai/
│   │   │   ├── code.generator.ts
│   │   │   ├── code.explainer.ts
│   │   │   ├── code.optimizer.ts
│   │   │   ├── error.diagnostic.ts
│   │   │   └── learning.assistant.ts
│   │   ├── auth.service.ts
│   │   ├── rate.limit.service.ts
│   │   └── user.service.ts
│   ├── models/              # 数据模型
│   │   ├── user.model.ts
│   │   ├── code.model.ts
│   │   └── usage.model.ts
│   ├── middleware/          # 中间件
│   │   ├── auth.middleware.ts
│   │   ├── error.middleware.ts
│   │   └── rate.limit.middleware.ts
│   ├── routes/              # 路由
│   │   ├── auth.routes.ts
│   │   ├── code.routes.ts
│   │   └── user.routes.ts
│   ├── utils/               # 工具函数
│   │   ├── claude.util.ts
│   │   ├── logger.util.ts
│   │   └── validator.util.ts
│   ├── config/              # 配置
│   │   ├── database.config.ts
│   │   └── claude.config.ts
│   ├── types/               # TypeScript 类型
│   │   ├── index.ts
│   │   └── api.types.ts
│   └── app.ts               # 应用入口
├── tests/                   # 测试
├── docker/                  # Docker 配置
├── package.json
├── tsconfig.json
└── docker-compose.yml
```

### 前端目录结构

```
frontend/
├── src/
│   ├── components/           # 组件
│   │   ├── ui/              # UI 组件（shadcn/ui）
│   │   ├── code-editor/     # 代码编辑器
│   │   ├── code-result/     # 代码结果展示
│   │   └── auth/           # 认证组件
│   ├── pages/               # 页面
│   │   ├── Home.tsx
│   │   ├── CodeGenerator.tsx
│   │   ├── CodeExplainer.tsx
│   │   ├── CodeOptimizer.tsx
│   │   ├── ErrorDiagnostic.tsx
│   │   ├── LearningAssistant.tsx
│   │   └── Pricing.tsx
│   ├── services/            # API 服务
│   │   ├── api.service.ts
│   │   └── auth.service.ts
│   ├── store/               # 状态管理
│   │   ├── auth.store.ts
│   │   └── code.store.ts
│   ├── types/               # TypeScript 类型
│   │   └── index.ts
│   ├── utils/               # 工具函数
│   │   └── logger.util.ts
│   ├── App.tsx
│   └── main.tsx
├── public/
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

---

## 🔄 核心功能设计

### 1. 代码生成器 (Code Generator)

**流程：**
```
用户输入需求
    ↓
验证和清理输入
    ↓
构建 AI 提示词
    ↓
调用 Claude API
    ↓
解析 AI 响应
    ↓
格式化和验证代码
    ↓
保存到数据库
    ↓
返回给用户
```

**API 设计：**
```typescript
POST /api/v1/code/generate
Request: {
  requirement: string,      // 用户需求描述
  language: string,         // 编程语言
  context?: string          // 上下文信息（可选）
}
Response: {
  id: string,
  code: string,
  explanation: string,
  language: string,
  timestamp: string
}
```

### 2. 代码解释器 (Code Explainer)

**流程：**
```
用户输入代码
    ↓
解析代码（AST）
    ↓
构建 AI 提示词
    ↓
调用 Claude API
    ↓
生成详细解释
    ↓
返回给用户
```

**API 设计：**
```typescript
POST /api/v1/code/explain
Request: {
  code: string,
  language: string
}
Response: {
  id: string,
  explanation: string,
  keyPoints: string[],
  bestPractices: string[]
}
```

### 3. 代码优化器 (Code Optimizer)

**流程：**
```
用户输入代码
    ↓
分析代码（静态分析）
    ↓
识别优化点
    ↓
构建 AI 提示词
    ↓
调用 Claude API
    ↓
生成优化后的代码
    ↓
性能对比
    ↓
返回给用户
```

**API 设计：**
```typescript
POST /api/v1/code/optimize
Request: {
  code: string,
  language: string,
  optimizationGoals: string[]  // 性能、可读性等
}
Response: {
  id: string,
  originalCode: string,
  optimizedCode: string,
  improvements: string[],
  performanceDiff: {
    timeComplexity: string,
    spaceComplexity: string
  }
}
```

### 4. 错误诊断器 (Error Diagnostic)

**流程：**
```
用户输入错误信息和代码
    ↓
解析错误
    ↓
分析代码
    ↓
构建 AI 提示词
    ↓
调用 Claude API
    ↓
生成诊断和修复方案
    ↓
返回给用户
```

**API 设计：**
```typescript
POST /api/v1/code/diagnose
Request: {
  code: string,
  errorMessage: string,
  language: string
}
Response: {
  id: string,
  errorType: string,
  errorCause: string,
  fixSuggestion: string,
  fixedCode: string,
  preventionTips: string[]
}
```

### 5. 学习助手 (Learning Assistant)

**流程：**
```
用户输入问题
    ↓
理解问题意图
    ↓
搜索相关知识库
    ↓
构建 AI 提示词
    ↓
调用 Claude API
    ↓
生成详细回答
    ↓
返回给用户
```

**API 设计：**
```typescript
POST /api/v1/learning/ask
Request: {
  question: string,
  topic?: string
}
Response: {
  id: string,
  answer: string,
  examples: string[],
  resources: string[],
  relatedTopics: string[]
}
```

---

## 🗄️ 数据库设计

### 用户表 (users)

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  subscription_tier VARCHAR(50) DEFAULT 'free',  -- free, basic, pro
  api_quota_daily INT DEFAULT 5,                 -- 每日配额
  api_quota_used INT DEFAULT 0,                  -- 已使用配额
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_subscription ON users(subscription_tier);
```

### 代码历史表 (code_history)

```sql
CREATE TABLE code_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  code_type VARCHAR(50) NOT NULL,               -- generate, explain, optimize, diagnose
  input_data JSONB NOT NULL,                      -- 输入数据
  output_data JSONB NOT NULL,                     -- 输出数据
  language VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_code_history_user ON code_history(user_id);
CREATE INDEX idx_code_history_type ON code_history(code_type);
CREATE INDEX idx_code_history_created ON code_history(created_at);
```

### 使用记录表 (usage_logs)

```sql
CREATE TABLE usage_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  endpoint VARCHAR(255) NOT NULL,
  method VARCHAR(10) NOT NULL,
  status_code INT NOT NULL,
  response_time_ms INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_usage_logs_user ON usage_logs(user_id);
CREATE INDEX idx_usage_logs_created ON usage_logs(created_at);
```

---

## 🔐 安全设计

### 认证和授权

**JWT Token：**
- Access Token：15 分钟有效
- Refresh Token：7 天有效
- Token 存储在 HttpOnly Cookie

**API 限流：**
- 免费用户：5 次/天
- 基础版用户：50 次/天
- 专业版用户：无限制
- 使用 Redis 实现

### 数据安全

**敏感数据：**
- 密码使用 bcrypt 加密
- API Key 存储在环境变量
- 用户数据加密存储

**输入验证：**
- 所有用户输入都进行验证和清理
- 使用 Joi 或 Zod 进行数据验证
- 防止 SQL 注入和 XSS 攻击

---

## 🚀 部署架构

### 开发环境

```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://...
      - CLAUDE_API_KEY=...
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app

  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=oca_db
      - POSTGRES_USER=oca_user
      - POSTGRES_PASSWORD=oca_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### 生产环境

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
    restart: always

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    restart: always
```

---

## 📊 监控和日志

### 监控指标

**应用监控：**
- API 响应时间
- API 成功率
- 数据库查询时间
- 缓存命中率
- 错误率

**业务监控：**
- 用户注册数
- 活跃用户数
- API 调用次数
- 收入

### 日志系统

**日志级别：**
- ERROR：严重错误
- WARN：警告信息
- INFO：一般信息
- DEBUG：调试信息

**日志内容：**
- 请求信息（IP、时间、路径）
- 响应信息（状态码、响应时间）
- 错误信息（错误堆栈）
- 用户行为（注册、登录、使用功能）

---

## 📝 MVP 范围

### 必须实现（MVP）

1. ✅ 用户认证（注册、登录）
2. ✅ 代码生成功能
3. ✅ 代码解释功能
4. ✅ 基础的限流（免费版 5 次/天）
5. ✅ 简单的 Web 界面

### 后续版本（v2.0）

1. 代码优化功能
2. 错误诊断功能
3. 学习助手功能
4. 付费订阅系统
5. 高级限流和配额管理

---

**文档创建时间：** 2026-02-03 14:40
**文档版本：** v1.0
**状态：** ✅ 架构设计完成

---

*"好的架构是成功的一半。设计好架构，然后开始编码。"* — 小智
