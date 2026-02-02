#!/usr/bin/env python3
"""
🕵️ 实时网络搜索脚本 V2（真实数据版本）
使用公开 API 和 HTML 抓取，获取真实数据
不模拟，不伪造
"""

import requests
from bs4 import BeautifulSoup
import json
import os
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
    log_message = f"[{timestamp}] [REAL-WEB-SEARCH-V2] {message}"
    print(log_message)
    
    # 记录到文件
    log_file = f"{WORKSPACE}/real_web_search_v2_log.txt"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

# 创建学习目录
os.makedirs(LEARNING_DIR, exist_ok=True)


def search_github_global(query, limit=10):
    """搜索 GitHub（全局搜索，不限仓库）"""
    log(f"\n🔍 [GitHub 全局] 搜索: {query}")
    
    url = f"{GITHUB_API}/search/repositories"
    params = {
        "q": query,
        "sort": "stars",  # 按星数排序
        "order": "desc",
        "per_page": limit
    }
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            log(f"   ✅ 找到 {len(items)} 个结果")
            
            results = []
            for item in items[:limit]:
                results.append({
                    "name": item.get("full_name", ""),
                    "description": item.get("description", ""),
                    "url": item.get("html_url", ""),
                    "language": item.get("language", ""),
                    "stars": item.get("stargazers_count", 0),
                    "forks": item.get("forks_count", 0),
                    "watchers": item.get("watchers_count", 0),
                    "created_at": item.get("created_at", ""),
                    "updated_at": item.get("updated_at", "")
                })
            
            return results
        else:
            log(f"   ❌ 搜索失败，状态码：{response.status_code}")
            return []
    
    except Exception as e:
        log(f"   ❌ 搜索失败：{str(e)}")
        return []


def search_hacker_news_stories(query, limit=10):
    """搜索 Hacker News 故事（使用 Algolia API）"""
    log(f"\n🔍 [Hacker News 故事] 搜索: {query}")
    
    url = "http://hn.algolia.com/api/v1/search"
    params = {
        "query": query,
        "tags": "story",
        "hitsPerPage": limit
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
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
                    "created_at_i": hit.get("created_at_i", 0)
                })
            
            return results
        else:
            log(f"   ❌ 搜索失败，状态码：{response.status_code}")
            return []
    
    except Exception as e:
        log(f"   ❌ 搜索失败：{str(e)}")
        return []


def scrape_towards_data_science(limit=10):
    """抓取 Towards Data Science (TDS) 最新文章"""
    log(f"\n🔍 [TDS] 抓取最新文章")
    
    url = "https://towardsdatascience.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # TDS 文章列表 (根据 TDS 的实际 HTML 结构)
            # 假设文章在特定的 div 中 (这里使用通用选择器，实际可能需要调整)
            articles = soup.find_all('article') # 通用标签
            
            results = []
            count = 0
            for article in articles:
                if count >= limit:
                    break
                
                try:
                    title_tag = article.find('h2') or article.find('h3')
                    title = title_tag.text.strip() if title_tag else "N/A"
                    
                    link_tag = article.find('a')
                    link = f"https://towardsdatascience.com{link_tag.get('href', '')}" if link_tag else "N/A"
                    
                    # 尝试提取作者、日期、标签等元数据 (根据 TDS 的实际结构)
                    author = "N/A"
                    date = "N/A"
                    tags = []
                    
                    # 提取摘要 (使用第一个 p 标签)
                    p_tags = article.find_all('p')
                    summary = p_tags[0].text.strip() if p_tags else "N/A"
                    
                    results.append({
                        "title": title,
                        "link": link,
                        "author": author,
                        "date": date,
                        "tags": tags,
                        "summary": summary
                    })
                    
                    count += 1
                except:
                    continue
            
            log(f"   ✅ 抓取到 {len(results)} 篇文章")
            return results
        else:
            log(f"   ❌ 抓取失败，状态码：{response.status_code}")
            return []
    
    except Exception as e:
        log(f"   ❌ 抓取失败：{str(e)}")
        return []


def analyze_and_filter(results):
    """分析和筛选优质内容"""
    log(f"\n🔍 开始分析和筛选优质内容...")
    
    filtered_results = []
    
    # 筛选标准
    MIN_POINTS = 50  # Hacker News 最小分数
    MIN_STARS = 100  # GitHub 最小星数
    MIN_FORKS = 10   # GitHub 最小 Fork 数
    
    for result in results:
        # Hacker News 故事
        if 'points' in result and result['points'] >= MIN_POINTS:
            filtered_results.append(result)
        
        # GitHub 仓库
        elif 'stars' in result and (result['stars'] >= MIN_STARS or result['forks'] >= MIN_FORKS):
            filtered_results.append(result)
        
        # TDS 文章 (全部保留，因为无法直接获取 Claps 数据)
        elif 'summary' in result and result['summary'] != "N/A":
            filtered_results.append(result)
    
    log(f"   ✅ 筛选后剩余 {len(filtered_results)} 个结果")
    
    return filtered_results


def save_to_learning_system(results):
    """保存到学习系统"""
    log(f"\n💾 保存到学习系统...")
    
    output_file = f"{LEARNING_DIR}/WEB_LEARNING_RESULTS_{datetime.now(BEIJING_TZ).strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 🌐 网络学习结果\n\n")
        f.write(f"**生成时间：** {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**来源：** Hacker News, GitHub, Towards Data Science\n\n")
        f.write("---\n\n")
        
        # Hacker News 结果
        f.write("## 🤖 Hacker News 故事\n\n")
        for i, result in enumerate(results, 1):
            if 'points' in result:
                f.write(f"{i}. **{result['title']}**\n")
                f.write(f"   - **链接：** [{result['url']}]({result['url']})\n")
                f.write(f"   - **分数：** {result['points']}\n")
                f.write(f"   - **作者：** {result['author']}\n")
                f.write(f"   - **评论数：** {result['num_comments']}\n")
                f.write("\n")
        
        # GitHub 结果
        f.write("## 🐙 GitHub 仓库\n\n")
        for i, result in enumerate(results, 1):
            if 'stars' in result:
                f.write(f"{i}. **{result['name']}**\n")
                f.write(f"   - **链接：** [{result['url']}]({result['url']})\n")
                f.write(f"   - **描述：** {result['description']}\n")
                f.write(f"   - **语言：** {result['language']}\n")
                f.write(f"   - **星数：** {result['stars']}\n")
                f.write(f"   - **Fork 数：** {result['forks']}\n")
                f.write("\n")
        
        # TDS 结果
        f.write("## 💻 Towards Data Science 文章\n\n")
        for i, result in enumerate(results, 1):
            if 'summary' in result:
                f.write(f"{i}. **{result['title']}**\n")
                f.write(f"   - **链接：** [{result['link']}]({result['link']})\n")
                f.write(f"   - **作者：** {result['author']}\n")
                f.write(f"   - **摘要：** {result['summary'][:100]}...\n")
                f.write("\n")
    
    log(f"   ✅ 学习结果已保存到 {output_file}")
    
    return output_file


# 主函数
def main():
    """主函数"""
    log("=" * 60)
    log("🕵️ 实时网络搜索 V2 - 开始（真实数据版本）")
    log("=" * 60)
    
    # 搜索查询
    queries = {
        "github_global": "langchain agent",
        "hacker_news_stories": "AI agent evolution",
        "hacker_news_stories_2": "AI赚钱"  # 中文关键词可能无效，尝试英文 "AI赚钱"
    }
    
    results = []
    
    # 1. GitHub 全局搜索
    results_github = search_github_global(queries['github_global'], limit=10)
    results.extend(results_github)
    
    # 2. Hacker News 故事搜索
    results_hn = search_hacker_news_stories(queries['hacker_news_stories'], limit=10)
    results.extend(results_hn)
    
    # 3. Hacker News 故事搜索 (中文关键词)
    results_hn_2 = search_hacker_news_stories("AI赚钱", limit=10)  # 可能无效
    results.extend(results_hn_2)
    
    # 4. TDS 抓取
    results_tds = scrape_towards_data_science(limit=10)
    results.extend(results_tds)
    
    # 分析和筛选
    filtered_results = analyze_and_filter(results)
    
    # 保存到学习系统
    output_file = save_to_learning_system(filtered_results)
    
    # 最终总结
    log(f"\n" + "=" * 60)
    log("✅ 实时网络搜索 V2 完成！")
    log("=" * 60)
    
    log(f"\n📊 搜索统计：")
    log(f"   GitHub 全局搜索：{len(results_github)} 个结果")
    log(f"   Hacker News 故事搜索：{len(results_hn)} 个结果")
    log(f"   TDS 抓取：{len(results_tds)} 个结果")
    log(f"   总计：{len(results)} 个结果")
    log(f"   筛选后：{len(filtered_results)} 个结果")
    
    log(f"\n🔗 学习结果文件：")
    log(f"   {output_file}")


if __name__ == '__main__':
    main()
