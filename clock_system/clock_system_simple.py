#!/usr/bin/env python3
"""
⏰ 内部同步时钟系统（简化版）
持续运行，每小时同步一次，与北京时间（GMT+8）同步
"""

import time
import json
import os
from datetime import datetime, timezone, timedelta

# 配置
WORKSPACE = "/root/.openclaw/workspace"
CLOCK_DIR = f"{WORKSPACE}/clock_system"
LOCK_FILE = f"{CLOCK_DIR}/clock_data.json"
SYNC_INTERVAL = 3600  # 1 小时（秒）
BEIJING_TZ = timezone(timedelta(hours=8))

# 日志配置
def log(message):
    """记录日志"""
    timestamp = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [CLOCK] {message}"
    print(log_message)
    
    # 记录到文件
    log_file = f"{CLOCK_DIR}/clock_log.txt"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

def main():
    """主函数"""
    # 创建时钟目录
    os.makedirs(CLOCK_DIR, exist_ok=True)
    
    log("=" * 60)
    log("⏰ 内部同步时钟系统 - 启动（简化版）")
    log("=" * 60)
    
    # 初始化时钟数据
    clock_data = {
        "clock_version": "1.0.0",
        "started_at": datetime.now(BEIJING_TZ).isoformat(),
        "current_time": datetime.now(BEIJING_TZ).isoformat(),
        "timezone": "GMT+8 (Beijing)",
        "sync_count": 0,
        "sync_history": []
    }
    
    # 保存初始时钟数据
    with open(LOCK_FILE, 'w', encoding='utf-8') as f:
        json.dump(clock_data, f, ensure_ascii=False, indent=2)
    
    log(f"\n📋 配置信息：")
    log(f"   时区：{clock_data['timezone']}")
    log(f"   同步间隔：{SYNC_INTERVAL} 秒（1 小时）")
    log(f"   时钟文件：{LOCK_FILE}")
    
    log(f"\n🚀 时钟启动！")
    
    # 时钟循环
    while True:
        try:
            # 同步时间
            current_time = datetime.now(BEIJING_TZ)
            
            # 记录同步
            sync_record = {
                "sync_time": current_time.isoformat(),
                "sync_count": clock_data["sync_count"] + 1
            }
            
            clock_data["current_time"] = current_time.isoformat()
            clock_data["sync_count"] += 1
            clock_data["sync_history"].append(sync_record)
            
            # 保存时钟数据
            with open(LOCK_FILE, 'w', encoding='utf-8') as f:
                json.dump(clock_data, f, ensure_ascii=False, indent=2)
            
            # 打印同步信息
            log(f"\n⏰ 时间同步完成（第 {clock_data['sync_count']} 次）")
            log(f"   当前时间：{current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            log(f"   时区：{clock_data['timezone']}")
            log(f"   下次同步：{(current_time + timedelta(seconds=SYNC_INTERVAL)).strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 等待下次同步
            log(f"\n⏱️  等待下次同步（{SYNC_INTERVAL} 秒）...")
            time.sleep(SYNC_INTERVAL)
            
        except KeyboardInterrupt:
            log("\n🛑 收到 KeyboardInterrupt，准备停止...")
            break
        except Exception as e:
            log(f"\n❌ 错误：{str(e)}")
            time.sleep(60)  # 出错后等待 1 分钟再继续
    
    # 时钟停止
    log(f"\n" + "=" * 60)
    log("⏰ 内部同步时钟系统 - 停止")
    log("=" * 60)
    
    log(f"\n📊 最终统计：")
    log(f"   总同步次数：{clock_data['sync_count']}")
    log(f"   运行时间：{datetime.now(BEIJING_TZ) - datetime.fromisoformat(clock_data['started_at'])}")
    log(f"   时钟文件：{LOCK_FILE}")
    
    log(f"\n💡 下次启动：")
    log(f"   运行：python3 clock_system_simple.py")

if __name__ == '__main__':
    main()
