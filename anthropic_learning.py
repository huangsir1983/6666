#!/usr/bin/env python3
"""
🧠 Anthropic/Claude Code 深度学习与实战项目
目标：
1. 深度搜索 Anthropic/Claude Code 技术
2. 学习 Anthropic Python SDK (anthropic 包) 编程
3. 实现一个实际需求（例如：文档摘要器、代码审查工具、AI Agent）
4. 成为未来赚钱的技能 (tool_use, API 集成, 企业应用)
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timezone, timedelta

# 配置
WORKSPACE = "/root/.openclaw/workspace"
LEARNING_DIR = f"{WORKSPACE}/memory_system/learning"
PROJECT_DIR = f"{WORKSPACE}/anthropic_projects"
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
    log_message = f"[{timestamp}] [ANTHROPIC-LEARNING] {message}"
    print(log_message)
    
    # 记录到文件
    log_file = f"{WORKSPACE}/anthropic_learning_log.txt"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

# 创建项目目录
os.makedirs(LEARNING_DIR, exist_ok=True)
os.makedirs(PROJECT_DIR, exist_ok=True)


class GitHubAnthropicSearcher:
    """GitHub 搜索器（专注于 Anthropic）"""
    
    def __init__(self, token):
        self.token = token
        self.base_url = f"{GITHUB_API}/search/repositories"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def search_repos(self, query="anthropic", language="python", limit=10):
        """搜索 Anthropic 相关仓库"""
        log(f"\n🔍 [GitHub 全局] 搜索: {query}")
        
        try:
            search_query = f"{query} language:{language}"
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


class HackerNewsAnthropicSearcher:
    """Hacker News 搜索器（专注于 Anthropic）"""
    
    def __init__(self):
        self.base_url = "http://hn.algolia.com/api/v1/search"
    
    def search_stories(self, query="anthropic claude", limit=10):
        """搜索 Hacker News 故事"""
        log(f"\n🔍 [Hacker News] 搜索: {query}")
        
        try:
            params = {
                "query": query,
                "tags": "story",
                "hitsPerPage": limit
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                hits = data.get("hits", [])
                log(f"   ✅ 找到 {len(hits)} 个故事")
                
                results = []
                for hit in hits[:limit]:
                    results.append({
                        "title": hit.get("title", ""),
                        "url": hit.get("url", ""),
                        "author": hit.get("author", ""),
                        "points": hit.get("points", 0),
                        "num_comments": hit.get("num_comments", 0),
                        "created_at_i": hit.get("created_at_i", 0)
                    })
                
                return results
            else:
                log(f"   ❌ 搜索失败，状态码：{response.status_code}")
                return []
        
        except Exception as e:
            log(f"   ❌ 搜索失败：{str(e)}")
            return []


class AnthropicDocScraper:
    """Anthropic 文档抓取器"""
    
    def __init__(self):
        self.base_url = "https://docs.anthropic.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def scrape(self, path="/", limit=10):
        """抓取 Anthropic 文档"""
        log(f"\n🔍 [Anthropic 文档] 抓取: {self.base_url}{path}")
        
        try:
            response = requests.get(f"{self.base_url}{path}", headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                log(f"   ✅ 成功抓取，长度：{len(response.text)} 字节")
                
                # 尝试提取文章链接（根据 Anthropic 文档的实际 HTML 结构）
                # 假设文章链接在特定的 class 中 (这里使用通用选择器，实际可能需要调整)
                links = []
                for link in soup.find_all('a'):
                    href = link.get('href', '')
                    if href and '/en/docs/' in href:
                        links.append({
                            "title": link.text.strip(),
                            "url": f"{self.base_url}{href.lstrip('/')}"
                        })
                
                # 限制链接数量
                return links[:limit]
            else:
                log(f"   ❌ 抓取失败，状态码：{response.status_code}")
                return []
        
        except Exception as e:
            log(f"   ❌ 抓取失败：{str(e)}")
            return []


def generate_learning_report(results):
    """生成学习报告"""
    log(f"\n📊 生成 Anthropic/Claude Code 学习报告...")
    
    report_lines = []
    report_lines.append("# 🧠 Anthropic/Claude Code 学习报告")
    report_lines.append(f"\n**生成时间：** {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"**来源：** GitHub 全局搜索, Hacker News, Anthropic 文档抓取")
    report_lines.append("\n---\n")
    
    # GitHub 仓库结果
    if results.get('github_repos'):
        report_lines.append("## 🐙 GitHub 仓库（Top 10）")
        for i, repo in enumerate(results['github_repos'], 1):
            report_lines.append(f"{i}. **{repo['name']}**")
            report_lines.append(f"   - **描述：** {repo['description']}")
            report_lines.append(f"   - **链接：** [{repo['url']}]({repo['url']})")
            report_lines.append(f"   - **星数：** {repo['stars']}")
            report_lines.append(f"   - **语言：** {repo['language']}")
            report_lines.append("\n")
    
    # Hacker News 故事结果
    if results.get('hacker_news_stories'):
        report_lines.append("## 🤖 Hacker News 故事（Top 10）")
        for i, story in enumerate(results['hacker_news_stories'], 1):
            report_lines.append(f"{i}. **{story['title']}**")
            report_lines.append(f"   - **链接：** [{story['url']}]({story['url']})")
            report_lines.append(f"   - **分数：** {story['points']}")
            report_lines.append(f"   - **作者：** {story['author']}")
            report_lines.append(f"   - **评论数：** {story['num_comments']}")
            report_lines.append("\n")
    
    # Anthropic 文档链接结果
    if results.get('anthropic_docs'):
        report_lines.append("## 📄 Anthropic 文档链接")
        for i, doc in enumerate(results['anthropic_docs'], 1):
            report_lines.append(f"{i}. **{doc['title']}**")
            report_lines.append(f"   - **链接：** [{doc['url']}]({doc['url']})")
            report_lines.append("\n")
    
    # 保存报告
    output_file = f"{LEARNING_DIR}/ANTHROPIC_LEARNING_REPORT_{datetime.now(BEIJING_TZ).strftime('%Y%m%d_%H%M%S')}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    log(f"   ✅ 学习报告已保存到 {output_file}")
    
    return output_file


# 主函数
def main():
    """主函数"""
    log("=" * 60)
    log("🧠 Anthropic/Claude Code 深度学习 - 开始")
    log("=" * 60)
    
    # 初始化搜索器
    github_searcher = GitHubAnthropicSearcher(GITHUB_TOKEN)
    hn_searcher = HackerNewsAnthropicSearcher()
    doc_scraper = AnthropicDocScraper()
    
    # 搜索查询
    queries = {
        "github_repos": "anthropic",
        "hacker_news_stories": "anthropic claude"
    }
    
    results = {
        "github_repos": [],
        "hacker_news_stories": [],
        "anthropic_docs": []
    }
    
    # 1. GitHub 全局搜索
    log(f"\n📋 第一步：GitHub 全局搜索（Anthropic 仓库）")
    results['github_repos'] = github_searcher.search_repos(
        queries['github_repos'],
        language="python",
        limit=10
    )
    
    # 2. Hacker News 搜索
    log(f"\n📋 第二步：Hacker News 搜索（Anthropic/Claude 故事）")
    results['hacker_news_stories'] = hn_searcher.search_stories(
        queries['hacker_news_stories'],
        limit=10
    )
    
    # 3. Anthropic 文档抓取（尝试抓取首页链接）
    log(f"\n📋 第三步：Anthropic 文档抓取")
    results['anthropic_docs'] = doc_scraper.scrape(limit=10)
    
    # 生成报告
    report_file = generate_learning_report(results)
    
    # 最终总结
    log(f"\n" + "=" * 60)
    log("✅ Anthropic/Claude Code 学习阶段 - 完成")
    log("=" * 60)
    
    log(f"\n📊 学习统计：")
    log(f"   GitHub 仓库：{len(results['github_repos'])} 个结果")
    log(f"   Hacker News 故事：{len(results['hacker_news_stories'])} 个结果")
    log(f"   Anthropic 文档链接：{len(results['anthropic_docs'])} 个结果")
    log(f"   总计：{len(results['github_repos']) + len(results['hacker_news_stories']) + len(results['anthropic_docs'])} 个结果")
    
    log(f"\n🔗 学习报告：")
    log(f"   {report_file}")


if __name__ == '__main__':
    main()
