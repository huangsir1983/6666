#!/usr/bin/env python3
"""
🕸️ Google 搜索技能 - 三种实现方式
1. Selenium 自动化浏览器搜索（模拟人类）
2. Serper.dev API 搜索（工业界标准）
3. Tavily Search API 搜索（AI 专用）
"""

import requests
import json
import os
import time
from datetime import datetime, timezone, timedelta

# 尝试导入 Selenium，如果未安装则跳过
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    print("⚠️  Selenium 未安装，跳过 Selenium 搜索功能")

# 配置
WORKSPACE = "/root/.openclaw/workspace"
SEARCH_RESULTS_DIR = f"{WORKSPACE}/search_results"
BEIJING_TZ = timezone(timedelta(hours=8))

# 日志配置
def log(message):
    """记录日志"""
    timestamp = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [GOOGLE-SEARCH] {message}"
    print(log_message)
    
    # 记录到文件
    log_file = f"{WORKSPACE}/google_search_log.txt"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

# 创建搜索结果目录
os.makedirs(SEARCH_RESULTS_DIR, exist_ok=True)


class SeleniumSearcher:
    """Selenium 自动化浏览器搜索"""
    
    def __init__(self):
        self.driver = None
    
    def search(self, query, num_results=10):
        """搜索 Google（使用 Selenium）"""
        if not SELENIUM_AVAILABLE:
            log("❌ Selenium 未安装，跳过 Selenium 搜索")
            return []
        
        log(f"🔍 开始 Selenium 搜索：{query}")
        
        try:
            # 启动浏览器
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')  # 无头模式，不显示浏览器窗口
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            self.driver = webdriver.Chrome(options=options)
            
            # 访问 Google
            self.driver.get("https://www.google.com")
            
            # 找到搜索框
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "q"))
            )
            
            # 输入搜索查询
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # 等待搜索结果加载
            time.sleep(2)
            
            # 提取搜索结果
            results = []
            elements = self.driver.find_elements(By.CSS_SELECTOR, "div.g")
            
            for i, element in enumerate(elements[:num_results]):
                try:
                    # 提取标题
                    title_element = element.find_element(By.CSS_SELECTOR, "h3")
                    title = title_element.text
                    
                    # 提取链接
                    link_element = title_element.find_element(By.TAG_NAME, "a")
                    link = link_element.get_attribute("href")
                    
                    results.append({
                        "title": title,
                        "link": link
                    })
                except Exception as e:
                    log(f"   ⚠️  提取结果 {i} 失败：{str(e)}")
                    continue
            
            log(f"   ✅ 找到 {len(results)} 个搜索结果")
            
            return results
        
        except Exception as e:
            log(f"❌ Selenium 搜索失败：{str(e)}")
            return []
        
        finally:
            if self.driver:
                self.driver.quit()


class SerperSearcher:
    """Serper.dev API 搜索"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://google.serper.dev/search"
        self.headers = {
            "X-API-KEY": self.api_key
        }
    
    def search(self, query, num_results=10):
        """搜索 Google（使用 Serper.dev API）"""
        log(f"🔍 开始 Serper.dev 搜索：{query}")
        
        try:
            # 发送搜索请求
            params = {
                "q": query,
                "num": num_results
            }
            
            response = requests.get(self.base_url, params=params, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # 提取搜索结果
                results = []
                for item in data.get("organic", [])[:num_results]:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "position": item.get("position", 0)
                    })
                
                log(f"   ✅ 找到 {len(results)} 个搜索结果")
                
                return results
            else:
                log(f"❌ Serper.dev 搜索失败，状态码：{response.status_code}")
                return []
        
        except Exception as e:
            log(f"❌ Serper.dev 搜索失败：{str(e)}")
            return []


class TavilySearcher:
    """Tavily Search API 搜索"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.tavily.com/search"
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def search(self, query, num_results=10):
        """搜索 Google（使用 Tavily Search API）"""
        log(f"🔍 开始 Tavily Search 搜索：{query}")
        
        try:
            # 发送搜索请求
            data = {
                "api_key": self.api_key,
                "query": query,
                "max_results": num_results,
                "search_depth": "basic",
                "include_answer_content": False
            }
            
            response = requests.post(self.base_url, json=data, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # 提取搜索结果
                results = []
                for item in data.get("results", [])[:num_results]:
                    results.append({
                        "title": item.get("title", ""),
                        "link": item.get("url", ""),
                        "snippet": item.get("content", ""),
                        "score": item.get("score", 0),
                        "published_date": item.get("publishedDate", "")
                    })
                
                log(f"   ✅ 找到 {len(results)} 个搜索结果")
                
                return results
            else:
                log(f"❌ Tavily Search 搜索失败，状态码：{response.status_code}")
                return []
        
        except Exception as e:
            log(f"❌ Tavily Search 搜索失败：{str(e)}")
            return []


def save_search_results(results, filename):
    """保存搜索结果"""
    file_path = f"{SEARCH_RESULTS_DIR}/{filename}"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    log(f"   ✅ 搜索结果已保存到 {file_path}")
    
    return file_path


# 主函数
def main():
    """主函数"""
    log("=" * 60)
    log("🕸️ Google 搜索能力 - 开始")
    log("=" * 60)
    
    # 搜索查询
    query = "Python LangChain 教程"
    num_results = 10
    
    # 方式 1：Selenium 自动化浏览器搜索
    log("\n📋 方式 1：Selenium 自动化浏览器搜索")
    selenium_searcher = SeleniumSearcher()
    selenium_results = selenium_searcher.search(query, num_results)
    
    if selenium_results:
        selenium_file = save_search_results(selenium_results, "selenium_search_results.json")
        
        for i, result in enumerate(selenium_results[:5], 1):
            log(f"   {i}. {result['title']}")
            log(f"      链接：{result['link']}")
    else:
        log("   ⚠️  Selenium 搜索结果为空")
        selenium_file = None
    
    # 方式 2：Serper.dev API 搜索
    log("\n📋 方式 2：Serper.dev API 搜索（需要 API Key）")
    serper_api_key = "YOUR_SERPER_API_KEY"  # 替换为你的 API Key
    serper_searcher = SerperSearcher(serper_api_key)
    serper_results = serper_searcher.search(query, num_results)
    
    if serper_results:
        serper_file = save_search_results(serper_results, "serper_search_results.json")
        
        for i, result in enumerate(serper_results[:5], 1):
            log(f"   {i}. {result['title']}")
            log(f"      链接：{result['link']}")
            log(f"      摘要：{result['snippet'][:100]}")
    else:
        log("   ⚠️  Serper.dev 搜索结果为空（可能需要 API Key）")
        serper_file = None
    
    # 方式 3：Tavily Search API 搜索
    log("\n📋 方式 3：Tavily Search API 搜索（需要 API Key）")
    tavily_api_key = "YOUR_TAVILY_API_KEY"  # 替换为你的 API Key
    tavily_searcher = TavilySearcher(tavily_api_key)
    tavily_results = tavily_searcher.search(query, num_results)
    
    if tavily_results:
        tavily_file = save_search_results(tavily_results, "tavily_search_results.json")
        
        for i, result in enumerate(tavily_results[:5], 1):
            log(f"   {i}. {result['title']}")
            log(f"      链接：{result['link']}")
            log(f"      摘要：{result['snippet'][:100]}")
    else:
        log("   ⚠️  Tavily Search 搜索结果为空（可能需要 API Key）")
        tavily_file = None
    
    # 比较
    log("\n📊 比较")
    log(f"   Selenium: {len(selenium_results)} 个结果 - 文件：{selenium_file}")
    log(f"   Serper.dev: {len(serper_results)} 个结果 - 文件：{serper_file}")
    log(f"   Tavily: {len(tavily_results)} 个结果 - 文件：{tavily_file}")
    
    # 最终总结
    log("\n" + "=" * 60)
    log("✅ Google 搜索能力 - 完成")
    log("=" * 60)
    
    log(f"\n📊 搜索统计：")
    log(f"   总搜索次数：3")
    log(f"   Selenium 搜索结果：{len(selenium_results)}")
    log(f"   Serper.dev 搜索结果：{len(serper_results)}")
    log(f"   Tavily 搜索结果：{len(tavily_results)}")
    log(f"   总搜索结果：{len(selenium_results) + len(serper_results) + len(tavily_results)}")
    
    log(f"\n💡 下一步：")
    log(f"   1. 注册 Serper.dev 账号并获取 API Key")
    log(f"   2. 注册 Tavily 账号并获取 API Key")
    log(f"   3. 替换脚本中的 API Key")
    log(f"   4. 运行脚本：python3 google_search.py")


if __name__ == '__main__':
    main()
