#!/usr/bin/env python3
"""
🌐 OpenCode Skills 搜索器
目标：
1. 搜索 GitHub (OpenCode Skills, Cursor, Tool Use)
2. 下载技能到技能库 (memory_system/skills/)
3. 学习 Claude Code Standards
4. 固化标准 (创建 Claude Skill 类)
5. 分析赚钱循环 (需求挖掘 -> 明确 -> 分析 -> 实现 -> 销售)
6. 强化学习 (针对赚钱循环的每一个环节进行强化)
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import base64
from datetime import datetime, timezone, timedelta

# 配置
WORKSPACE = "/root/.openclaw/workspace"
SKILLS_DIR = f"{WORKSPACE}/memory_system/skills"
LEARNING_DIR = f"{WORKSPACE}/memory_system/learning"
PROJECT_DIR = f"{WORKSPACE}/opencode_projects"
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
    log_message = f"[{timestamp}] [OPENCODE-SEARCH] {message}"
    print(log_message)
    
    # 记录到文件
    log_file = f"{WORKSPACE}/opencode_search_log.txt"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

# 创建目录
os.makedirs(SKILLS_DIR, exist_ok=True)
os.makedirs(LEARNING_DIR, exist_ok=True)
os.makedirs(PROJECT_DIR, exist_ok=True)


class GitHubSearcher:
    """GitHub 搜索器（专注于 OpenCode, Cursor, Tool Use）"""
    
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


class SkillDownloader:
    """技能下载器（下载 README 和代码到技能库）"""
    
    def __init__(self, token, owner, repo):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def download_file(self, url, dest_dir, filename):
        """下载文件"""
        log(f"\n📥 [下载器] URL: {url}")
        log(f"   目标目录：{dest_dir}")
        log(f"   文件名：{filename}")
        
        try:
            # 获取文件内容
            content_url = f"{GITHUB_API}/repos/{self.owner}/{self.repo}/contents/{dest_dir}/{filename}"
            response = requests.get(content_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("content", "")
                encoding = data.get("encoding", "utf-8")
                
                # Base64 解码
                if encoding == "base64":
                    file_content = base64.b64decode(content)
                else:
                    file_content = content
                
                # 保存文件
                file_path = f"{SKILLS_DIR}/{dest_dir}/{filename}"
                os.makedirs(f"{SKILLS_DIR}/{dest_dir}", exist_ok=True)
                
                with open(file_path, 'wb') as f:
                    f.write(file_content)
                
                log(f"   ✅ 下载成功：{file_path}")
                
                return file_path
            else:
                log(f"   ❌ 下载失败，状态码：{response.status_code}")
                return None
        
        except Exception as e:
            log(f"   ❌ 下载失败：{str(e)}")
            return None
    
    def download_repos_readme(self, repos, limit=5):
        """下载仓库的 README"""
        log(f"\n📥 [下载器] 下载 README (前 {min(len(repos), limit)} 个仓库）")
        
        downloaded_files = []
        for i, repo in enumerate(repos[:limit], 1):
            repo_name = repo['name']
            readme_url = f"https://raw.githubusercontent.com/{repo_name}/main/README.md"
            
            log(f"\n{i}. 下载 {repo_name} 的 README...")
            
            try:
                response = requests.get(readme_url, timeout=10)
                
                if response.status_code == 200:
                    # 保存文件
                    safe_repo_name = repo_name.replace('/', '_')
                    file_path = f"{SKILLS_DIR}/github_repos/{safe_repo_name}_README.md"
                    os.makedirs(f"{SKILLS_DIR}/github_repos", exist_ok=True)
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    downloaded_files.append(file_path)
                    log(f"   ✅ 下载成功：{file_path}")
                else:
                    log(f"   ❌ 下载失败，状态码：{response.status_code}")
            
            except Exception as e:
                log(f"   ❌ 下载失败：{str(e)}")
        
        log(f"\n   ✅ 下载完成：{len(downloaded_files)} 个 README 文件")
        return downloaded_files


class OpenCodeSkillsSearcher:
    """OpenCode Skills 搜索器（综合）"""
    
    def __init__(self, github_token, github_owner, github_repo):
        self.github_searcher = GitHubSearcher(github_token, github_owner, github_repo)
        self.skill_downloader = SkillDownloader(github_token, github_owner, github_repo)
    
    def search_and_download(self, queries):
        """搜索并下载技能"""
        log("=" * 60)
        log("🌐 OpenCode Skills 搜索 - 开始")
        log("=" * 60)
        
        # 1. 搜索 OpenCode 相关仓库
        log(f"\n📋 第一步：搜索 OpenCode 相关仓库（查询：{queries.get('repos', '')}）")
        repos = self.github_searcher.search_repos(
            queries.get('repos', 'cursor opencode'),
            language="python",
            limit=10
        )
        
        # 2. 搜索 Tool Use 相关代码
        log(f"\n📋 第二步：搜索 Tool Use 相关代码（查询：{queries.get('code', '')}）")
        codes = self.github_searcher.search_code(
            queries.get('code', 'anthropic-tools tool_use'),
            limit=10
        )
        
        # 3. 下载 README
        if repos:
            log(f"\n📋 第三步：下载 README（前 5 个仓库）")
            self.skill_downloader.download_repos_readme(repos, limit=5)
        
        # 4. 分析结果
        log(f"\n📊 分析结果...")
        log(f"   仓库搜索：{len(repos)} 个结果")
        log(f"   代码搜索：{len(codes)} 个结果")
        
        # 5. 保存搜索结果
        output_file = f"{LEARNING_DIR}/OPENCODE_SKILLS_SEARCH_RESULTS_{datetime.now(BEIJING_TZ).strftime('%Y%m%d_%H%M%S')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 🌐 OpenCode Skills 搜索结果\n\n")
            f.write(f"**搜索时间：** {datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**来源：** GitHub 全局搜索, GitHub 代码搜索\n")
            f.write("\n---\n\n")
            
            # 仓库结果
            if repos:
                f.write("## 🐙 OpenCode 仓库\n\n")
                for i, repo in enumerate(repos, 1):
                    f.write(f"{i}. **{repo['name']}**\n")
                    f.write(f"   - **描述：** {repo['description']}\n")
                    f.write(f"   - **链接：** [{repo['url']}]({repo['url']})\n")
                    f.write(f"   - **语言：** {repo['language']}\n")
                    f.write(f"   - **星数：** {repo['stars']}\n")
                    f.write("\n")
            
            # 代码结果
            if codes:
                f.write("## 📄 OpenCode 代码片段\n\n")
                for i, code in enumerate(codes, 1):
                    f.write(f"{i}. **{code['name']}**\n")
                    f.write(f"   - **仓库：** {code['repository']}\n")
                    f.write(f"   - **路径：** `{code['path']}`\n")
                    f.write(f"   - **链接：** [{code['html_url']}]({code['html_url']})\n")
                    f.write(f"   - **分数：** {code['score']}\n")
                    f.write("\n")
        
        log(f"   ✅ 搜索结果已保存到 {output_file}")
        
        # 最终总结
        log(f"\n" + "=" * 60)
        log("✅ OpenCode Skills 搜索 - 完成")
        log("=" * 60)
        
        return output_file


# 主函数
def main():
    """主函数"""
    searcher = OpenCodeSkillsSearcher(
        github_token=GITHUB_TOKEN,
        github_owner=REPO_OWNER,
        github_repo=REPO_NAME
    )
    
    # 搜索查询
    queries = {
        "repos": "cursor opencode",
        "code": "anthropic-tools tool_use"
    }
    
    # 执行搜索
    report_file = searcher.search_and_download(queries)
    
    # 打印总结
    log(f"\n🔗 报告地址：")
    log(f"   {report_file}")
    
    log(f"\n💡 下一步：")
    log(f"   1. 学习 Claude Code Standards（关于 Skills 建立的标准）")
    log(f"   2. 固化标准（创建 Claude Skill 类）")
    log(f"   3. 分析赚钱循环（需求挖掘 -> 明确 -> 分析 -> 实现 -> 销售）")
    log(f"   4. 强化学习（针对赚钱循环的每一个环节进行强化）")


if __name__ == '__main__':
    main()
