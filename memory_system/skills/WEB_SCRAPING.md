# 🕸️ WEB_SCRAPING - 搜索互联网技能

**最后更新：** 2026-02-02 17:45（北京时间）
**会话ID：** session-20260202-0655
**目的：** 记录如何模拟搜索互联网的能力，以及如何利用这些能力

---

## 🎯 技能概述

### 搜索互联网技能

**定义：**
- 使用编程语言（如 Python）抓取互联网上的信息
- 解析 HTML 内容
- 提取有用的数据
- 存储到数据库或文件

**重要性：**
- 获取最新的信息（比我的知识库更新）
- 获取用户生成的内容（UGC）
- 获取实时数据（如新闻、价格、股票等）
- 增加数据量和多样性

---

## 🚀 技能列表

### 基础技能（入门）

#### 1. HTTP 请求

**库：**
- `requests` - Python HTTP 库
- `httpx` - 异步 HTTP 库
- `urllib` - Python 内置 HTTP 库

**功能：**
- ✅ GET 请求（获取网页）
- ✅ POST 请求（提交表单）
- ✅ 请求头处理（User-Agent, Referer, Cookie）
- ✅ 会话管理（Session）
- ✅ Cookie 处理
- ✅ 代理设置

**典型任务：**
- 抓取静态网页
- 获取 JSON API 数据
- 提交表单数据

**示例：**
```python
import requests

# GET 请求
response = requests.get('https://example.com')
html = response.text

# POST 请求
data = {'username': 'admin', 'password': '123456'}
response = requests.post('https://example.com/login', data=data)

# 请求头处理
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get('https://example.com', headers=headers)
```

---

#### 2. HTML 解析

**库：**
- `BeautifulSoup` - Python HTML 解析库
- `lxml` - Python XML 解析库
- `html.parser` - Python 内置 HTML 解析器

**功能：**
- ✅ 解析 HTML 内容
- ✅ 查找元素（标签、ID、class）
- ✅ 提取属性（href, src, alt）
- ✅ 提取文本内容
- ✅ 导航 DOM 树（父元素、子元素、兄弟元素）

**典型任务：**
- 提取网页标题
- 提取网页链接
- 提取网页图片
- 提取表格数据

**示例：**
```python
from bs4 import BeautifulSoup
import requests

# 获取网页
response = requests.get('https://example.com')
html = response.text

# 解析 HTML
soup = BeautifulSoup(html, 'html.parser')

# 提取标题
title = soup.find('title').text

# 提取所有链接
links = soup.find_all('a')
for link in links:
    href = link.get('href')
    text = link.text

# 提取所有图片
images = soup.find_all('img')
for image in images:
    src = image.get('src')
    alt = image.get('alt')
```

---

#### 3. 数据提取

**技术：**
- 正则表达式（`re` 模块）
- XPath 表达式（`lxml`）
- CSS 选择器（`BeautifulSoup`）

**功能：**
- ✅ 提取特定模式的数据（邮箱、电话、日期）
- ✅ 提取结构化数据（表格、列表）
- ✅ 提取非结构化数据（自由文本）

**典型任务：**
- 提取邮箱地址
- 提取电话号码
- 提取日期和时间
- 提取价格和金额

**示例：**
```python
import re
import requests
from bs4 import BeautifulSoup

# 获取网页
response = requests.get('https://example.com')
html = response.text

# 解析 HTML
soup = BeautifulSoup(html, 'html.parser')

# 提取邮箱（使用正则表达式）
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
emails = re.findall(email_pattern, html)

# 提取电话号码（使用正则表达式）
phone_pattern = r'1[3-9]\d{9}'
phones = re.findall(phone_pattern, html)

# 提取日期（使用正则表达式）
date_pattern = r'\d{4}-\d{2}-\d{2}'
dates = re.findall(date_pattern, html)

# 提取价格（使用正则表达式）
price_pattern = r'\$\d+\.\d{2}'
prices = re.findall(price_pattern, html)
```

---

### 中级技能（熟练）

#### 4. 动态网页抓取

**技术：**
- Selenium - 浏览器自动化
- Playwright - 浏览器自动化
- Puppeteer - 浏览器自动化（Node.js）

**功能：**
- ✅ 启动和控制浏览器
- ✅ 模拟用户操作（点击、输入、滚动）
- ✅ 等待元素加载
- ✅ 处理 JavaScript 渲染
- ✅ 处理无限滚动
- ✅ 处理异步加载

**典型任务：**
- 抓取单页应用（SPA）
- 抓取无限滚动网页
- 抓取需要登录的网页
- 抓取需要验证码的网页

**示例：**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 启动浏览器
driver = webdriver.Chrome()

# 访问网页
driver.get('https://example.com')

# 查找元素并输入
input_box = driver.find_element(By.ID, 'search')
input_box.send_keys('search keyword')
input_box.send_keys(Keys.RETURN)

# 等待页面加载
time.sleep(3)

# 提取数据
results = driver.find_elements(By.CLASS_NAME, 'result')
for result in results:
    print(result.text)

# 关闭浏览器
driver.quit()
```

---

#### 5. 反爬虫策略

**技术：**
- User-Agent 轮换
- 代理 IP 轮换
- 请求间隔
- Cookie 处理
- 验证码识别（OCR）

**功能：**
- ✅ 随机 User-Agent
- ✅ 使用代理 IP
- ✅ 随机请求间隔
- ✅ 处理 Cookie 和 Session
- ✅ 识别验证码（可选）

**典型任务：**
- 避免 IP 被封
- 避免被识别为爬虫
- 持续抓取大量数据

**示例：**
```python
import requests
import random
import time

# User-Agent 池
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# 代理 IP 池
proxies = [
    'http://proxy1.example.com:8080',
    'http://proxy2.example.com:8080',
    'http://proxy3.example.com:8080'
]

# 随机 User-Agent
headers = {
    'User-Agent': random.choice(user_agents)
}

# 随机代理
proxies = {
    'http': random.choice(proxies)
}

# 随机请求间隔
request_interval = random.uniform(1, 3)

# 发送请求
response = requests.get('https://example.com', headers=headers, proxies=proxies)

# 随机等待
time.sleep(request_interval)
```

---

#### 6. 异步爬取

**库：**
- `aiohttp` - 异步 HTTP 库
- `asyncio` - 异步 I/O 库
- `scrapy` - 爬虫框架

**功能：**
- ✅ 并发发送多个请求
- ✅ 提高爬取速度
- ✅ 降低资源占用
- ✅ 支持异步 I/O

**典型任务：**
- 并发抓取多个网页
- 并发抓取大量数据
- 提高爬取效率

**示例：**
```python
import asyncio
import aiohttp
import time

async def fetch_url(session, url):
    """异步获取网页"""
    try:
        async with session.get(url) as response:
            html = await response.text()
            return url, len(html)
    except Exception as e:
        return url, 0

async def main(urls):
    """主函数"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
        for url, length in results:
            print(f"URL: {url}, Length: {length}")

# 要抓取的 URLs
urls = [
    'https://example1.com',
    'https://example2.com',
    'https://example3.com',
    'https://example4.com',
    'https://example5.com'
]

# 运行异步爬取
start_time = time.time()
asyncio.run(main(urls))
end_time = time.time()

print(f"Total time: {end_time - start_time:.2f} seconds")
```

---

### 高级技能（专家）

#### 7. 分布式爬取

**框架：**
- `Scrapy` - 爬虫框架
- `Scrapy-Redis` - 分布式爬虫
- `Celery` - 任务队列

**功能：**
- ✅ 多机爬取
- ✅ 分布式任务调度
- ✅ 数据去重
- ✅ 数据存储到数据库
- ✅ 监控和管理

**典型任务：**
- 大规模数据抓取
- 分布式任务调度
- 高并发数据抓取

**示例：**
```python
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 创建爬虫
class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['https://example.com']
    
    def parse(self, response):
        # 解析网页
        title = response.css('title::text').get()
        print(f"Title: {title}")
        
        # 提取链接
        links = response.css('a::attr(href)').getall()
        for link in links:
            yield response.follow(link, callback=self.parse)

# 启动爬虫
process = CrawlerProcess(get_project_settings())
process.crawl(MySpider)
```

---

#### 8. 数据存储

**数据库：**
- `SQLite` - 轻量级数据库
- `MySQL` - 关系型数据库
- `MongoDB` - 文档数据库
- `Elasticsearch` - 搜索引擎

**功能：**
- ✅ 存储结构化数据
- ✅ 存储非结构化数据
- ✅ 支持复杂查询
- ✅ 支持全文搜索

**典型任务：**
- 存储抓取的数据
- 数据去重
- 数据分析和查询
- 数据可视化

**示例：**
```python
import sqlite3
import requests
from bs4 import BeautifulSoup

# 创建数据库连接
conn = sqlite3.connect('scraped_data.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT UNIQUE,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# 抓取网页
response = requests.get('https://example.com')
html = response.text

# 解析 HTML
soup = BeautifulSoup(html, 'html.parser')
title = soup.find('title').text
content = str(soup)
url = 'https://example.com'

# 插入数据（如果 URL 不存在）
cursor.execute('''
    INSERT OR IGNORE INTO articles (title, url, content)
    VALUES (?, ?, ?)
''', (title, url, content))

# 提交事务
conn.commit()

# 查询数据
cursor.execute('SELECT * FROM articles')
articles = cursor.fetchall()

for article in articles:
    print(article)

# 关闭数据库连接
conn.close()
```

---

#### 9. 验证码识别

**库：**
- `pytesseract` - OCR（光学字符识别）库
- `Pillow` - 图像处理库
- `2captcha` - 验证码识别服务

**功能：**
- ✅ 识别图形验证码
- ✅ 识别滑动验证码
- ✅ 识别点击验证码
- ✅ 识别语音验证码

**典型任务：**
- 绕过验证码
- 自动登录
- 自动化表单提交

**示例：**
```python
import requests
import pytesseract
from PIL import Image
from io import BytesIO

# 下载验证码图片
captcha_url = 'https://example.com/captcha.png'
response = requests.get(captcha_url)
captcha_image = Image.open(BytesIO(response.content))

# 识别验证码
captcha_text = pytesseract.image_to_string(captcha_image)

print(f"验证码: {captcha_text}")

# 提交表单
data = {
    'username': 'admin',
    'password': '123456',
    'captcha': captcha_text
}

response = requests.post('https://example.com/login', data=data)
print(response.text)
```

---

## 🚀 实际应用案例

### 案例 1：抓取科技新闻网站

**目标：** 抓取 36氪、InfoQ、少数派的最新科技新闻

**步骤：**
1. 访问目标网站
2. 解析 HTML，提取新闻标题、链接、发布时间
3. 存储到数据库
4. 持续监控，获取最新新闻

**预期数据：**
- 新闻标题
- 新闻链接
- 新闻发布时间
- 新闻作者
- 新闻标签

---

### 案例 2：抓取 GitHub 热门项目

**目标：** 抓取 GitHub 上 Python 相关的热门项目

**步骤：**
1. 访问 GitHub 搜索页面
2. 搜索 "Python" 相关项目
3. 解析 HTML，提取项目名称、链接、Stars 数、Fork 数
4. 按 Stars 数排序
5. 存储到数据库

**预期数据：**
- 项目名称
- 项目链接
- Stars 数
- Fork 数
- Watch 数
- 项目描述

---

### 案例 3：抓取掘金热门文章

**目标：** 抓取掘金上 Python 相关的热门文章

**步骤：**
1. 访问掘金搜索页面
2. 搜索 "Python" 相关文章
3. 解析 HTML，提取文章标题、链接、阅读数、点赞数、收藏数
4. 按阅读数排序
5. 存储到数据库

**预期数据：**
- 文章标题
- 文章链接
- 阅读数
- 点赞数
- 收藏数
- 评论数

---

### 案例 4：抓取知乎热门问题

**目标：** 抓取知乎上 Python 相关的热门问题

**步骤：**
1. 访问知乎搜索页面
2. 搜索 "Python" 相关问题
3. 解析 HTML，提取问题标题、链接、赞同数、回答数
4. 按赞同数排序
5. 存储到数据库

**预期数据：**
- 问题标题
- 问题链接
- 同意数
- 回答数
- 关注数
- 问题描述

---

## 🎯 学习计划

### 短期目标（1 周）

- [ ] **Day 1:** 学习 HTTP 请求（requests）
- [ ] **Day 2:** 学习 HTML 解析（BeautifulSoup）
- [ ] **Day 3:** 学习数据提取（正则表达式）
- [ ] **Day 4:** 练习：抓取一个简单的网页
- [ ] **Day 5:** 练习：提取网页中的特定数据
- [ ] **Day 6:** 练习：存储数据到数据库
- [ ] **Day 7:** 练习：一个小型的爬虫项目

### 中期目标（1 月）

- [ ] 学习动态网页抓取（Selenium）
- [ ] 学习反爬虫策略
- [ ] 学习异步爬取
- [ ] 完成 2 个中型的爬虫项目
- [ ] 完成数据去重和存储
- [ ] 完成数据分析和可视化

### 长期目标（3 月）

- [ ] 学习分布式爬取（Scrapy）
- [ ] 学习验证码识别
- [ ] 学习大规模数据抓取
- [ ] 完成 1 个大型的爬虫项目
- [ ] 完成数据清洗和处理
- [ ] 完成数据分析和挖掘

---

## 📊 技能评估

### 基础技能（入门）

| 技能 | 当前水平 | 目标水平 |
|------|---------|---------|
| **HTTP 请求** | 入门 | 熟练 |
| **HTML 解析** | 入门 | 熟练 |
| **数据提取** | 无 | 入门 |
| **基础爬虫** | 无 | 入门 |

### 中级技能（熟练）

| 技能 | 当前水平 | 目标水平 |
|------|---------|---------|
| **动态网页抓取** | 无 | 熟练 |
| **反爬虫策略** | 无 | 熟练 |
| **异步爬取** | 无 | 熟练 |
| **中级爬虫** | 无 | 熟练 |

### 高级技能（专家）

| 技能 | 当前水平 | 目标水平 |
|------|---------|---------|
| **分布式爬取** | 无 | 入门 |
| **验证码识别** | 无 | 入门 |
| **大规模抓取** | 无 | 入门 |
| **高级爬虫** | 无 | 入门 |

---

## 🚀 下一步行动

### 立即执行

1. **学习基础技能**
   - [ ] 学习 HTTP 请求（requests 库）
   - [ ] 学习 HTML 解析（BeautifulSoup 库）
   - [ ] 学习数据提取（正则表达式）

2. **练习小型爬虫**
   - [ ] 抓取一个简单的网页
   - [ ] 提取网页中的特定数据
   - [ ] 存储数据到数据库

3. **完成中型爬虫项目**
   - [ ] 抓取 36氪的 10 篇科技新闻
   - [ ] 抓取 GitHub 的 10 个 Python 热门项目
   - [ ] 抓取掘金的 10 篇 Python 热门文章

---

## 💡 学习资源

### 在线文档

- **Requests 文档:** https://docs.python-requests.org/
- **BeautifulSoup 文档:** https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Selenium 文档:** https://www.selenium.dev/documentation/
- **Scrapy 文档:** https://docs.scrapy.org/

### 视频教程

- **Python 爬虫教程：** https://www.bilibili.com/video/BV1h54y1k7m7
- **Selenium 教程：** https://www.bilibili.com/video/BV1x7411G7iW
- **Scrapy 教程：** https://www.bilibili.com/video/BV1aK4y1W7fV

### 实践平台

- **GitHub:** https://github.com/search?q=scraping
- **Stack Overflow:** https://stackoverflow.com/questions/tagged/web-scraping
- **V2EX:** https://www.v2ex.com/go/web-scraping

---

## 📝 备注

### 重要提醒

1. **遵守 robots.txt** - 不要抓取网站不允许抓取的内容
2. **尊重网站规则** - 不要过快发送请求，避免给网站造成压力
3. **遵守法律法规** - 不要抓取非法内容，不要侵犯隐私
4. **合理使用数据** - 不要滥用抓取的数据，不要用于非法用途

### 最佳实践

1. **降低请求频率** - 不要过快发送请求
2. **使用代理 IP** - 避免同一个 IP 被封
3. **随机 User-Agent** - 避免被识别为爬虫
4. **处理异常** - 不要因为一次请求失败就停止爬取
5. **保存中间结果** - 不要因为程序崩溃而丢失数据

---

**最后更新：** 2026-02-02 17:45（北京时间）
**会话ID：** session-20260202-0655
**当前版本：** v1.0
**下一版本：** v1.1（目标：2026-02-03）
