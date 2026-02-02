#!/usr/bin/env python3
"""
🌐 向外拓展搜索引擎
策略：
1. 使用公开免费的 API（无需 Key）
2. 网页抓取
3. 链接跳转和深度抓取
4. User-Agent 伪装
5. 代理池（如果环境支持）
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import time
from datetime import datetime, timezone, timedelta

# 配置
WORKSPACE = "/root/.openclaw/workspace"
LEARNING_DIR = f"{WORKSPACE}/memory_system/learning"
BEIJING_TZ = timezone(timedelta(hours=8))

# GitHub 配置
GITHUB_TOKEN = "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"
GITHUB_API = "https://api.github.com"
REPO_OWNER = "huangsir1983"
REPO_NAME = "6666"

# 日志配置
def log(message):
    """记录日志"""
    timestamp = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [EXTERNAL-SEARCH] {message}"
    print(log_message)
    
    # 记录到文件
    log_file = f"{WORKSPACE}/external_search_log.txt"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

# 创建学习目录
os.makedirs(LEARNING_DIR, exist_ok=True)


class HackerNewsSearcher:
    """Hacker News 搜索器（使用 Algolia API，免费，无需 Key）"""
    
    def __init__(self):
        self.base_url = "http://hn.algolia.com/api/v1/search"
    
    def search(self, query, tags=None, limit=10):
        """搜索 Hacker News"""
        log(f"\n🔍 [Hacker News] 搜索: {query}")
        
        try:
            params = {
                "query": query,
                "tags": tags,
                "hitsPerPage": limit
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                hits = data.get("hits", [])
                log(f"   ✅ 找到 {len(hits)} 个结果")
                
                results = []
                for hit in hits[:limit]:
                    results.append({
                        "title": hit.get("title", ""),
                        "url": hit.get("url", ""),
                        "author": hit.get("author", ""),
                        "points": hit.get("points", 0),
                        "num_comments": hit.get("num_comments", 0),
                        "created_at": hit.get("created_at", ""),
                        "objectID": hit.get("objectID", "")
                    })
                
                return results
            else:
                log(f"   ❌ 搜索失败，状态码：{response.status_code}")
                return []
        
        except Exception as e:
            log(f"   ❌ 搜索失败：{str(e)}")
            return []


class GitHubGlobalSearcher:
    """GitHub 全局搜索器（使用 REST API，需要 Key，但有免费额度）"""
    
    def __init__(self, token, owner=None, repo=None):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = f"{GITHUB_API}/search/repositories"
        self.code_url = f"{GITHUB_API}/search/code"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def search_repos(self, query, language=None, limit=10):
        """搜索 GitHub 仓库（全局）"""
        log(f"\n🔍 [GitHub 仓库] 搜索: {query}")
        
        try:
            if language:
                search_query = f"{query} language:{language}"
            else:
                search_query = query
            
            params = {
                "q": search_query,
                "sort": "stars",
                "order": "desc",
                "per_page": limit
            }
            
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                log(f"   ✅ 找到 {len(items)} 个仓库")
                
                results = []
                for item in items[:limit]:
                    results.append({
                        "name": item.get("full_name", ""),
                        "description": item.get("description", ""),
                        "url": item.get("html_url", ""),
                        "language": item.get("language", ""),
                        "stars": item.get("stargazers_count", 0),
                        "forks": item.get("forks_count", 0),
                        "created_at": item.get("created_at", "")
                    })
                
                return results
            else:
                log(f"   ❌ 搜索失败，状态码：{response.status_code}")
                return []
        
        except Exception as e:
            log(f"   ❌ 搜索失败：{str(e)}")
            return []
    
    def search_code(self, query, limit=10):
        """搜索 GitHub 代码（全局）"""
        log(f"\n🔍 [GitHub 代码] 搜索: {query}")
        
        try:
            params = {
                "q": query,
                "sort": "indexed",
                "order": "desc",
                "per_page": limit
            }
            
            response = requests.get(self.code_url, params=params, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                log(f"   ✅ 找到 {len(items)} 个代码片段")
                
                results = []
                for item in items[:limit]:
                    results.append({
                        "name": item.get("name", ""),
                        "path": item.get("path", ""),
                        "html_url": item.get("html_url", ""),
                        "repository": item.get("repository", {}).get("full_name", ""),
                        "score": item.get("score", 0),
                        "language": item.get("language", "")
                    })
                
                return results
            else:
                log(f"   ❌ 搜索失败，状态码：{response.status_code}")
                return []
        
        except Exception as e:
            log(f"   ❌ 搜索失败：{str(e)}")
            return []


class WebScraper:
    """网页抓取器（绕过部分限制）"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def scrape(self, url, timeout=10):
        """抓取单个网页"""
        log(f"\n🔍 [网页抓取] URL: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                log(f"   ✅ 成功抓取，长度：{len(response.text)} 字节")
                
                # 提取标题、正文、链接
                title = soup.find('title')
                title_text = title.text.strip() if title else "N/A"
                
                # 尝试提取正文（取第一个 p 标签）
                body = soup.find('p')
                body_text = body.text.strip() if body else "N/A"
                
                return {
                    "url": url,
                    "title": title_text,
                    "body": body_text[:500] + "..." if len(body_text) > 500 else body_text,
                    "length": len(response.text)
                }
            else:
                log(f"   ❌ 抓取失败，状态码：{response.status_code}")
                return None
        
        except Exception as e:
            log(f"   ❌ 抓取失败：{str(e)}")
            return None
    
    def scrape_from_search_results(self, search_results, limit=5):
        """从搜索结果中抓取内容"""
        log(f"\n🔍 [从搜索结果抓取] 抓取 {min(len(search_results), limit)} 个结果...")
        
        scraped_results = []
        for i, result in enumerate(search_results[:limit], 1):
            url = result.get('url', "")
            if url:
                scraped_data = self.scrape(url)
                if scraped_data:
                    scraped_results.append({
                        "title": scraped_data['title'],
                        "url": url,
                        "body": scraped_data['body']
                    })
        
        log(f"   ✅ 成功抓取 {len(scraped_results)} 个结果")
        return scraped_results


class ExternalSearchEngine:
    """向外拓展搜索引擎（综合）"""
    
    def __init__(self, github_token=None, github_owner=None, github_repo=None):
        self.hacker_news_searcher = HackerNewsSearcher()
        
        if github_token:
            self.github_searcher = GitHubGlobalSearcher(
                token=github_token,
                owner=github_owner,
                repo=github_repo
            )
        else:
            self.github_searcher = None
        
        self.web_scraper = WebScraper()
    
    def search(self, sources=['hacker_news', 'github_repos', 'github_code'], queries=None):
        """综合搜索"""
        log("=" * 60)
        log("🌐 向外拓展搜索引擎 - 开始")
        log("=" * 60)
        
        # 默认查询
        if not queries:
            queries = {
                "hacker_news": "AI agent",
                "github_repos": "langchain",
                "github_code": "langchain agent"
            }
        
        results = {
            "hacker_news": [],
            "github_repos": [],
            "github_code": [],
            "scraped": []
        }
        
        # 1. Hacker News 搜索
        if 'hacker_news' in sources:
            log(f"\n📋 来源 1：Hacker News")
            results['hacker_news'] = self.hacker_news_searcher.search(
                queries.get('hacker_news', "AI agent"),
                tags=None,
                limit=10
            )
        
        # 2. GitHub 仓库搜索
        if 'github_repos' in sources and self.github_searcher:
            log(f"\n📋 来源 2：GitHub 仓库")
            results['github_repos'] = self.github_searcher.search_repos(
                queries.get('github_repos', "langchain"),
                language="python",
                limit=10
            )
        
        # 3. GitHub 代码搜索
        if 'github_code' in sources and self.github_searcher:
            log(f"\n📋 来源 3：GitHub 代码")
            results['github_code'] = self.github_searcher.search_code(
                queries.get('github_code', "langchain agent"),
                limit=10
            )
        
        # 4. 从搜索结果中抓取内容
        all_search_results = results['hacker_news'] + results['github_repos'] + results['github_code']
        if all_search_results:
            log(f"\n📋 来源 4：从搜索结果抓取")
            results['scraped'] = self.web_scraper.scrape_from_search_results(all_search_results, limit=5)
        
        # 保存结果
        self.save_results(results)
        
        # 最终总结
        log(f"\n" + "=" * 60)
        log("✅ 向外拓展搜索完成！")
        log("=" * 60)
        
        return results
    
    def save_results(self, results):
        """保存结果"""
        log(f"\n💾 保存搜索结果...")
        
        output_file = f"{LEARNING_DIR}/EXTERNAL_SEARCH_RESULTS_{datetime.now(BEIJING_TZ).strftime('%Y%m%d_%H%M%S')}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 🌐 向外拓展搜索结果\n\n")
            f.write(f"**搜索时间：** {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**来源：** Hacker News, GitHub\n")
            f.write("---\n\n")
            
            # Hacker News 结果
            if results['hacker_news']:
                f.write("## 🤖 Hacker News 搜索结果\n\n")
                for i, result in enumerate(results['hacker_news'], 1):
                    f.write(f"{i}. **{result['title']}**\n")
                    f.write(f"   - **链接：** [{result['url']}]({result['url']})\n")
                    f.write(f"   - **分数：** {result['points']}\n")
                    f.write(f"   - **作者：** {result['author']}\n")
                    f.write(f"   - **评论数：** {result['num_comments']}\n")
                    f.write("\n")
            
            # GitHub 仓库结果
            if results['github_repos']:
                f.write("## 🐙 GitHub 仓库搜索结果\n\n")
                for i, result in enumerate(results['github_repos'], 1):
                    f.write(f"{i}. **{result['name']}**\n")
                    f.write(f"   - **链接：** [{result['url']}]({result['url']})\n")
                    f.write(f"   - **描述：** {result['description']}\n")
                    f.write(f"   - **语言：** {result['language']}\n")
                    f.write(f"   - **星数：** {result['stars']}\n")
                    f.write(f"   - **Fork 数：** {result['forks']}\n")
                    f.write("\n")
            
            # GitHub 代码结果
            if results['github_code']:
                f.write("## 🐙 GitHub 代码搜索结果\n\n")
                for i, result in enumerate(results['github_code'], 1):
                    f.write(f"{i}. **{result['name']}**\n")
                    f.write(f"   - **仓库：** {result['repository']}\n")
                    f.write(f"   - **路径：** `{result['path']}`\n")
                    f.write(f"   - **链接：** [{result['html_url']}]({result['html_url']})\n")
                    f.write(f"   - **分数：** {result['score']}\n")
                    f.write("\n")
            
            # 抓取的内容
            if results['scraped']:
                f.write("## 📄 抓取的内容\n\n")
                for i, result in enumerate(results['scraped'], 1):
                    f.write(f"{i}. **{result['title']}**\n")
                    f.write(f"   - **链接：** {result['url']}\n")
                    f.write(f"   - **正文：** {result['body']}\n")
                    f.write("\n")
        
        log(f"   ✅ 搜索结果已保存到 {output_file}")


# 主函数
def main():
    """主函数"""
    engine = ExternalSearchEngine(
        github_token=GITHUB_TOKEN,
        github_owner=REPO_OWNER,
        github_repo=REPO_NAME
    )
    
    # 搜索来源
    sources = ['hacker_news', 'github_repos', 'github_code', 'scrape']
    
    # 执行搜索
    results = engine.search(sources=sources)
    
    # 打印总结
    log(f"\n📊 搜索统计：")
    log(f"   Hacker News: {len(results['hacker_news'])} 个结果")
    log(f"   GitHub 仓库: {len(results['github_repos'])} 个结果")
    log(f"   GitHub 代码: {len(results['github_code'])} 个结果")
    log(f"   抓取的内容: {len(results['scraped'])} 个结果")
    log(f"   总计: {len(results['hacker_news']) + len(results['github_repos']) + len(results['github_code']) + len(results['scraped'])} 个结果")


if __name__ == '__main__':
    main()
