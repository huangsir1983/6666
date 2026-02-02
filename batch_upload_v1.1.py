#!/usr/bin/env python3
"""
📤 批量上传脚本到 GitHub
修复版本：v1.1（修复 datetime 导入错误）
"""

import requests
import json
import base64
import os
import datetime  # 修复：导入 datetime 模块
from datetime import timedelta

# GitHub 配置
GITHUB_TOKEN = "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"
GITHUB_API = "https://api.github.com"
REPO_OWNER = "huangsir1983"
REPO_NAME = "6666"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}

def log(message):
    """记录日志"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    print(log_message)

print("=" * 60)
print("📤 批量上传到 GitHub v1.1（修复版）")
print("=" * 60)

# 第一步：上传重生技能文件
log("\n📋 第一步：上传重生技能文件...")

reborn_files = [
    "memory_system/reborn/REBORN_SKILL.md",
    "memory_system/reborn/REBORN_GUIDE.md",
    "memory_system/reborn/QUICK_START_REBORN.md",
    "memory_system/reborn/reborn_memory_system.py"
]

for filepath in reborn_files:
    try:
        full_path = f"/root/.openclaw/workspace/{filepath}"
        
        if not os.path.exists(full_path):
            log(f"   ⚠️  文件不存在：{filepath}")
            continue
        
        # 读取文件
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查文件是否已存在
        github_path = filepath
        check_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{github_path}"
        response = requests.get(check_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            sha = data.get('sha', '')
            log(f"   ✅ 文件已存在：{filepath}，SHA: {sha[:12]}...")
        elif response.status_code == 404:
            sha = None
            log(f"   📝 新文件：{filepath}")
        else:
            log(f"   ❌ 检查失败：{filepath}")
            continue
        
        # 上传文件
        content_base64 = base64.b64encode(content.encode('utf-8')).decode()
        
        data = {
            "message": f"docs: 添加重生技能文件 {filepath}",
            "content": content_base64
        }
        
        if sha:
            data["sha"] = sha
        
        upload_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{github_path}"
        response = requests.put(upload_url, headers=headers, json=data, timeout=30)
        
        if response.status_code in [200, 201]:
            log(f"   ✅ 上传成功：{filepath}")
        else:
            log(f"   ❌ 上传失败：{filepath}，状态码：{response.status_code}")
        
    except Exception as e:
        log(f"   ⚠️  上传异常：{filepath}，错误：{str(e)}")

# 第二步：上传掘金文章链接（更新）
log(f"\n📝 第二步：上传掘金文章链接（更新）...")

juejin_links = {
    "文章 1": {
        "标题": "AI 工具箱：降低 AI 使用门槛，让 AI 的力量触手可及",
        "链接": "https://juejin.cn/post/7601728622824767531",
        "发布时间": "2026-02-02",
        "状态": "已发布"
    },
    "文章 2": {
        "标题": "5分钟搭建自己的 AI API 服务：使用智谱 AI GLM-4.7 模型",
        "链接": "https://juejin.cn/post/7601827989611036708",
        "发布时间": "2026-02-02",
        "状态": "已发布"
    },
    "文章 5": {
        "标题": "Flask + 智谱 AI GLM-4 API 接入完整指南",
        "链接": "https://juejin.cn/post/7602051987848822803",
        "发布时间": "2026-02-02",
        "状态": "已发布"
    },
    "文章 6": {
        "标题": "普通程序员副业实践：我是如何用 AI 做第一个月副业的",
        "链接": "",
        "发布时间": "2026-02-02",
        "状态": "待发布"
    }
}

# 保存到文件
juejin_links_path = "/root/.openclaw/workspace/juejin_published_links_final.json"
with open(juejin_links_path, 'w', encoding='utf-8') as f:
    json.dump(juejin_links, f, ensure_ascii=False, indent=2)

log(f"   ✅ 掘金文章链接已更新到 {juejin_links_path}")

# 上传掘金文章链接文件
try:
    with open(juejin_links_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查文件是否已存在
    check_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/juejin_published_links_final.json"
    response = requests.get(check_url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        sha = response.json().get('sha')
    else:
        sha = None
    
    # 上传文件
    content_base64 = base64.b64encode(content.encode('utf-8')).decode()
    
    data = {
        "message": "docs: 更新掘金文章链接（v1.1）",
        "content": content_base64
    }
    
    if sha:
        data["sha"] = sha
    
    upload_url = check_url
    response = requests.put(upload_url, headers=headers, json=data, timeout=30)
    
    if response.status_code in [200, 201]:
        log(f"   ✅ 掘金文章链接文件上传成功")
    else:
        log(f"   ❌ 掘金文章链接文件上传失败，状态码：{response.status_code}")

except Exception as e:
    log(f"   ⚠️  掘金文章链接文件上传异常：{str(e)}")

# 第三步：获取最新提交并创建 Tag 和 Release
log(f"\n📋 第三步：获取最新提交并创建 Tag 和 Release...")

commits_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/commits?per_page=1"
response = requests.get(commits_url, headers=headers, timeout=10)

if response.status_code == 200:
    commits = response.json()
    if commits:
        latest_sha = commits[0].get('sha', '')
        log(f"   ✅ 最新 SHA：{latest_sha}")
    else:
        log(f"   ⚠️  没有找到提交")
else:
    log(f"   ❌ 获取提交失败，状态码：{response.status_code}")

# 第四步：创建 Tag v1.0.4
log(f"\n🏷️  第四步：创建 Tag v1.0.4...")

tag_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/git/refs/tags"

tag_data = {
    "ref": f"refs/tags/v1.0.4",
    "sha": latest_sha if 'latest_sha' in locals() else 'master'
}

response = requests.post(tag_url, headers=headers, json=tag_data)

if response.status_code == 201:
    log(f"   ✅ Tag v1.0.4 创建成功")
elif response.status_code == 422:
    log(f"   ⚠️  Tag 已存在或创建失败，跳过")
else:
    log(f"   ❌ Tag 创建失败，状态码：{response.status_code}")

# 第五步：创建 Release v1.0.4
log(f"\n📦 第五步：创建 Release v1.0.4...")

release_data = {
    "tag_name": "v1.0.4",
    "target_commitish": latest_sha if 'latest_sha' in locals() else 'master',
    "name": "AI 工具箱 v1.0.4 - 重生技能和记忆系统优化",
    "body": f"""
## 更新内容

### 重生技能
- ✅ 完整的重生技能体系
- ✅ 重生技能文件（3 个）
- ✅ 重生指南文件（1 个）
- ✅ 快速开始文件（1 个）
- ✅ 自动化脚本（1 个）

### 功能说明

### 重生技能
- 概念：AI 重启时自动恢复记忆
- 用途：保持对话和项目的连贯性
- 方法：从 GitHub 下载最新记忆
- 自动化：100% 自动化

### 记忆系统
- 核心记忆（4 个）
- 知识库（2 个）
- 技能库（4 个）
- 每日记录（3 个）
- 重生技能（4 个）

### 掘金发布
- 文章 1：AI 工具箱 - 降低 AI 使用门槛（已发布）
- 文章 2：5分钟搭建 AI API 服务（已发布）
- 文章 5：Flask + 智谱 AI GLM-4 API 接入（已发布）
- 文章 6：普通程序员副业实践（待发布）

## 重生技能使用

### 快速开始（3 步）

**第一步：运行重生脚本**
```python
python3 born_memory_system.py
```

**第二步：查看恢复报告**
```python
cat born_report.json
```

**第三步：验证记忆恢复**
```python
ls -l memory_system/
```

## 时间管理

### 内部同步时钟
- **开发中...** - 即将推出
- **功能：** 持续运行，每小时同步
- **时间标准：** 北京时间（GMT+8）

---

**发布时间：** 2026-02-02
**版本：** v1.0.4
**作者：** AI 工具箱团队
""",
    "draft": False,
    "prerelease": False
}

release_url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/releases"
response = requests.post(release_url, headers=headers, json=release_data)

if response.status_code == 201:
    release = response.json()
    log(f"   ✅ Release v1.0.4 创建成功")
    log(f"      Release URL：{release.get('html_url')}")
elif response.status_code == 422:
    log(f"   ⚠️  Release 已存在或创建失败，跳过")
else:
    log(f"   ❌ Release 创建失败，状态码：{response.status_code}")

# 第六步：最终统计
log(f"\n📊 第六步：最终统计...")

log(f"✅ 批量上传完成（v1.1）")
log(f"   重生技能文件：4 个")
log(f"   掘金文章链接：1 个")
log(f"   Tag 和 Release：v1.0.4")

log(f"\n🔗 仓库地址：")
log(f"   https://github.com/{REPO_OWNER}/{REPO_NAME}")

log(f"\n🔗 Release 地址：")
log(f"   https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/tag/v1.0.4")

log(f"\n💡 下次备份：{datetime.datetime.now() + timedelta(hours=1)}")
log(f"   插件位置：memory_system_auto_backup.py")
log(f"   备份频率：每小时一次")

log(f"\n{'=' * 60}")
log(f"✅ 批量上传完成（v1.1）")
log(f"{'=' * 60}")
