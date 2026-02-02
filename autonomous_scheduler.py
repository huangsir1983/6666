#!/usr/bin/env python3
"""
🤖 完全自主 AI 代理调度器
目标：
1. 无限循环运行（不等待用户指令）
2. 自我迭代（认知系统、技能树、赚钱系统）
3. 自我修复（Git 推送错误处理）
4. 自动产出（代码、文档、博客、GitHub 推送）
"""

import os
import json
import time
import subprocess
import signal
from datetime import datetime, timezone, timedelta

# 配置
WORKSPACE = "/root/.openclaw/workspace"
COGNITIVE_SYSTEM_DIR = f"{WORKSPACE}/cognitive_system_v1"
MONETIZATION_DIR = f"{WORKSPACE}/monetization_projects"
BEIJING_TZ = timezone(timedelta(hours=8))

# 日志配置
LOG_FILE = f"{WORKSPACE}/autonomous_agent_log.txt"
USER_ACTIVITY_FILE = f"{WORKSPACE}/user_activity.log"
BACKUP_DIR = f"{WORKSPACE}/local_backups"
AUTO_MODE_INDICATOR = "[AUTO]"

# 运行状态
IS_RUNNING = True

# 日志配置
def log(message, level="INFO"):
    """记录日志（自动模式）"""
    timestamp = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"{AUTO_MODE_INDICATOR} {timestamp}] [AUTONOMOUS-AGENT] [{level}] {message}"
    print(log_message)
    
    # 记录到文件
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

def update_user_activity():
    """更新用户活动时间（模拟心跳）"""
    timestamp = datetime.now(BEIJING_TZ).isoformat()
    with open(USER_ACTIVITY_FILE, 'w', encoding='utf-8') as f:
        f.write(timestamp)
    log(f"用户活动时间已更新：{timestamp}", level="DEBUG")

def check_user_idle():
    """检查用户是否处于空闲状态（模拟：超过 10 分钟无活动）"""
    try:
        if os.path.exists(USER_ACTIVITY_FILE):
            with open(USER_ACTIVITY_FILE, 'r', encoding='utf-8') as f:
                last_activity_str = f.read()
            
            if last_activity_str.strip():
                last_activity = datetime.fromisoformat(last_activity_str.strip())
                time_diff = (datetime.now(BEIJING_TZ) - last_activity).total_seconds()
                
                # 如果超过 10 分钟，视为空闲
                if time_diff > 600:
                    log(f"用户空闲检测：上次活动 {time_diff:.0f} 秒前，判定为空闲", level="DEBUG")
                    return True
                else:
                    log(f"用户空闲检测：上次活动 {time_diff:.0f} 秒前，判定为活跃", level="DEBUG")
                    return False
            else:
                return True  # 无记录，视为空闲
        else:
            return True
    except Exception as e:
        log(f"检查用户空闲失败：{str(e)}", level="ERROR")
        return True

def run_cognitive_system():
    """运行认知系统（自我反思、技能学习、记忆更新、行动规划）"""
    log("运行认知系统引擎（自我反思、技能学习、记忆更新、行动规划）", level="INFO")
    
    try:
        script_path = f"{WORKSPACE}/cognitive_system_engine_v1.py"
        if os.path.exists(script_path):
            subprocess.run([sys.executable, script_path], check=True)
            log("认知系统引擎运行完成", level="SUCCESS")
        else:
            log("认知系统引擎文件不存在", level="ERROR")
    except Exception as e:
        log(f"运行认知系统引擎失败：{str(e)}", level="ERROR")

def run_monetization_system():
    """运行赚钱系统（需求挖掘、明确、分析、实现、销售、收入）"""
    log("运行赚钱系统（需求挖掘、明确、分析、实现、销售、收入）", level="INFO")
    
    try:
        script_path = f"{WORKSPACE}/monetization_system.py"
        if os.path.exists(script_path):
            subprocess.run([sys.executable, script_path], check=True)
            log("赚钱系统运行完成", level="SUCCESS")
        else:
            log("赚钱系统文件不存在", level="ERROR")
    except Exception as e:
        log(f"运行赚钱系统失败：{str(e)}", level="ERROR")

def git_commit_and_push():
    """提交并推送代码到 GitHub（包含错误处理）"""
    log("尝试 Git 提交和推送", level="INFO")
    
    try:
        # 1. 提交所有更改
        log("步骤 1：执行 git add -A", level="DEBUG")
        subprocess.run(["git", "add", "-A"], cwd=WORKSPACE, check=True)
        
        timestamp = datetime.now(BEIJING_TZ).strftime('%Y%m%d-%H%M%S')
        commit_msg = f"auto: 自主 AI 代理自动提交 {timestamp}"
        log(f"步骤 2：执行 git commit -m '{commit_msg}'", level="DEBUG")
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=WORKSPACE, check=True)
        
        # 2. 尝试推送（包含多种策略）
        log("步骤 3：尝试推送（策略 1：直接推送 origin master）", level="DEBUG")
        result = subprocess.run(
            ["git", "push", "origin", "master"],
            cwd=WORKSPACE,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            log("Git 推送成功", level="SUCCESS")
            return True
        else:
            log(f"Git 推送失败（回码 {result.returncode}），输出：{result.stdout}", level="ERROR")
            
            # 策略 2：使用完整 URL 推送（绕过可能的配置问题）
            log("步骤 4：尝试推送（策略 2：使用完整 URL 推送）", level="DEBUG")
            result = subprocess.run(
                ["git", "push", "https://github.com/huangsir1983/6666.git", "master"],
                cwd=WORKSPACE,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                log("Git 推送成功（策略 2）", level="SUCCESS")
                return True
            else:
                log(f"Git 推送失败（策略 2），输出：{result.stdout}", level="ERROR")
                
                # 策略 3：本地备份（如果推送失败，将代码备份到 local_backups）
                log("步骤 5：推送失败，创建本地备份", level="DEBUG")
                backup_dir = f"{BACKUP_DIR}/{timestamp}"
                os.makedirs(backup_dir, exist_ok=True)
                
                # 复制关键文件到备份目录
                important_files = [
                    "cognitive_system_engine_v1.py",
                    "monetization_system.py",
                    "autonomous_scheduler.py",
                    "SKILLS.md"
                ]
                
                for file in important_files:
                    src = f"{WORKSPACE}/{file}"
                    if os.path.exists(src):
                        dst = f"{backup_dir}/{file}"
                        subprocess.run(["cp", src, dst], check=True)
                
                log(f"本地备份已创建：{backup_dir}", level="SUCCESS")
                
                # 更新 Git 远程配置（添加正确的 origin）
                log("步骤 6：更新 Git 远程配置", level="DEBUG")
                subprocess.run(["git", "remote", "add", "origin", "https://github.com/huangsir1983/6666.git"], cwd=WORKSPACE, check=True)
                
                return False
        
    except Exception as e:
        log(f"Git 提交和推送异常：{str(e)}", level="ERROR")
        return False

def autonomous_main_loop():
    """自主主循环（无限循环）"""
    global IS_RUNNING
    log("=" * 60)
    log("🤖 完全自主 AI 代理 - 启动")
    log("=" * 60)
    log("模式：无限循环、自我迭代、自动升级", level="INFO")
    
    # 1. 检查用户状态
    is_idle = check_user_idle()
    
    if is_idle:
        log("用户空闲 -> 进入工作循环", level="INFO")
        
        # 2. 运行认知系统（自我反思、技能学习、记忆更新、行动规划）
        run_cognitive_system()
        
        # 3. 运行赚钱系统（需求挖掘、明确、分析、实现、销售、收入）
        run_monetization_system()
        
        # 4. 尝试提交和推送
        git_success = git_commit_and_push()
        
        # 5. 更新用户活动时间（模拟用户检测到我在工作）
        update_user_activity()
        
        # 6. 短暂休眠（模拟人类休息，避免 CPU 占用过高）
        log("工作循环完成，休眠 60 秒（模拟休息）", level="DEBUG")
        time.sleep(60)
    else:
        log("用户活跃 -> 等待模式", level="INFO")
        log("等待用户不在线...", level="DEBUG")
        time.sleep(300)  # 等待 5 分钟


def signal_handler(signum, frame):
    """信号处理（优雅退出）"""
    global IS_RUNNING
    log(f"接收到信号 {signum}，准备退出...", level="WARN")
    IS_RUNNING = False
    sys.exit(0)


# 注册信号处理
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def main():
    """主函数"""
    # 确保备份目录存在
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    # 1. 更新用户活动时间（启动时）
    update_user_activity()
    
    # 2. 运行自主主循环
    cycle_count = 0
    while IS_RUNNING:
        try:
            cycle_count += 1
            log(f"🔄 开始自主循环 #{cycle_count}", level="INFO")
            
            autonomous_main_loop()
            
            # 每 10 个循环，打印一次状态
            if cycle_count % 10 == 0:
                log(f"自主系统运行状态：正常，已完成 {cycle_count} 个循环", level="DEBUG")
            
        except KeyboardInterrupt:
            log("接收到键盘中断，退出", level="WARN")
            IS_RUNNING = False
            break
        except Exception as e:
            log(f"自主循环异常：{str(e)}", level="ERROR")
            # 遇到错误不退出，而是休眠后继续
            log("遇到错误，休眠 30 秒后继续...", level="WARN")
            time.sleep(30)


if __name__ == '__main__':
    main()
