# 🎹 GOOGLE_SEARCH - Google 搜索速查表

**最后更新：** 2026-02-02 21:15（北京时间）
**会话ID：** session-20260202-0655
**目的：** 快速查找 Google 搜索的命令、代码片段和最佳实践

---

## 🕸️ Google 搜索速查表

### Selenium 自动化

**安装 Selenium**
```bash
pip install selenium
pip install webdriver-manager
```

**安装 ChromeDriver（自动）**
```python
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.google.com")
```

**搜索 Google**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.google.com")

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Python LangChain 教程")
search_box.send_keys(Keys.RETURN)
```

**提取搜索结果**
```python
from selenium.webdriver.common.by import By

results = driver.find_elements(By.CSS_SELECTOR, "div.g")
for i, result in enumerate(results[:10]):
    title = result.find_element(By.CSS_SELECTOR, "h3").text
    link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    print(f"{i + 1}. {title}")
    print(f"   链接：{link}")
```

---

### Serper.dev API

**安装 Serper.dev SDK**
```bash
pip install google-search-results
# 或者直接使用 requests
```

**搜索 Google**
```python
import requests
import json

api_key = "YOUR_SERPER_API_KEY"

url = "https://google.serper.dev/search"
params = {
    "q": "Python LangChain 教程",
    "num": 10
}

headers = {
    "X-API-KEY": api_key
}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    # 提取搜索结果
    results = []
    for item in data.get("organic", [])[:10]:
        results.append({
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", "")
        })
    
    print(f"找到 {len(results)} 个搜索结果")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   链接：{result['link']}")
        print(f"   摘要：{result['snippet'][:100]}...")
```

---

### Tavily Search API

**安装 Tavily SDK**
```bash
pip install tavily-python
```

**搜索 Google**
```python
from tavily import TavilyClient

api_key = "YOUR_TAVILY_API_KEY"
client = TavilyClient(api_key=api_key)

response = client.search(query="Python LangChain 教程", max_results=10)

print(f"找到 {len(response['results'])} 个搜索结果")
for i, result in enumerate(response['results'][:10], 1):
    print(f"{i}. {result['title']}")
    print(f"   链接：{result['url']}")
    print(f"   摘要：{result['content'][:100]}...")
```

**高级搜索选项**
```python
from tavily import TavilyClient

api_key = "YOUR_TAVILY_API_KEY"
client = TavilyClient(api_key=api_key)

response = client.search(
    query="Python LangChain 教程",
    max_results=10,
    search_depth="basic",
    include_answer_content=False,
    include_domains=["github.com", "juejin.cn"]
)
```

---

## 🎯 使用技巧

### 高级搜索语法

**精确搜索（双引号）**
```
"Python LangChain 教程"
```

**排除关键词（减号）**
```
Python LangChain 教程 -Java
```

**搜索特定网站（site:）**
```
site:github.com "Python LangChain"
```

**搜索多个关键词（OR）**
```
Python OR Golang "LangChain"
```

---

## 📊 三种方式对比

| 特性 | Selenium | Serper.dev | Tavily |
|------|----------|-----------|--------|
| **速度** | 慢（3-5 秒） | 快（100-300ms） | 快（100-300ms） |
| **资源占用** | 高（浏览器） | 低（HTTP 请求） | 低（HTTP 请求） |
| **数据质量** | 中（原始 HTML） | 高（结构化 JSON） | 高（结构化 JSON） |
| **适用场景** | 可视化、低频搜索 | 高频搜索、AI Agent | 高频搜索、AI 优化 |

---

## 🚀 快速开始

### 立即搜索

**使用 Serper.dev（推荐）**
```python
import requests

api_key = "YOUR_SERPER_API_KEY"
query = "Python LangChain 教程"

url = "https://google.serper.dev/search"
params = {"q": query, "num": 10}
headers = {"X-API-KEY": api_key}

response = requests.get(url, params=params, headers=headers)
data = response.json()

for item in data.get("organic", [])[:10]:
    print(item['title'])
    print(item['link'])
```

**使用 Tavily（AI 优化）**
```python
from tavily import TavilyClient

api_key = "YOUR_TAVILY_API_KEY"
client = TavilyClient(api_key=api_key)

response = client.search(query="Python LangChain 教程")

for item in response['results'][:10]:
    print(item['title'])
    print(item['url'])
```

---

## 💡 最佳实践

### 选择合适的方式

**高频搜索 / AI Agent：** Serper.dev 或 Tavily
**可视化 / 低频搜索：** Selenium
**快速原型：** Serper.dev

### 尊重 API 限制

- 不要超过 API 的免费额度
- 不要滥用搜索功能
- 不要用搜索功能进行恶意爬虫

---

## 📝 备注

### 重要提醒

1. **遵守 Google 的搜索条款** - 不要过度搜索
2. **尊重 API 限制** - 不要超过免费额度
3. **不要滥用搜索** - 不要用搜索功能进行恶意爬虫

---

**最后更新：** 2026-02-02 21:15（北京时间）
**会话ID：** session-20260202-0655
**当前版本：** v1.0
**下一版本：** v1.1（目标：完成 Day 0：Google 搜索能力）
