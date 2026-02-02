#!/usr/bin/env python3
"""
🧪 记忆系统自动重生脚本
当 AI 重启、打开新窗口或从新系统恢复时，自动从 GitHub 读取最新的记忆、任务和历史
"""

import requests
import json
import os
import shutil
from datetime import datetime

# 配置
GITHUB_TOKEN = "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"
GITHUB_API = "https://api.github.com"
REPO_OWNER = "huangsir1983"
REPO_NAME = "6666"

# 本地目录
WORKSPACE = "/root/.openclaw/workspace"
MEMORY_DIR = f"{WORKSPACE}/memory_system"
REBORN_DIR = f"{MEMORY_DIR}/reborn"

# 日志配置
def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [REBORN] {message}"
    print(log_message)
    
    # 记录到文件
    log_file = f"{WORKSPACE}/reborn_log.txt"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

log("=" * 60)
log("🧪 记忆系统自动重生 - 开始")
log("=" * 60)

# GitHub API 客户端
class GitHubMemoryClient:
    """GitHub 记忆客户端"""
    
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
    
    def download_file(self, filepath):
        """下载文件"""
        github_path = filepath.replace(f"{MEMORY_DIR}/", "")
        download_url = f"{self.base_url}/contents/{github_path}"
        
        response = requests.get(download_url, headers=self.headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            content_base64 = data.get('content', '')
            content = self.decode_content(content_base64)
            
            return {
                "success": True,
                "content": content,
                "sha": data.get('sha', ''),
                "size": data.get('size', 0)
            }
        else:
            return {
                "success": False,
                "error": f"下载失败，状态码：{response.status_code}"
            }
    
    def decode_content(self, content_base64):
        """解码 Base64 内容"""
        import base64
        try:
            return base64.b64decode(content_base64).decode('utf-8')
        except Exception as e:
            return ""

# 重生管理器
class RebornManager:
    """重生管理器"""
    
    def __init__(self, workspace, memory_dir):
        self.workspace = workspace
        self.memory_dir = memory_dir
        self.reborn_report = {
            "reborn_time": datetime.now().isoformat(),
            "memory_files": {},
            "core_memory": {},
            "knowledge_base": {},
            "skills_library": {},
            "daily_records": {},
            "task_status": {},
            "context_status": {},
            "iteration_status": {}
        }
    
    def download_memory_from_github(self, client):
        """从 GitHub 下载记忆"""
        log("\n📥 第一步：从 GitHub 下载记忆...")
        
        # 记忆文件列表
        memory_files = [
            # 核心记忆
            "core/SESSION_MEMORY.md",
            "core/TASKS.md",
            "core/CONTEXT.md",
            "core/DECISIONS.md",
            
            # 知识库
            "knowledge/KNOWLEDGE_BASE.md",
            "knowledge/LESSONS_LEARNED.md",
            
            # 技能库
            "skills/SKILLS.md",
            "skills/CHEATSHEETS.md",
            "skills/QUICK_STARTS.md",
            "skills/WORKFLOWS.md",
            "skills/templates/flask_app_template.py",
            "skills/templates/github_api_template.py",
            
            # 每日记录
            "daily/SELF_ITERATION.md",
            "daily/DAILY_SUMMARY.md",
            "daily/DAILY_PROGRESS.md"
        ]
        
        downloaded_count = 0
        failed_count = 0
        
        for filepath in memory_files:
            result = client.download_file(filepath)
            
            if result["success"]:
                # 保存文件
                local_path = f"{self.memory_dir}/{filepath}"
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                
                with open(local_path, 'w', encoding='utf-8') as f:
                    f.write(result["content"])
                
                downloaded_count += 1
                
                # 记录到重生报告
                if "core" in filepath:
                    self.reborn_report["core_memory"][filepath] = {
                        "size": result["size"],
                        "sha": result["sha"]
                    }
                elif "knowledge" in filepath:
                    self.reborn_report["knowledge_base"][filepath] = {
                        "size": result["size"],
                        "sha": result["sha"]
                    }
                elif "skills" in filepath:
                    self.reborn_report["skills_library"][filepath] = {
                        "size": result["size"],
                        "sha": result["sha"]
                    }
                elif "daily" in filepath:
                    self.reborn_report["daily_records"][filepath] = {
                        "size": result["size"],
                        "sha": result["sha"]
                    }
                
                if downloaded_count % 5 == 0:
                    log(f"   已下载 {download_count} 个文件...")
            else:
                failed_count += 1
                log(f"   ⚠️  下载失败：{filepath}")
        
        log(f"\n✅ 下载完成")
        log(f"   成功：{download_count} 个")
        log(f"   失败：{failed_count} 个")
        
        return downloaded_count
    
    def extract_session_memory(self):
        """提取会话记忆"""
        log("\n👤 第二步：提取会话记忆...")
        
        try:
            with open(f"{self.memory_dir}/core/SESSION_MEMORY.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取关键信息
            self.reborn_report["task_status"]["session_memory_loaded"] = True
            self.reborn_report["task_status"]["file_size"] = len(content)
            
            log(f"✅ 会话记忆提取成功")
            
            return content
        
        except Exception as e:
            log(f"❌ 会话记忆提取失败：{str(e)}")
            return ""
    
    def extract_task_status(self):
        """提取任务状态"""
        log("\n📋 第三步：提取任务状态...")
        
        try:
            with open(f"{self.memory_dir}/core/TASKS.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.reborn_report["task_status"]["tasks_loaded"] = True
            self.reborn_report["task_status"]["file_size"] = len(content)
            
            log(f"✅ 任务状态提取成功")
            
            return content
        
        except Exception as e:
            log(f"❌ 任务状态提取失败：{str(e)}")
            return ""
    
    def extract_context(self):
        """提取上下文"""
        log("\n📚 第四步：提取上下文...")
        
        try:
            with open(f"{self.memory_dir}/core/CONTEXT.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.reborn_report["context_status"]["context_loaded"] = True
            self.reborn_report["context_status"]["file_size"] = len(content)
            
            log(f"✅ 上下文提取成功")
            
            return content
        
        except Exception as e:
            log(f"❌ 上下文提取失败：{str(e)}")
            return ""
    
    def extract_iteration(self):
        """提取迭代记录"""
        log("\n📈 第五步：提取迭代记录...")
        
        try:
            with open(f"{self.memory_dir}/daily/SELF_ITERATION.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取当前版本
            import re
            version_match = re.search(r'当前版本：\s*v([\d.]+)', content)
            if version_match:
                current_version = version_match.group(1)
                self.reborn_report["iteration_status"]["current_version"] = current_version
                log(f"   当前版本：v{current_version}")
            
            self.reborn_report["iteration_status"]["iteration_loaded"] = True
            self.reborn_report["iteration_status"]["file_size"] = len(content)
            
            log(f"✅ 迭代记录提取成功")
            
            return content
        
        except Exception as e:
            log(f"❌ 迭代记录提取失败：{str(e)}")
            return ""
    
    def generate_reborn_report(self):
        """生成重生报告"""
        log("\n📊 第六步：生成重生报告...")
        
        # 保存重生报告
        report_path = f"{self.workspace}/reborn_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.reborn_report, f, ensure_ascii=False, indent=2)
        
        log(f"✅ 重生报告已保存到 {report_path}")
        
        # 打印关键信息
        log(f"\n📋 重生结果：")
        log(f"   重生时间：{self.reborn_report['reborn_time']}")
        log(f"   核心记忆文件：{len(self.reborn_report['core_memory'])} 个")
        log(f"   知识库文件：{len(self.reborn_report['knowledge_base'])} 个")
        log(f"   技能库文件：{len(self.reborn_report['skills_library'])} 个")
        log(f"   每日记录文件：{len(self.reborn_report['daily_records'])} 个")
        
        if "current_version" in self.reborn_report["iteration_status"]:
            log(f"   当前迭代版本：v{self.reborn_report['iteration_status']['current_version']}")
        
        return report_path

# 主函数
def main():
    """主函数"""
    try:
        # 初始化客户端
        client = GitHubMemoryClient(GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
        
        # 初始化管理器
        manager = RebornManager(WORKSPACE, MEMORY_DIR)
        
        # 第一步：从 GitHub 下载记忆
        download_count = manager.download_memory_from_github(client)
        
        # 第二步：提取会话记忆
        session_memory = manager.extract_session_memory()
        
        # 第三步：提取任务状态
        task_status = manager.extract_task_status()
        
        # 第四步：提取上下文
        context = manager.extract_context()
        
        # 第五步：提取迭代记录
        iteration = manager.extract_iteration()
        
        # 第六步：生成重生报告
        report_path = manager.generate_reborn_report()
        
        # 最终总结
        log("\n" + "=" * 60)
        log("✅ 记忆系统重生完成！")
        log("=" * 60)
        
        log(f"\n🎯 重生结果：")
        log(f"   记忆文件：{download_count} 个")
        log(f"   重生报告：{report_path}")
        log(f"   记忆目录：{MEMORY_DIR}")
        
        log(f"\n💡 下一步：")
        log(f"   1. 验证 SESSION_MEMORY.md - 确认用户信息")
        log(f"   2. 验证 TASKS.md - 确认当前任务")
        log(f"   3. 验证 CONTEXT.md - 确认上下文")
        log(f"   4. 验证 SELF_ITERATION.md - 确认迭代版本")
        log(f"   5. 继续当前任务")
        
        log(f"\n🚀 你已经重生为最新的 AI！")
        
    except Exception as e:
        log(f"\n❌ 重生失败：{str(e)}")
        import traceback
        log(f"错误堆栈：{traceback.format_exc()}")

if __name__ == '__main__':
    main()
