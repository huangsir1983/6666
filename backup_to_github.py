#!/usr/bin/env python3
"""
记忆系统备份脚本
每天自动备份记忆文件到 GitHub 私有仓库
"""

import requests
import json
import os
from datetime import datetime
import subprocess

# 配置
GITHUB_TOKEN = "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"
GITHUB_API = "https://api.github.com"
MEMORY_DIR = "/root/.openclaw/workspace/memory_system"
REPO_OWNER = "huangsir1983"
REPO_NAME = "ai-toolkit-memory"

# GitHub 认证
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}

print("=" * 60)
print("🔄 记忆系统备份到 GitHub")
print("=" * 60)

# 第一步：检查或创建私有仓库
print(f"\n📋 第一步：检查私有仓库 {REPO_NAME}...")

check_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}"
response = requests.get(check_url, headers=headers)

if response.status_code == 200:
    repo = response.json()
    print(f"✅ 仓库已存在")
    print(f"   名称：{repo.get('name')}")
    print(f"   可见性：{'私有' if repo.get('private') else '公开'}")
elif response.status_code == 404:
    print(f"⚠️ 仓库不存在，尝试创建...")
    
    # 创建私有仓库
    create_url = f"{GITHUB_API}/user/repos"
    data = {
        "name": REPO_NAME,
        "description": "AI 工具箱长期记忆系统 - 知识库、技能库、核心记忆",
        "private": True,  # 私有仓库
        "has_issues": True,
        "has_wiki": True
    }
    
    response = requests.post(create_url, headers=headers, json=data)
    
    if response.status_code == 201:
        repo = response.json()
        print(f"✅ 私有仓库创建成功")
        print(f"   名称：{repo.get('name')}")
        print(f"   URL：{repo.get('html_url')}")
    else:
        print(f"❌ 仓库创建失败，状态码：{response.status_code}")
        print(f"   错误：{response.text}")
        exit(1)
else:
    print(f"❌ 检查仓库失败，状态码：{response.status_code}")
    print(f"   错误：{response.text}")
    exit(1)

# 第二步：添加所有记忆文件到 Git
print(f"\n📝 第二步：添加所有记忆文件到 Git...")

# 检查是否在 Git 仓库中
if not os.path.exists(os.path.join(MEMORY_DIR, '.git')):
    print(f"⚠️  {MEMORY_DIR} 不是 Git 仓库，需要先初始化")
    print(f"💡 建议：在 {MEMORY_DIR} 中执行 `git init`")
    print(f"💡 建议：添加远程仓库 `git remote add origin {repo.get('clone_url')}`")
    print(f"💡 建议：提交所有文件 `git add . && git commit -m 'Initial commit'`")
    print(f"💡 建议：推送到远程 `git push -u origin main`")
    exit(0)

# 添加所有文件到 Git
os.chdir(MEMORY_DIR)

# Git add
result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True)
print(f"✅ Git add: {result.returncode == 0 and '成功' or '失败'}")

# Git commit
commit_message = f"Daily backup - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
result = subprocess.run(['git', 'commit', '-m', commit_message], capture_output=True, text=True)
print(f"✅ Git commit: {result.returncode == 0 and '成功' or '失败'}")

# Git push
result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
if result.returncode == 0:
    print(f"✅ Git push: 成功")
else:
    print(f"⚠️ Git push: 失败")
    print(f"   输出：{result.stdout}")
    print(f"   错误：{result.stderr}")

# 第三步：记录备份信息
print(f"\n📊 第三步：记录备份信息...")

backup_info = {
    "backup_time": datetime.now().isoformat(),
    "files_backed": [],
    "categories": {
        "core": 0,
        "knowledge": 0,
        "skills": 0,
        "daily": 0
    }
}

# 统计各分类的文件
categories = {
    "core": ["SESSION_MEMORY.md", "TASKS.md", "CONTEXT.md", "DECISIONS.md"],
    "knowledge": ["KNOWLEDGE_BASE.md", "LESSONS_LEARNED.md"],
    "skills": ["SKILLS.md", "CHEATSHEETS.md", "QUICK_STARTS.md", "WORKFLOWS.md"],
    "daily": ["DAILY_SUMMARY.md", "DAILY_PROGRESS.md"]
}

for category, files in categories.items():
    count = 0
    for filename in files:
        filepath = os.path.join(MEMORY_DIR, category if category != 'skills' else 'knowledge', filename)
        if os.path.exists(filepath):
            backup_info["files_backed"].append({
                "filename": filename,
                "category": category,
                "path": filepath,
                "size": os.path.getsize(filepath)
            })
            count += 1
    backup_info["categories"][category] = count

# 保存备份信息
backup_info_file = os.path.join(MEMORY_DIR, "backup_info.json")
with open(backup_info_file, 'w', encoding='utf-8') as f:
    json.dump(backup_info, f, ensure_ascii=False, indent=2)

print(f"✅ 备份信息已保存到 {backup_info_file}")
print(f"   备份时间：{backup_info['backup_time']}")
print(f"   文件数量：{len(backup_info['files_backed'])}")
print(f"   核心文件：{backup_info['categories']['core']}")
print(f"   知识库文件：{backup_info['categories']['knowledge']}")
print(f"   技能库文件：{backup_info['categories']['skills']}")
print(f"   每日文件：{backup_info['categories']['daily']}")

# 第四步：更新 SESSION_MEMORY.md（如果有新的知识或技能）
print(f"\n📝 第四步：更新 SESSION_MEMORY.md...")

session_memory_path = os.path.join(MEMORY_DIR, "core/SESSION_MEMORY.md")

try:
    with open(session_memory_path, 'r', encoding='utf-8') as f:
        session_memory = f.read()
    
    # 添加备份记录
    backup_record = f"""
## 🔄 记忆系统备份

**备份时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}

**备份到：**
- GitHub 私有仓库：{REPO_OWNER}/{REPO_NAME}
- 仓库 URL：https://github.com/{REPO_OWNER}/{REPO_NAME}

**备份文件：**
- 核心记忆：{backup_info['categories']['core']} 个文件
- 知识库：{backup_info['categories']['knowledge']} 个文件
- 技能库：{backup_info['categories']['skills']} 个文件
- 每日记录：{backup_info['categories']['daily']} 个文件
- 总计：{len(backup_info['files_backed'])} 个文件

**备份频率：** 每天凌晨 2:00（北京时间）

---

"""
    
    # 追加到 SESSION_MEMORY.md
    with open(session_memory_path, 'a', encoding='utf-8') as f:
        f.write(session_memory)
        f.write(backup_record)
    
    print(f"✅ SESSION_MEMORY.md 已更新")
    
except Exception as e:
    print(f"⚠️  更新 SESSION_MEMORY.md 失败：{str(e)}")

print(f"\n{'=' * 60}")
print(f"✅ 备份完成！")
print(f"{'=' * 60}")
print(f"\n💡 下次备份：{datetime.now() + timedelta(days=1)}")
