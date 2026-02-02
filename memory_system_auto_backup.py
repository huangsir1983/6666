#!/usr/bin/env python3
"""
💾 记忆系统自动备份脚本（修复版 v2）
修复：修正分支名称（master -> main）
自动上传记忆系统到 GitHub
"""

import requests
import json
import os
import base64
from datetime import datetime, timezone, timedelta
import glob

# 配置
WORKSPACE = "/root/.openclaw/workspace"
MEMORY_DIR = f"{WORKSPACE}/memory_system"
GITIGNORE_FILE = f"{WORKSPACE}/.gitignore"
BACKUP_LOG_FILE = f"{WORKSPACE}/memory_auto_backup.log"
BACKUP_REPORT_FILE = f"{WORKSPACE}/memory_auto_backup_report.json"

GITHUB_TOKEN = "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"
GITHUB_API = "https://api.github.com"
REPO_OWNER = "huangsir1983"
REPO_NAME = "6666"
DEFAULT_BRANCH = "main"  # 修正：使用 main 分支

# 日志配置
def log(message):
    """记录日志"""
    timestamp = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [AUTO-BACKUP] {message}"
    print(log_message)
    
    # 记录到文件
    with open(BACKUP_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

# GitHub 客户端
class GitHubMemoryClient:
    """GitHub 记忆客户端"""
    
    def __init__(self, token, owner, repo, branch):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.branch = branch  # 使用正确的分支
        self.base_url = f"{GITHUB_API}/repos/{owner}/{repo}"
        
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
    
    def read_gitignore(self):
        """读取 .gitignore 文件"""
        ignore_patterns = []
        if os.path.exists(GITIGNORE_FILE):
            with open(GITIGNORE_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        ignore_patterns.append(line)
        return ignore_patterns
    
    def is_ignored(self, filepath, ignore_patterns):
        """检查文件是否被忽略"""
        # 简单的 .gitignore 匹配
        for pattern in ignore_patterns:
            if pattern in filepath:
                return True
        return False
    
    def upload_file(self, filepath, base64_content):
        """上传文件"""
        # 获取相对于工作区的路径
        relative_path = filepath.replace(f"{WORKSPACE}/", "")
        
        # 检查文件是否被忽略
        ignore_patterns = self.read_gitignore()
        if self.is_ignored(relative_path, ignore_patterns):
            return {
                "success": False,
                "skipped": True,
                "reason": "File is in .gitignore"
            }
        
        # 检查文件是否在 memory_system 目录
        if not filepath.startswith(MEMORY_DIR):
            return {
                "success": False,
                "skipped": True,
                "reason": "File is not in memory_system directory"
            }
        
        # 检查文件是否存在
        if not os.path.exists(filepath):
            return {
                "success": False,
                "skipped": True,
                "reason": "File does not exist"
            }
        
        # 读取文件
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
        except Exception as e:
            return {
                "success": False,
                "error": f"读取文件失败：{str(e)}"
            }
        
        # 检查文件是否已存在
        github_path = relative_path.replace("\\", "/")
        check_url = f"{self.base_url}/contents/{github_path}"
        response = requests.get(check_url, headers=self.headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            sha = data.get('sha', '')
        elif response.status_code == 404:
            sha = None
        else:
            return {
                "success": False,
                "error": f"检查文件失败，状态码：{response.status_code}"
            }
        
        # 上传文件
        upload_data = {
            "message": f"docs: 自动备份记忆系统文件 {relative_path}",
            "content": base64_content,
            "branch": self.branch  # 使用正确的分支
        }
        
        if sha:
            upload_data["sha"] = sha
        
        upload_url = f"{self.base_url}/contents/{github_path}"
        response = requests.put(upload_url, headers=self.headers, json=upload_data, timeout=60)
        
        if response.status_code in [200, 201]:
            data = response.json()
            return {
                "success": True,
                "sha": data.get('sha', ''),
                "content": data.get('content', {}),
                "path": relative_path
            }
        else:
            return {
                "success": False,
                "error": f"上传失败，状态码：{response.status_code}",
                "message": response.text
            }

# 主函数
def main():
    """主函数"""
    log("=" * 60)
    log("💾 记忆系统自动备份 - 开始（修复版 v2：main 分支）")
    log("=" * 60)
    
    # 初始化客户端
    client = GitHubMemoryClient(GITHUB_TOKEN, REPO_OWNER, REPO_NAME, DEFAULT_BRANCH)
    
    # 查找记忆系统目录下的所有文件
    log("\n📋 第一步：查找记忆系统文件...")
    
    memory_files = []
    
    # 查找所有 Markdown 文件
    for root, dirs, files in os.walk(MEMORY_DIR):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                memory_files.append(filepath)
    
    # 查找所有 JSON 文件
    for root, dirs, files in os.walk(MEMORY_DIR):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                memory_files.append(filepath)
    
    log(f"   找到 {len(memory_files)} 个文件（Markdown + JSON）")
    
    # 第二步：上传文件
    log(f"\n📤 第二步：上传文件到 GitHub（分支：{DEFAULT_BRANCH}）...")
    
    uploaded_count = 0
    failed_count = 0
    skipped_count = 0
    backup_report = {
        "backup_time": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "workspace": WORKSPACE,
        "memory_dir": MEMORY_DIR,
        "repo_owner": REPO_OWNER,
        "repo_name": REPO_NAME,
        "branch": DEFAULT_BRANCH,
        "total_files": len(memory_files),
        "uploaded_files": 0,
        "failed_files": 0,
        "skipped_files": 0,
        "uploaded_files_list": [],
        "failed_files_list": [],
        "skipped_files_list": []
    }
    
    for i, filepath in enumerate(memory_files, 1):
        try:
            # 读取文件
            with open(filepath, 'rb') as f:
                content = f.read()
            
            # Base64 编码
            base64_content = base64.b64encode(content).decode('utf-8')
            
            # 上传文件
            result = client.upload_file(filepath, base64_content)
            
            if result["success"]:
                uploaded_count += 1
                backup_report["uploaded_files"] += 1
                backup_report["uploaded_files_list"].append({
                    "path": result["path"],
                    "sha": result["sha"]
                })
                
                if i % 10 == 0:
                    log(f"   已上传 {uploaded_count} 个文件...")
            elif result.get("skipped"):
                skipped_count += 1
                backup_report["skipped_files"] += 1
                backup_report["skipped_files_list"].append({
                    "path": filepath.replace(f"{WORKSPACE}/", ""),
                    "reason": result.get("reason", "")
                })
            else:
                failed_count += 1
                backup_report["failed_files"] += 1
                backup_report["failed_files_list"].append({
                    "path": filepath.replace(f"{WORKSPACE}/", ""),
                    "error": result.get("error", "Unknown error")
                })
                log(f"   ❌ 上传失败：{filepath.replace(f'{WORKSPACE}/', '')}")
                log(f"      错误：{result.get('error', '')}")
        
        except Exception as e:
            failed_count += 1
            backup_report["failed_files"] += 1
            backup_report["failed_files_list"].append({
                "path": filepath.replace(f"{WORKSPACE}/", ""),
                "error": str(e)
            })
            log(f"   ❌ 上传失败：{filepath.replace(f'{WORKSPACE}/', '')}")
            log(f"      错误：{str(e)}")
    
    # 第三步：保存备份报告
    log(f"\n📊 第三步：保存备份报告...")
    
    with open(BACKUP_REPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(backup_report, f, ensure_ascii=False, indent=2)
    
    log(f"   ✅ 备份报告已保存到 {BACKUP_REPORT_FILE}")
    
    # 第四步：上传备份报告
    log(f"\n📤 第四步：上传备份报告到 GitHub...")
    
    try:
        with open(BACKUP_REPORT_FILE, 'rb') as f:
            content = f.read()
        
        base64_content = base64.b64encode(content).decode('utf-8')
        result = client.upload_file(BACKUP_REPORT_FILE, base64_content)
        
        if result["success"]:
            log(f"   ✅ 备份报告上传成功")
        else:
            log(f"   ❌ 备份报告上传失败")
    except Exception as e:
        log(f"   ❌ 备份报告上传失败：{str(e)}")
    
    # 第五步：最终总结
    log(f"\n" + "=" * 60)
    log("✅ 记忆系统自动备份完成！")
    log("=" * 60)
    
    log(f"\n📊 备份统计：")
    log(f"   总文件数：{len(memory_files)}")
    log(f"   已上传：{uploaded_count}")
    log(f"   失败：{failed_count}")
    log(f"   跳过：{skipped_count}")
    log(f"   分支：{DEFAULT_BRANCH}")
    
    log(f"\n💡 下次备份：")
    log(f"   运行：python3 memory_system_auto_backup.py")
    log(f"   或者：nohup python3 memory_system_auto_backup.py > memory_auto_backup.log 2>&1 &")

if __name__ == '__main__':
    main()
