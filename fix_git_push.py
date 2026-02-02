#!/usr/bin/env python3
"""
🔧 Git 推送彻底修复器
目标：1. 移除现有远程仓库，2. 添加正确的远程仓库，3. 验证配置，4. 推送
"""

import subprocess
import sys
from datetime import datetime, timezone, timedelta

# 配置
WORKSPACE = "/root/.openclaw/workspace"
BEIJING_TZ = timezone(timedelta(hours=8))

# 正确的 GitHub 仓库 URL
CORRECT_GIT_URL = "https://github.com/huangsir1983/6666.git"

# 日志配置
def log(message):
    """记录日志"""
    timestamp = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [GIT-PUSH-FIX] {message}"
    print(log_message)


def remove_remote():
    """移除现有的 origin 远程仓库"""
    log("\n[步骤 1] 移除现有的 origin 远程仓库...")
    try:
        # 先尝试移除
        subprocess.run(["git", "remote", "remove", "origin"], cwd=WORKSPACE, capture_output=True, text=True)
        log("   ✅ 移除 origin 成功")
        return True
    except Exception as e:
        log(f"   ❌ 移除 origin 失败：{str(e)}")
        return False


def add_correct_remote():
    """添加正确的远程仓库"""
    log(f"\n[步骤 2] 添加正确的远程仓库 (URL：{CORRECT_GIT_URL})...")
    try:
        # 添加远程仓库 origin，使用正确的 URL
        result = subprocess.run(
            ["git", "remote", "add", "origin", CORRECT_GIT_URL],
            cwd=WORKSPACE,
            capture_output=True,
            text=True
        )
        log(f"   结果：{result.stdout}")
        log("   ✅ 添加 origin 成功")
        return True
    except Exception as e:
        log(f"   ❌ 添加 origin 失败：{str(e)}")
        return False


def verify_remote():
    """验证远程仓库配置"""
    log("\n[步骤 3] 验证远程仓库配置...")
    try:
        # 查看所有远程仓库
        result = subprocess.run(["git", "remote", "-v"], cwd=WORKSPACE, capture_output=True, text=True)
        log(f"   远程仓库列表：\n{result.stdout}")
        
        # 检查 origin 是否存在且正确
        if f"origin\t{CORRECT_GIT_URL}" in result.stdout:
            log("   ✅ 远程仓库 origin 配置正确")
            return True
        else:
            log(f"   ❌ 远程仓库 origin 配置不正确")
            return False
    except Exception as e:
        log(f"   ❌ 验证远程仓库失败：{str(e)}")
        return False


def push_to_remote():
    """推送到远程仓库"""
    log("\n[步骤 4] 推送到 origin...")
    try:
        # 设置上游（如果需要）
        subprocess.run(["git", "push", "--set-upstream", "origin", "master"], cwd=WORKSPACE, capture_output=True, text=True)
        
        # 推送
        result = subprocess.run(["git", "push", "origin", "master"], cwd=WORKSPACE, capture_output=True, text=True)
        
        log(f"   推送结果：\n{result.stdout}")
        
        # 检查错误
        if "error" in result.stdout.lower() or result.returncode != 0:
            log(f"   ❌ 推送可能失败")
            log(f"   返回码：{result.returncode}")
            return False
        else:
            log("   ✅ 推送成功")
            return True
    except Exception as e:
        log(f"   ❌ 推送失败：{str(e)}")
        return False


def main():
    """主函数"""
    log("=" * 60)
    log("🔧 Git 推送彻底修复 - 开始")
    log("=" * 60)
    
    # 1. 移除现有远程
    if not remove_remote():
        log("   ⚠️  移除现有远程失败，继续下一步...")
    
    # 2. 添加正确的远程
    if not add_correct_remote():
        log("   ❌ 添加正确的远程失败，终止")
        sys.exit(1)
    
    # 3. 验证配置
    if not verify_remote():
        log("   ❌ 验证配置失败，终止")
        sys.exit(1)
    
    # 4. 推送
    if not push_to_remote():
        log("   ❌ 推送失败")
        sys.exit(1)
    
    # 最终总结
    log(f"\n" + "=" * 60)
    log("✅ Git 推送彻底修复 - 完成")
    log("=" * 60)
    
    log(f"\n💡 下一步：")
    log(f"   1. 检查 GitHub 仓库：https://github.com/huangsir1983/6666")
    log(f"   2. 运行认知系统引擎（cognitive_system_engine_v1.py）")
    log(f"   3. 开始 PDCA 循环（计划 -> 执行 -> 检查 -> 处理）")
    log(f"   4. 不断产出好的东西，发帖、发程序")


if __name__ == '__main__':
    main()
