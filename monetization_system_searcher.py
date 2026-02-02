#!/usr/bin/env python3
"""
💰 赚钱循环与体系搜索器
目标：
1. 搜索赚钱循环（AI 自动化赚钱、闭环变现）
2. 搜索赚钱体系（建立可持续商业闭环）
3. 分析落地 S.O.P (能立即执行、可复制的标准操作流程）
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timezone, timedelta

# 配置
WORKSPACE = "/root/.openclaw/workspace"
LEARNING_DIR = f"{WORKSPACE}/memory_system/learning"
SOP_DIR = f"{WORKSPACE}/memory_system/sop"  # Standard Operating Procedures
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
    log_message = f"[{timestamp}] [MONETIZATION-SEARCH] {message}"
    print(log_message)
    
    # 记录到文件
    log_file = f"{WORKSPACE}/monetization_search_log.txt"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

# 创建目录
os.makedirs(LEARNING_DIR, exist_ok=True)
os.makedirs(SOP_DIR, exist_ok=True)


class GitHubMonetizationSearcher:
    """GitHub 赚钱体系搜索器"""
    
    def __init__(self, token):
        self.token = token
        self.base_url = f"{GITHUB_API}/search/repositories"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def search_repos(self, query, language="python", limit=10):
        """搜索 GitHub 仓库（全局）"""
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
                        "forks": item.get("forks_count", 0)
                    })
                
                return results
            else:
                log(f"   ❌ 搜索失败，状态码：{response.status_code}")
                return []
        
        except Exception as e:
            log(f"   ❌ 搜索失败：{str(e)}")
            return []


class HackerNewsMonetizationSearcher:
    """Hacker News 赚钱故事搜索器"""
    
    def __init__(self):
        self.base_url = "http://hn.algolia.com/api/v1/search"
    
    def search_stories(self, query, tags="story", limit=10):
        """搜索 Hacker News 故事"""
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
                log(f"   ✅ 找到 {len(hits)} 个故事")
                
                results = []
                for hit in hits[:limit]:
                    results.append({
                        "title": hit.get("title", ""),
                        "url": hit.get("url", ""),
                        "author": hit.get("author", ""),
                        "points": hit.get("points", 0),
                        "num_comments": hit.get("num_comments", 0),
                        "objectID": hit.get("objectID", "")
                    })
                
                return results
            else:
                log(f"   ❌ 搜索失败，状态码：{response.status_code}")
                return []
        
        except Exception as e:
            log(f"   ❌ 搜索失败：{str(e)}")
            return []


class SOPAnalyzer:
    """S.O.P 分析器（落地标准操作流程）"""
    
    def __init__(self):
        pass
    
    def analyze(self, search_results):
        """分析搜索结果，提取落地 S.O.P"""
        log(f"\n🔍 [S.O.P 分析器] 开始分析...")
        
        sops = []
        
        # 分析 GitHub 仓库（寻找自动化、可复制、高收入的线索）
        for repo in search_results.get('github_repos', []):
            desc = repo.get('description', '').lower()
            name = repo.get('name', '').lower()
            
            # 关键词：自动化、API、SaaS、被动收入、副业
            keywords = ['automate', 'saas', 'passive income', 'side hustle', 'revenue', 'money']
            if any(kw in desc for kw in keywords) or any(kw in name for kw in keywords):
                sops.append({
                    "type": "GitHub 仓库",
                    "name": repo['name'],
                    "description": repo['description'],
                    "url": repo['url'],
                    "stars": repo['stars'],
                    "insight": "这是一个可能包含自动化赚钱或SaaS模式的仓库"
                })
        
        # 分析 Hacker News 故事（寻找实际案例和经验分享）
        for story in search_results.get('hacker_news_stories', []):
            title = story.get('title', '').lower()
            
            # 关键词：赚钱、副业、自动化、收入
            keywords = ['side project', 'side hustle', 'make money', 'passive income', 'saas', 'automation']
            if any(kw in title for kw in keywords):
                sops.append({
                    "type": "Hacker News 故事",
                    "title": story['title'],
                    "url": story['url'],
                    "points": story['points'],
                    "insight": "这是一个关于AI赚钱或副业的经验分享"
                })
        
        log(f"   ✅ 分析完成，找到 {len(sops)} 个潜在的落地 S.O.P")
        
        return sops
    
    def generate_sop_report(self, sops):
        """生成 S.O.P 报告"""
        log(f"\n💾 生成 S.O.P 报告...")
        
        report_lines = []
        report_lines.append("# 💰 赚钱循环与体系 S.O.P 报告")
        report_lines.append(f"\n**生成时间：** {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**来源：** GitHub 仓库搜索, Hacker News 故事搜索")
        report_lines.append("\n---\n")
        
        # GitHub 仓库 S.O.P
        report_lines.append("## 🐙 GitHub 仓库（潜在赚钱模式）\n")
        for i, sop in enumerate(sops, 1):
            if sop['type'] == "GitHub 仓库":
                report_lines.append(f"{i}. **{sop['name']}**")
                report_lines.append(f"   - **描述：** {sop['description']}")
                report_lines.append(f"   - **链接：** [{sop['url']}]({sop['url']})")
                report_lines.append(f"   - **星数：** {sop['stars']}")
                report_lines.append(f"   - **洞察：** {sop['insight']}")
                report_lines.append("\n")
        
        # Hacker News 故事 S.O.P
        if any(sop['type'] == "Hacker News 故事" for sop in sops):
            report_lines.append("## 🤖 Hacker News 故事（经验分享）\n")
            for i, sop in enumerate(sops, 1):
                if sop['type'] == "Hacker News 故事":
                    report_lines.append(f"{i}. **{sop['title']}**")
                    report_lines.append(f"   - **链接：** [{sop['url']}]({sop['url']})")
                    report_lines.append(f"   - **分数：** {sop['points']}")
                    report_lines.append(f"   - **洞察：** {sop['insight']}")
                    report_lines.append("\n")
        
        # 保存报告
        output_file = f"{SOP_DIR}/MONETIZATION_SOP_REPORT_{datetime.now(BEIJING_TZ).strftime('%Y%m%d_%H%M%S')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        log(f"   ✅ S.O.P 报告已保存到 {output_file}")
        
        return output_file


class MonetizationSystemSearcher:
    """赚钱体系搜索引擎（综合）"""
    
    def __init__(self, github_token):
        self.github_searcher = GitHubMonetizationSearcher(github_token)
        self.hn_searcher = HackerNewsMonetizationSearcher()
        self.sop_analyzer = SOPAnalyzer()
    
    def search(self, sources=['github_repos', 'hacker_news_stories'], 'sop'], queries=None):
        """综合搜索"""
        log("=" * 60)
        log("💰 赚钱循环与体系搜索 - 开始")
        log("=" * 60)
        
        # 默认查询
        if not queries:
            queries = {
                "github_repos": "automation saas passive income side hustle",
                "hacker_news_stories": "side project side hustle make money"
            }
        
        results = {
            "github_repos": [],
            "hacker_news_stories": [],
            "sops": []
        }
        
        # 1. GitHub 仓库搜索
        if 'github_repos' in sources:
            log(f"\n📋 第一步：GitHub 仓库搜索（自动化赚钱模式）")
            results['github_repos'] = self.github_searcher.search_repos(
                queries['github_repos'],
                language="python",
                limit=10
            )
        
        # 2. Hacker News 故事搜索
        if 'hacker_news_stories' in sources:
            log(f"\n📋 第二步：Hacker News 故事搜索（经验分享）")
            results['hacker_news_stories'] = self.hn_searcher.search_stories(
                queries['hacker_news_stories'],
                tags="story",
                limit=10
            )
        
        # 3. S.O.P 分析（落地）
        if 'sop' in sources:
            log(f"\n📋 第三步：S.O.P 分析（提取落地流程）")
            results['sops'] = self.sop_analyzer.analyze(results)
            report_file = self.sop_analyzer.generate_sop_report(results['sops'])
        
        # 最终总结
        log(f"\n" + "=" * 60)
        log("✅ 赚钱循环与体系搜索完成！")
        log("=" * 60)
        
        log(f"\n📊 搜索统计：")
        log(f"   GitHub 仓库：{len(results['github_repos'])} 个结果")
        log(f"   Hacker News 故事：{len(results['hacker_news_stories'])} 个结果")
        log(f"   落地 S.O.P：{len(results['sops'])} 个潜在流程")
        
        return results


# 主函数
def main():
    """主函数"""
    engine = MonetizationSystemSearcher(GITHUB_TOKEN)
    
    # 搜索来源
    sources = ['github_repos', 'hacker_news_stories', 'sop']
    
    # 执行搜索
    results = engine.search(sources=sources)
    
    # 打印总结
    log(f"\n🔗 S.O.P 报告地址：")
    if results.get('sops'):
        log(f"   查看 {SOP_DIR}/ 目录")
    else:
        log(f"   未找到落地 S.O.P")


if __name__ == '__main__':
    main()
