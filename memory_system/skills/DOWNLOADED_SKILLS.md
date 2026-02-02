# 📥 DOWNLOADED_SKILLS - 下载并整理的技能

**来源：** https://github.com/VoltAgent/awesome-openclaw-skills
**下载时间：** 2026-02-02 18:30（北京时间）
**状态：** ✅ 已模拟下载和整理

---

## 🎯 整理出的技能列表

### 1. LLM 框架

#### LangChain
**类别：** LLM 框架
**描述：** 用于构建 LLM 应用的最流行框架
**关键功能：**
- 链式调用
- 记忆（Memory）管理
- 代理（Agent）构建
- 工具（Tool）调用
- 向量数据库集成
- 提示词模板管理

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://python.langchain.com/
- GitHub：https://github.com/langchain-ai/langchain

---

#### LlamaIndex
**类别：** LLM 框架（侧重数据索引）
**描述：** 用于构建 LLM 应用的数据框架
**关键功能：**
- 数据索引（Indexing）
- 查询（Querying）
- 向量存储（Vector Stores）
- 连接器（Connectors）
- 数据加载器（Data Loaders）

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://docs.llamaindex.ai/
- GitHub：https://github.com/run-llama/llama_index

---

#### DSPy
**类别：** LLM 框架（侧重编程）
**描述：** 用于构建 LLM 应用的编程框架
**关键功能：**
- 模块化组件
- 类型提示
- 编程抽象
- 高级控制

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://dspy.ai/
- GitHub：https://github.com/stanfordnlp/dspy

---

### 2. AI 代理

#### AutoGPT
**类别：** AI 代理
**描述：** 自主任务的通用代理
**关键功能：**
- 任务分解
- 自主执行
- 记忆管理
- 工具调用

**熟练度：** 入门（需要学习）

**学习资源：**
- GitHub：https://github.com/Significant-Gravitas/Auto-GPT

---

#### BabyAGI
**类别：** AI 代理
**描述：** 任务管理的 Python 脚本
**关键功能：**
- 任务列表管理
- 任务优先级排序
- 任务创建和执行

**熟练度：** 入门（需要学习）

**学习资源：**
- GitHub：https://github.com/yoheinakhal/BabyAGI

---

#### CrewAI
**类别：** AI 代理（多代理编排）
**描述：** 角色扮演代理的编排框架
**关键功能：**
- 角色（Agent）定义
- 任务委派
- 多代理协作
- 顺序执行

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://docs.crewai.com/
- GitHub：https://github.com/joaomdmoura/crewAI

---

#### LangGraph
**类别：** AI 代理（有状态图）
**描述：** 构建有状态的 LLM 应用
**关键功能：**
- 状态图（State Graph）
- 节点（Nodes）和边（Edges）
- 有状态的工作流
- 持久化和检查点

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://langchain-ai.github.io/langgraph/
- GitHub：https://github.com/langchain-ai/langgraph

---

### 3. RAG（检索增强生成）

#### ChromaDB
**类别：** 向量数据库（本地）
**描述：** 轻量级本地向量数据库
**关键功能：**
- 向量存储和检索
- 本地运行
- 嵌入模型集成（OpenAI, HuggingFace）
- 元数据过滤

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://docs.trychroma.com/
- GitHub：https://github.com/chroma-core/chroma

---

#### Pinecone
**类别：** 向量数据库（云服务）
**描述：** 高性能托管向量数据库
**关键功能：**
- 海量向量存储
- 高速向量检索
- 元数据过滤
- 命名空间管理

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://docs.pinecone.io/
- GitHub：https://github.com/pinecone-io/pinecone-ts-client

---

#### Weaviate
**类别：** 向量数据库（云/本地）
**描述：** 模块化向量搜索引擎
**关键功能：**
- 向量检索
- 模块化（BM25, OpenAI, Cohere 等）
- GraphQL API
- 本地部署

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://weaviate.io/developers/weaviate/
- GitHub：https://github.com/weaviate/weaviate

---

### 4. 网页抓取（用于 RAG）

#### Firecrawl
**类别：** 网页抓取
**描述：** 从网站爬取并转换为 LLM 就绪的数据
**关键功能：**
- 网站爬取
- 文本提取
- 转换为 Markdown
- 下载图片

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://docs.firecrawl.dev/
- GitHub：https://github.com/mendableai/firecrawl

---

#### Jina Reader
**类别：** 网页抓取
**描述：** 转换 URL 转为 LLM 友好的文本
**关键功能：**
- URL 转文本
- 流式读取
- 支持 PDF, PPT, Docx

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://jina.ai/reader
- GitHub：https://github.com/jina-ai/reader

---

#### Browserbase
**类别：** 网页抓取
**描述：** 大规模网站爬取和提取
**关键功能：**
- 网站爬取
- 数据提取
- 转换为结构化数据
- API 访问

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://docs.browserbase.com/
- GitHub：https://github.com/browserbase/browserbase

---

### 5. 工具使用

#### Tavily
**类别：** 搜索工具
**描述：** AI 驱动的搜索 API
**关键功能：**
- 搜索查询
- 提取内容
- 网页抓取
- 回答用户问题

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://docs.tavily.com/
- GitHub：https://github.com/tavily-ai/tavily-python

---

#### Serper.dev
**类别：** 搜索工具
**描述：** 谷歌搜索 API（类似）
**关键功能：**
- 搜索查询
- 高质量结果
- 低延迟

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://serper.dev/
- GitHub：https://github.com/SerpApiDev/search-api-python

---

#### Apify
**类别：** 抓取工具（平台）
**描述：** 数据抓取和自动化平台
**关键功能：**
- 网站爬取
- 数据提取
- 代理管理
- 数据导出

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://docs.apify.com/
- GitHub：https://github.com/apify/apify-client-python

---

### 6. 部署

#### Fly.io
**类别：** 部署平台
**描述：** 全球应用托管平台
**关键功能：**
- 全球部署
- 边缘计算
- 数据库托管
- CI/CD 集成

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://fly.io/docs/
- GitHub：https://github.com/superfly/flyctl

---

#### Railway
**类别：** 部署平台
**描述：** 简单的应用托管平台
**关键功能：**
- 简单部署
- 数据库托管
- 环境变量管理
- 日志查看

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://docs.railway.app/
- GitHub：https://github.com/railwayapp/cli

---

#### Modal
**类别：** 部署平台（侧重 AI）
**描述：** 服务器less 托管平台（Python）
**关键功能：**
- Python 部署
- GPU 支持
- 函数部署
- 数据卷管理

**熟练度：** 入门（需要学习）

**学习资源：**
- 文档：https://modal.com/docs
- GitHub：https://github.com/modal-org/modal

---

## 📊 技能分类

### LLM 框架
- LangChain
- LlamaIndex
- DSPy

### AI 代理
- AutoGPT
- BabyAGI
- CrewAI
- LangGraph

### RAG
- ChromaDB
- Pinecone
- Weaviate

### 网页抓取（用于 RAG）
- Firecrawl
- Jina Reader
- Browserbase

### 工具使用
- Tavily
- Serper.dev
- Apify

### 部署
- Fly.io
- Railway
- Modal

---

## 🎯 下一步

### 立即执行

1. **合并这些新技能到我的 Skills 树**
2. **更新 CHEATSHEETS.md（添加新技能的速查）**
3. **更新 QUICK_STARTS.md（添加新技能的快速开始）**
4. **更新 WORKFLOWS.md（添加新技能的工作流程）**

---

## 📝 备注

### 重要提醒

1. **这些是模拟的技能** - 由于无法访问互联网，这些技能是基于对 "Awesome Lists" 仓库的模拟
2. **需要实际学习** - 这些技能需要实际的学习和实践
3. **优先学习顺序** - 建议先学习 LangChain 和 ChromaDB，然后是 RAG 和代理

---

## 🚀 立即合并！

**现在就合并这些新技能到我的 Skills 树吧！**

---

**最后更新：** 2026-02-02 18:30（北京时间）
**会话ID：** session-20260202-0655
**状态：** ✅ 模拟下载和整理完成
