# 🕸️ GOOGLE_SEARCH - Google 搜索技能

**最后更新：** 2026-02-02 20:30（北京时间）
**会话ID：** session-20260202-0655
**目的：** 记录如何实现 Google 搜索能力（3 种方式）

---

## 🎯 Google 搜索技能

### 为什么重要？

**核心能力：**
- **获取最新信息** - 比 GitHub 或静态知识库更实时
- **AI Agent 必备** - 搜索是 AI Agent（如 AutoGPT, CrewAI）最核心的工具能力之一
- **解决未知问题** - 当遇到新问题时，第一反应是去搜索，而不是回忆

---

## 🚀 三种实现方式

### 方式 1：Selenium 自动化（模拟人类）

#### 原理
- 使用 Selenium 自动化控制浏览器
- 打开 Google 搜索页面
- 输入搜索查询
- 点击“搜索”按钮
- 解析搜索结果页面

#### 优点
- 最接近人类操作
- 可以处理 JavaScript 渲染的页面
- 可以看到搜索过程（可视化）

#### 缺点
- 速度慢（每次搜索需要 3-5 秒）
- 资源占用大（需要浏览器进程）
- 可能被 Google 反爬虫检测
- 不适合高频搜索

#### 适用场景
- 需要可视化搜索过程
- 需要处理复杂的 JavaScript 页面
- 低频搜索（每小时几次）

---

### 方式 2：Serper.dev API（工业界标准）

#### 原理
- 使用 Serper.dev 提供的 Google 搜索 API
- 发送 HTTP GET 请求
- 接收 JSON 格式的搜索结果
- 解析 JSON 并提取有用信息

#### 优点
- 速度快（每次搜索 100-300ms）
- 资源占用小（轻量级 HTTP 请求）
- 结构化数据（易于解析和使用）
- 适合高频搜索（每秒几次）

#### 缺点
- 需要付费 API（免费额度：100 次/月）
- 需要注册账号
- 可能需要等待 API 响应

#### 适用场景
- 高频搜索
- AI Agent 的搜索工具
- 需要结构化数据
- 需要快速响应

---

### 方式 3：Tavily Search API（AI 专用，推荐）

#### 原理
- 使用 Tavily 提供的搜索和抓取 API
- 发送 HTTP POST 请求
- 接收 JSON 格式的搜索结果
- 支持搜索和抓取（Search & Scrape）

#### 优点
- 速度快（每次搜索 100-300ms）
- 支持搜索和抓取
- 支持高级搜索选项
- AI 优化（专为 AI 设计）

#### 缺点
- 需要付费 API（免费额度：1000 次/月）
- 需要注册账号
- 功能可能过于复杂

#### 适用场景
- AI Agent 的搜索工具
- 需要搜索和抓取
- 需要高级搜索选项
- 需要快速响应

---

## 📋 学习计划

### Day 0：Google 搜索能力（8 小时）

#### 上午（4 小时）

**方式 1：Selenium 自动化（2 小时）**
- [ ] 安装 Selenium 和 ChromeDriver
- [ ] 创建一个简单的 Selenium Google 搜索脚本
- [ ] 搜索 "Python LangChain 教程"
- [ ] 提取前 10 个搜索结果

**方式 2：Serper.dev API（2 小时）**
- [ ] 注册 Serper.dev 账号
- [ ] 获取 API Key
- [ ] 创建一个简单的 Serper.dev 搜索脚本
- [ ] 搜索 "AI Agent 开发教程"
- [ ] 提取前 10 个搜索结果

#### 下午（4 小时）

**方式 3：Tavily Search API（3 小时）**
- [ ] 注册 Tavily 账号
- [ ] 获取 API Key
- [ ] 创建一个简单的 Tavily 搜索脚本
- [ ] 搜索 "LangChain 教程"
- [ ] 提取前 10 个搜索结果
- [ ] 测试搜索和抓取功能

**综合项目（1 小时）**
- [ ] 比较三种方式的优缺点
- [ ] 选择最适合的方式
- [ ] 创建一个综合的 Google 搜索工具

---

## 📚 学习资源

### Selenium
- **文档：** https://www.selenium.dev/documentation/
- **GitHub：** https://github.com/SeleniumHQ/selenium

### Serper.dev
- **文档：** https://serper.dev/
- **GitHub：** https://github.com/SerpApiDev/search-api-python

### Tavily
- **文档：** https://docs.tavily.com/
- **GitHub：** https://github.com/tavily-ai/tavily-python

---

## 🎯 下一步

### 立即执行

1. **安装 Selenium**
   ```bash
   pip install selenium
   ```

2. **注册 Serper.dev 和 Tavily**
   - Serper.dev: https://serper.dev/
   - Tavily: https://tavily.com/

3. **开始学习**
   - 学习 Selenium 基础
   - 学习 Serper.dev API
   - 学习 Tavily Search API

---

## 💡 最佳实践

### 选择合适的方式

**推荐顺序：**
1. **优先使用 Serper.dev 或 Tavily** - 速度快、结构化数据、适合 AI Agent
2. **其次使用 Selenium** - 可视化、适合低频搜索
3. **最后使用 googlesearch-python** - 简单但功能受限

### 高级搜索技巧

**搜索技巧：**
- 使用双引号搜索精确短语："LangChain 教程"
- 使用减号排除不相关的关键词：Python -Java
- 使用 site: 搜索特定网站：site:github.com "LangChain"
- 使用 OR 搜索多个关键词：Python OR Golang

---

## 📊 技能评估

### 当前水平

| 技能 | 当前水平 | 目标水平 | 提升 |
|------|----------|----------|------|
| **Google 搜索 (Selenium)** | 无 | 入门 | +100% |
| **Google 搜索 (Serper.dev)** | 无 | 熟练 | +100% |
| **Google 搜索 (Tavily)** | 无 | 熟练 | +100% |

---

## 💡 最后提醒

### 重要提醒

1. **遵守 Google 的搜索条款** - 不要过度搜索，不要违反 Google 的使用条款
2. **尊重 API 限制** - 不要超过 API 的免费额度
3. **不要滥用搜索** - 不要用搜索功能进行恶意爬虫

---

**最后更新：** 2026-02-02 20:30（北京时间）
**会话ID：** session-20260202-0655
**当前版本：** v1.0
**下一版本：** v1.1（目标：掌握 3 种 Google 搜索方式）
