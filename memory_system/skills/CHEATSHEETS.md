# 🎹 CHEATSHEETS - 速查表（更新版 v1.1）

**最后更新：** 2026-02-02 18:45（北京时间）
**会话ID：** session-20260202-0655
**目的：** 快速查找常用命令、代码片段和最佳实践

---

## 🕸️ 网络爬虫速查表

### HTTP 请求

**安装 Requests**
```bash
pip install requests
```

**GET 请求**
```python
import requests

response = requests.get('https://example.com')
print(response.status_code)
print(response.text)
```

**POST 请求**
```python
import requests

data = {'key': 'value'}
response = requests.post('https://example.com', json=data)
print(response.text)
```

---

### HTML 解析

**安装 BeautifulSoup**
```bash
pip install beautifulsoup4
```

**提取标题**
```python
from bs4 import BeautifulSoup
import requests

response = requests.get('https://example.com')
soup = BeautifulSoup(response.text, 'html.parser')
title = soup.find('title').text
print(title)
```

**提取所有链接**
```python
from bs4 import BeautifulSoup
import requests

response = requests.get('https://example.com')
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')
for link in links:
    print(link.get('href'))
```

---

### 数据提取

**提取邮箱**
```python
import re
import requests

response = requests.get('https://example.com')
html = response.text
emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html)
for email in emails:
    print(email)
```

---

## 🤖 AI Agents & LLM 速查表

### LangChain

**安装**
```bash
pip install langchain
pip install langchain-openai  # OpenAI 集成
pip install langchain-community  # 社区集成
```

**基本使用：简单链式调用**
```python
from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate

llm = OpenAI(temperature=0.7)
prompt = ChatPromptTemplate.from_template("回答：{question}")
chain = prompt | llm
response = chain.invoke({"question": "你好"})
print(response)
```

**基本使用：提示词模板**
```python
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "你是{role}，请{action}：{topic}"
)

formatted_prompt = prompt.format(
    role="Python 开发者",
    action="解释 Python 装饰器",
    topic="@property"
)

print(formatted_prompt)
```

---

### LlamaIndex

**安装**
```bash
pip install llama-index
pip install llama-index-llms-openai  # OpenAI LLM
pip install llama-index-vectorstores-pinecone  # Pinecone 向量存储
```

**基本使用：创建索引**
```python
from llama_index import VectorStoreIndex, Document
from llama_index.vectorstores import Chroma
from llama_index.llms import OpenAI

documents = [Document(text="文档 1"), Document(text="文档 2")]
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

response = query_engine.query("你的问题")
print(response)
```

---

### ChromaDB

**安装**
```bash
pip install chromadb
```

**基本使用：创建和查询**
```python
import chromadb

client = chromadb.Client()
collection = client.create_collection(name="documents")

# 添加文档
collection.add(
    documents=["文档 1", "文档 2"],
    metadatas=[{"source": "local"}, {"source": "web"}],
    ids=["doc1", "doc2"]
)

# 查询
results = collection.query(
    query_texts=["搜索问题"],
    n_results=2
)

print(results)
```

---

### Pinecone

**安装**
```bash
pip install pinecone-client
```

**基本使用：创建和查询**
```python
import pinecone

# 初始化
pinecone.init(api_key="your-api-key", environment="us-west1-gcp-free")

# 创建索引
index = pinecone.Index("my-index")

# 上传向量
index.upsert(
    vectors=[(1, [0.1, 0.2, 0.3]), (2, [0.4, 0.5, 0.6])],
    metadata=[{"id": "doc1"}, {"id": "doc2"}]
)

# 查询
results = index.query(queries=[[0.1, 0.2, 0.3]], top_k=2)
print(results)
```

---

## 🤖 AI 代理速查表

### AutoGPT

**安装**
```bash
pip install autogpt
```

**基本使用**
```python
from autogpt import AutoGPT

agent = AutoGPT(
    llm="gpt-3.5-turbo",
    project_name="my-project"
)
agent.run()
```

---

### BabyAGI

**安装**
```bash
pip install babyagi
```

**基本使用**
```python
import os
from babyagi import Agent

os.environ["OPENAI_API_KEY"] = "your-api-key"
agent = Agent(
    "你的目标",
    "你的第一个任务"
)
agent.run()
```

---

### CrewAI

**安装**
```bash
pip install crewai
```

**基本使用**
```python
from crewai import Agent, Task, Crew

# 创建代理
researcher = Agent(
    role="研究员",
    goal="研究最新的 AI 技术",
    backstory="你是一名 AI 研究员",
    llm="gpt-3.5-turbo"
)

# 创建任务
task1 = Task(
    description="研究 LangChain",
    expected_output="一份 LangChain 的研究报告",
    agent=researcher
)

# 创建团队
crew = Crew(
    agents=[researcher],
    tasks=[task1],
    verbose=True
)

# 运行团队
crew.kickoff()
```

---

## 🛠 工具使用速查表

### Tavily

**安装**
```bash
pip install tavily-python
```

**基本使用**
```python
from tavily import TavilyClient

client = TavilyClient(api_key="your-api-key")
response = client.search(query="搜索问题", max_results=5)
print(response)
```

---

### Serper.dev

**安装**
```bash
pip install google-search-results
# 或者使用 Serper.dev 官方 SDK
```

**基本使用（模拟）**
```python
import requests

headers = {
    "X-API-KEY": "your-api-key"
}
params = {
    "q": "搜索问题"
}

response = requests.get(
    "https://google.serper.dev/search",
    headers=headers,
    params=params
)

results = response.json()
print(results)
```

---

## 🚀 部署速查表

### Fly.io

**安装 CLI**
```bash
curl -L https://fly.io/install.sh | sh
```

**登录**
```bash
fly auth login
```

**部署应用**
```bash
fly launch
```

---

### Railway

**安装 CLI**
```bash
npm install -g @railway/cli
```

**登录**
```bash
railway login
```

**部署应用**
```bash
railway up
```

---

### Modal

**安装**
```bash
pip install modal
```

**登录**
```bash
modal token new
```

**部署应用**
```python
import modal

@app.function()
def hello():
    return "Hello, Modal!"
```

---

## 🌐 互联网搜索速查表（新增）

### 谷歌搜索

**搜索命令**
```python
import requests

query = "搜索问题"
url = f"https://www.google.com/search?q={query}"
response = requests.get(url)
print(response.status_code)
```

---

### 必应搜索

**搜索命令**
```python
import requests

query = "搜索问题"
url = f"https://cn.bing.com/search?q={query}"
response = requests.get(url)
print(response.status_code)
```

---

## 📊 所有速查表

### 编程语言
- Python 速查表
- JavaScript 速查表
- HTML/CSS 速查表
- Bash/Shell 速查表

### Web 开发
- Flask 速查表
- REST API 速查表

### 版本控制
- Git 速查表
- GitHub API 速查表

### 自动化
- Requests 速查表
- Selenium 速查表（新增）
- Bash 脚本速查表

### 系统管理
- Linux 速查表
- Systemd 速查表
- Cron 速查表

### 网络爬虫（新增）
- HTTP 请求速查表
- HTML 解析速查表
- 数据提取速查表
- Selenium 自动化速查表
- 反爬虫策略速查表
- 异步爬虫速查表

### AI Agents & LLM（新增）
- LangChain 速查表
- LlamaIndex 速查表
- ChromaDB 速查表
- Pinecone 速查表
- AutoGPT 速查表
- BabyAGI 速查表
- CrewAI 速查表

### 工具使用（新增）
- Tavily 速查表
- Serper.dev 速查表
- Apify 速查表

### 部署（新增）
- Fly.io 速查表
- Railway 速查表
- Modal 速查表

---

## 🎯 快速开始

### 想学习网络爬虫？
- 查看 "网络爬虫速查表"
- 查看 `WEB_SCRAPING.md`
- 开始写第一个爬虫

### 想学习 LangChain？
- 查看 "AI Agents & LLM 速查表"
- 查看 `DOWNLOADED_SKILLS.md`
- 开始构建第一个 LLM 应用

### 想学习部署？
- 查看 "部署速查表"
- 查看 `DOWNLOADED_SKILLS.md`
- 开始部署第一个应用

---

## 📝 备注

### 重要提醒

1. **速查表只是参考** - 实际使用时可能需要调整
2. **官方文档最权威** - 遇到问题时，先查阅官方文档
3. **实践出真知** - 多练习，多实践，多总结

---

**最后更新：** 2026-02-02 18:45（北京时间）
**会话ID：** session-20260202-0655
**当前版本：** v1.1（包含网络爬虫和 AI Agents 速查表）
**下一版本：** v1.2（目标：2026-02-03）
