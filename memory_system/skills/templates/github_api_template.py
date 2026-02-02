#!/usr/bin/env python3
"""
GitHub API 模板
"""

import requests
import json
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class GitHubClient:
    """GitHub API 客户端"""
    
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
    
    def get_user(self):
        """获取用户信息"""
        try:
            response = requests.get(f"{self.base_url}/user", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"获取用户信息失败：{response.status_code}")
                return None
        except Exception as e:
            logging.error(f"获取用户信息错误：{str(e)}")
            return None
    
    def get_repos(self):
        """获取仓库列表"""
        try:
            response = requests.get(f"{self.base_url}/user/repos", headers=self.headers)
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"获取仓库列表失败：{response.status_code}")
                return None
        except Exception as e:
            logging.error(f"获取仓库列表错误：{str(e)}")
            return None
    
    def get_commits(self, owner, repo, limit=10):
        """获取提交列表"""
        try:
            params = {"per_page": limit}
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}/commits",
                headers=self.headers,
                params=params
            )
            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"获取提交列表失败：{response.status_code}")
                return None
        except Exception as e:
            logging.error(f"获取提交列表错误：{str(e)}")
            return None
    
    def create_tag(self, owner, repo, tag_name, message, sha):
        """创建 Tag"""
        try:
            data = {
                "tag": tag_name,
                "message": message,
                "object": sha,
                "type": "commit"
            }
            response = requests.post(
                f"{self.base_url}/repos/{owner}/{repo}/git/tags",
                headers=self.headers,
                json=data
            )
            if response.status_code == 201:
                logging.info(f"Tag 创建成功：{tag_name}")
                return response.json()
            else:
                logging.error(f"Tag 创建失败：{response.status_code}")
                return None
        except Exception as e:
            logging.error(f"创建 Tag 错误：{str(e)}")
            return None
    
    def create_release(self, owner, repo, tag_name, release_data):
        """创建 Release"""
        try:
            data = {
                "tag_name": tag_name,
                "target_commitish": "main",
                "name": release_data.get('name', f"Release {tag_name}"),
                "body": release_data.get('body', ''),
                "draft": False,
                "prerelease": False
            }
            response = requests.post(
                f"{self.base_url}/repos/{owner}/{repo}/releases",
                headers=self.headers,
                json=data
            )
            if response.status_code == 201:
                release = response.json()
                logging.info(f"Release 创建成功：{release.get('html_url')}")
                return release
            else:
                logging.error(f"Release 创建失败：{response.status_code}")
                logging.error(f"错误信息：{response.text}")
                return None
        except Exception as e:
            logging.error(f"创建 Release 错误：{str(e)}")
            return None

# 使用示例
if __name__ == '__main__':
    # GitHub Token（只在内存中使用）
    GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
    
    # 创建客户端
    client = GitHubClient(GITHUB_TOKEN)
    
    # 获取用户信息
    user = client.get_user()
    if user:
        print(f"用户信息：")
        print(f"  用户名：{user.get('login')}")
        print(f"  显示名：{user.get('name')}")
        print(f"  类型：{user.get('type')}")
        print(f"  仓库数：{user.get('public_repos', 0)}")
    
    # 获取仓库列表
    repos = client.get_repos()
    if repos:
        print(f"\n仓库列表（前 5 个）：")
        for i, repo in enumerate(repos[:5]):
            print(f"  {i+1}. {repo.get('name')} - {repo.get('description', 'N/A')[:50]}")
