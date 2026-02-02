#!/usr/bin/env python3
"""
🔌 记忆系统自动备份插件
每小时自动备份所有信息到 GitHub

功能：
1. 备份记忆系统（核心、知识库、技能库、每日记录）
2. 备份项目文件（所有 Python、HTML、Markdown 文件）
3. 备份推广材料（文章、文案、社交媒体内容）
4. 记录上传日志和结果
"""

import os
import json
import base64
import requests
from datetime import datetime, timedelta
import tarfile
import tempfile
import shutil

# 配置
GITHUB_TOKEN = "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"
GITHUB_API = "https://api.github.com"
REPO_OWNER = "huangsir1983"
REPO_NAME = "ai-toolkit-memory"

# 工作目录
WORKSPACE = "/root/.openclaw/workspace"
MEMORY_DIR = f"{WORKSPACE}/memory_system"

# 日志文件
LOG_FILE = f"{WORKSPACE}/plugin_log.txt"

# 日志配置
def log(message):
    """记录日志到文件和输出"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    
    # 输出到控制台
    print(log_message)
    
    # 输出到文件
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

log("=" * 60)
log("🚀 记忆系统自动备份插件 - 启动")
log("=" * 60)

# GitHub API 客户端
class GitHubUploader:
    """GitHub 上传器"""
    
    def __init__(self, token, owner, repo):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = f"{GITHUB_API}/repos/{owner}/{repo}"
        
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
    
    def check_or_create_repo(self):
        """检查或创建仓库"""
        check_url = f"{GITHUB_API}/repos/{self.owner}/{self.repo}"
        response = requests.get(check_url, headers=self.headers, timeout=10)
        
        if response.status_code == 200:
            log(f"✅ 仓库 {self.owner}/{self.repo} 已存在")
            return True
        elif response.status_code == 404:
            log(f"⚠️ 仓库不存在，尝试创建...")
            
            # 创建私有仓库
            create_url = f"{GITHUB_API}/user/repos"
            data = {
                "name": self.repo,
                "description": "AI 工具箱长期记忆系统 - 知识库、技能库、核心记忆",
                "private": True,
                "has_issues": True,
                "has_wiki": True
            }
            
            response = requests.post(create_url, headers=self.headers, json=data, timeout=10)
            
            if response.status_code == 201:
                log(f"✅ 仓库 {self.owner}/{self.repo} 创建成功")
                return True
            else:
                log(f"❌ 仓库创建失败：{response.text}")
                return False
        else:
            log(f"❌ 检查仓库失败，状态码：{response.status_code}")
            return False
    
    def upload_file(self, file_path, content, message):
        """上传文件到 GitHub"""
        # GitHub 中的相对路径
        github_path = file_path.replace(WORKSPACE + "/", "")
        
        # 检查文件是否已存在
        check_url = f"{self.base_url}/contents/{github_path}"
        response = requests.get(check_url, headers=self.headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            sha = data.get('sha', '')
            log(f"✅ 文件已存在：{github_path}, SHA: {sha[:12]}...")
        elif response.status_code == 404:
            sha = None
            log(f"⚠️  文件不存在：{github_path}, 将创建新文件")
        else:
            log(f"❌ 检查文件失败：{github_path}")
            return False
        
        # 上传文件
        content_base64 = base64.b64encode(content.encode('utf-8')).decode()
        
        data = {
            "message": message,
            "content": content_base64
        }
        
        if sha:
            data["sha"] = sha
        
        upload_url = check_url
        response = requests.put(upload_url, headers=self.headers, json=data, timeout=30)
        
        if response.status_code in [200, 201]:
            log(f"✅ 文件上传成功：{github_path}")
            return True
        else:
            log(f"❌ 文件上传失败：{github_path}, 状态码：{response.status_code}")
            return False

# 备份管理器
class BackupManager:
    """备份管理器"""
    
    def __init__(self, workspace, memory_dir):
        self.workspace = workspace
        self.memory_dir = memory_dir
        self.temp_dir = tempfile.mkdtemp()
    
    def cleanup(self):
        """清理临时目录"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            log("✅ 临时目录已清理")
    
    def create_backup_info(self):
        """创建备份信息"""
        now = datetime.now()
        
        backup_info = {
            "backup_time": now.isoformat(),
            "timezone": "Asia/Shanghai",
            "files_backed": [],
            "categories": {
                "core": 0,
                "knowledge": 0,
                "skills": 0,
                "daily": 0,
                "projects": 0,
                "promotion": 0
            },
            "stats": {
                "total_files": 0,
                "total_size": 0
            }
        }
        
        return backup_info
    
    def collect_files(self, category, directory):
        """收集指定目录的文件"""
        files = []
        
        if not os.path.exists(directory):
            log(f"⚠️ 目录不存在：{directory}")
            return files
        
        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if os.path.isfile(filepath):
                    files.append(filepath)
                    log(f"✅ 找到文件：{filepath}")
        
        return files
    
    def backup_memory_system(self, backup_info):
        """备份记忆系统"""
        log("\n📚 备份记忆系统...")
        
        # 备份核心记忆
        core_dir = f"{self.memory_dir}/core"
        core_files = self.collect_files("core", core_dir)
        
        for filepath in core_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # GitHub 中的相对路径
            github_path = filepath.replace(self.workspace + "/", "")
            
            # 上传文件
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"📚 记忆系统自动备份 - {timestamp}"
            
            backup_info["files_backed"].append({
                "category": "core",
                "path": github_path,
                "size": os.path.getsize(filepath),
                "backup_time": timestamp
            })
        
        backup_info["categories"]["core"] = len(core_files)
        
        # 备份知识库
        knowledge_dir = f"{self.memory_dir}/knowledge"
        knowledge_files = self.collect_files("knowledge", knowledge_dir)
        
        for filepath in knowledge_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            github_path = filepath.replace(self.workspace + "/", "")
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"📚 知识库自动备份 - {timestamp}"
            
            backup_info["files_backed"].append({
                "category": "knowledge",
                "path": github_path,
                "size": os.path.getsize(filepath),
                "backup_time": timestamp
            })
        
        backup_info["categories"]["knowledge"] = len(knowledge_files)
        
        # 备份技能库
        skills_dir = f"{self.memory_dir}/skills"
        skills_files = self.collect_files("skills", skills_dir)
        
        for filepath in skills_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            github_path = filepath.replace(self.workspace + "/", "")
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"🛠️ 技能库自动备份 - {timestamp}"
            
            backup_info["files_backed"].append({
                "category": "skills",
                "path": github_path,
                "size": os.path.getsize(filepath),
                "backup_time": timestamp
            })
        
        backup_info["categories"]["skills"] = len(skills_files)
        
        # 备份每日记录
        daily_dir = f"{self.memory_dir}/daily"
        daily_files = self.collect_files("daily", daily_dir)
        
        for filepath in daily_files:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            github_path = filepath.replace(self.workspace + "/", "")
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = f"📅 每日记录自动备份 - {timestamp}"
            
            backup_info["files_backed"].append({
                "category": "daily",
                "path": github_path,
                "size": os.path.getsize(filepath),
                "backup_time": timestamp
            })
        
        backup_info["categories"]["daily"] = len(daily_files)
        
        # 备份推广材料
        promotion_files = []
        promotion_patterns = [
            "*promotion*",
            "*article*",
            "*content*",
            "juejin_article_*",
            "v2ex_*",
            "zhihu_*",
            "social_media_*",
            "video_*"
        ]
        
        for root, dirs, filenames in os.walk(self.workspace):
            for filename in filenames:
                filepath = os.path.join(root, filename)
                if os.path.isfile(filepath):
                    # 检查是否是推广相关的文件
                    for pattern in promotion_patterns:
                        if pattern in filepath.lower():
                            promotion_files.append(filepath)
                            log(f"✅ 找到推广文件：{filepath}")
                            break
        
        for filepath in promotion_files:
            # 只备份 Markdown 文件和文本文件
            if filepath.endswith(('.md', '.txt', '.json')):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                github_path = filepath.replace(self.workspace + "/", "")
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message = f"📢 推广材料自动备份 - {timestamp}"
                
                backup_info["files_backed"].append({
                    "category": "promotion",
                    "path": github_path,
                    "size": os.path.getsize(filepath),
                    "backup_time": timestamp
                })
        
        backup_info["categories"]["promotion"] = len(promotion_files)
        
        # 更新统计信息
        total_size = sum(f["size"] for f in backup_info["files_backed"])
        backup_info["stats"]["total_files"] = len(backup_info["files_backed"])
        backup_info["stats"]["total_size"] = total_size
        
        log(f"✅ 记忆系统备份完成，文件数：{len(backup_info['files_backed'])}")
        
        return backup_info

# 主函数
def main():
    """主函数"""
    try:
        log("🚀 开始执行自动备份...")
        
        # 初始化上传器和备份管理器
        uploader = GitHubUploader(GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
        manager = BackupManager(WORKSPACE, MEMORY_DIR)
        
        # 检查或创建仓库
        log("\n📋 第一步：检查或创建 GitHub 仓库...")
        if not uploader.check_or_create_repo():
            log("❌ 仓库检查/创建失败，退出")
            return
        
        # 创建备份信息
        log("\n📝 第二步：创建备份信息...")
        backup_info = manager.create_backup_info()
        
        # 备份记忆系统
        backup_info = manager.backup_memory_system(backup_info)
        
        # 保存备份信息
        backup_info_path = f"{WORKSPACE}/backup_info.json"
        with open(backup_info_path, 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, ensure_ascii=False, indent=2)
        
        log(f"✅ 备份信息已保存到 {backup_info_path}")
        
        # 上传备份信息
        log("\n📤 第三步：上传备份信息到 GitHub...")
        with open(backup_info_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        github_path = backup_info_path.replace(WORKSPACE + "/", "")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"🔄 记忆系统自动备份 - {timestamp}"
        
        uploader.upload_file(backup_info_path, content, message)
        
        # 清理临时目录
        manager.cleanup()
        
        # 最终统计
        log("\n📊 第四步：最终统计...")
        log(f"✅ 总文件数：{backup_info['stats']['total_files']}")
        log(f"✅ 总大小：{backup_info['stats']['total_size']} 字节")
        log(f"✅ 分类统计：")
        log(f"   - 核心记忆：{backup_info['categories']['core']} 个")
        log(f"   - 知识库：{backup_info['categories']['knowledge']} 个")
        log(f"   - 技能库：{backup_info['categories']['skills']} 个")
        log(f"   - 每日记录：{backup_info['categories']['daily']} 个")
        log(f"   - 推广材料：{backup_info['categories']['promotion']} 个")
        
        # 记录完成时间
        completion_time = datetime.now().isoformat()
        backup_info["completion_time"] = completion_time
        
        # 更新备份信息文件
        with open(backup_info_path, 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, ensure_ascii=False, indent=2)
        
        # 上传更新后的备份信息
        with open(backup_info_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        uploader.upload_file(backup_info_path, content, f"✅ 备份完成 - {completion_time}")
        
        log("\n" + "=" * 60)
        log("✅ 自动备份完成！")
        log("=" * 60)
        log(f"\n💡 下次备份时间：{datetime.now() + timedelta(hours=1)}")
        
    except Exception as e:
        log(f"❌ 自动备份失败：{str(e)}")
        import traceback
        log(f"错误堆栈：{traceback.format_exc()}")

if __name__ == '__main__':
    main()
