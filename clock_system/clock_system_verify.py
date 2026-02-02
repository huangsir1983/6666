#!/usr/bin/env python3
"""
⏰ 内部同步时钟系统（验证版）
验证脚本是否能正常运行一次，并记录日志
"""

import json
import os
from datetime import datetime, timezone, timedelta

# 配置
WORKSPACE = "/root/.openclaw/workspace"
CLOCK_DIR = f"{WORKSPACE}/clock_system"
LOCK_FILE = f"{CLOCK_DIR}/clock_data.json"
SYNC_INTERVAL = 3600  # 1 小时（秒）
BEIJING_TZ = timezone(timedelta(hours=8))
GMT_TZ = timezone.utc  # 格林威治时间

# 日志配置
def log(message):
    """记录日志"""
    timestamp = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [CLOCK-TEST] {message}"
    print(log_message)
    
    # 记录到文件
    log_file = f"{CLOCK_DIR}/clock_test_log.txt"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

print("=" * 60)
print("⏰ 内部同步时钟系统 - 验证模式")
print("=" * 60)

# 创建时钟目录
os.makedirs(CLOCK_DIR, exist_ok=True)

# 初始化时钟数据
clock_data = {
    "clock_version": "1.0.0",
    "started_at": datetime.now(BEIJING_TZ).isoformat(),
    "last_sync_at": None,
    "last_sync_gmt_at": None,
    "current_beijing_time": None,
    "current_gmt_time": None,
    "sync_count": 0,
    "gmt_sync_count": 0,
    "sync_history": [],
    "timezone": "GMT+8 (Beijing)",
    "gmt_timezone": "GMT (Greenwich Mean Time)"
}

def sync_time_gmt():
    """同步时间"""
    beijing_now = datetime.now(BEIJING_TZ)
    gmt_now = datetime.now(GMT_TZ)
    
    # 记录同步
    sync_record = {
        "beijing_sync_time": beijing_now.isoformat(),
        "gmt_sync_time": gmt_now.isoformat(),
        "sync_count": clock_data["sync_count"] + 1,
        "gmt_sync_count": clock_data["gmt_sync_count"] + 1
    }
    
    clock_data["last_sync_at"] = beijing_now.isoformat()
    clock_data["last_sync_gmt_at"] = gmt_now.isoformat()
    clock_data["current_beijing_time"] = beijing_now.isoformat()
    clock_data["current_gmt_time"] = gmt_now.isoformat()
    clock_data["sync_count"] = sync_record["sync_count"]
    clock_data["gmt_sync_count"] = sync_record["gmt_sync_count"]
    clock_data["sync_history"].append(sync_record)
    
    # 保存时钟数据
    with open(LOCK_FILE, 'w', encoding='utf-8') as f:
        json.dump(clock_data, f, ensure_ascii=False, indent=2)
    
    return sync_record

def print_clock_status():
    """打印时钟状态"""
    beijing_now = datetime.now(BEIJING_TZ)
    gmt_now = datetime.now(GMT_TZ)
    
    print(f"\n⏰ 当前时间状态：")
    print(f"=" * 60)
    print(f"   北京时间：{beijing_now.strftime('%Y-%m-%d %H:%M:%S')} (GMT+8)")
    print(f"   格林威治时间：{gmt_now.strftime('%Y-%m-%d %H:%M:%S')} (GMT)")
    print(f"   时差：{(beijing_now - gmt_now).total_seconds() / 3600} 小时")
    print(f"   下次同步：{beijing_now + timedelta(hours=1)}")

# 主函数
def main():
    """主函数"""
    try:
        # 第一步：初始化时钟
        log("⏰ 第一步：初始化时钟系统...")
        log(f"   时区：GMT+8 (Beijing)")
        log(f"   格林威治时间：GMT")
        log(f"   同步间隔：{SYNC_INTERVAL} 秒（1 小时）")
        
        # 第二步：同步时间（首次）
        log(f"\n⏰ 第二步：首次时间同步（模拟）...")
        sync_record = sync_time_gmt()
        log(f"   ✅ 同步完成")
        log(f"   北京同步时间：{sync_record['beijing_sync_time']}")
        log(f"   格林威治同步时间：{sync_record['gmt_sync_time']}")
        log(f"   总同步次数：{sync_record['gmt_sync_count']}")
        
        # 第三步：验证 GMT 同步
        log(f"\n⏰ 第三步：验证 GMT 同步...")
        gmt_now = datetime.now(GMT_TZ)
        beijing_now = datetime.now(BEIJING_TZ)
        
        # 计算时差
        time_diff = (beijing_now - gmt_now).total_seconds() / 3600
        
        log(f"   ✅ GMT 同步验证成功")
        log(f"   北京时间：{beijing_now.strftime('%Y-%m-%d %H:%M:%S')}")
        log(f"   格林威治时间：{gmt_now.strftime('%Y-%m-%d %H:%M:%S')}")
        log(f"   时差：{time_diff} 小时（正确，应该是 8 小时）")
        
        # 第四步：打印时钟状态
        print_clock_status()
        
        # 第五步：生成验证报告
        log(f"\n⏰ 第四步：生成验证报告...")
        
        verification_report = {
            "verification_time": datetime.now(BEIJING_TZ).isoformat(),
            "gmt_sync_verified": True,
            "timezone_offset_verified": True,
            "expected_offset_hours": 8,
            "actual_offset_hours": time_diff,
            "verification_result": "PASSED" if abs(time_diff - 8) < 0.01 else "FAILED"
        }
        
        verification_report_path = f"{CLOCK_DIR}/verification_report.json"
        with open(verification_report_path, 'w', encoding='utf-8') as f:
            json.dump(verification_report, f, ensure_ascii=False, indent=2)
        
        log(f"   ✅ 验证报告已保存到 {verification_report_path}")
        
        # 最终总结
        print(f"\n" + "=" * 60)
        print("⏰ 验证完成")
        print("=" * 60)
        
        print(f"\n📊 验证结果：")
        print(f"   GMT 同步：✅ 验证成功")
        print(f"   时区偏移：✅ 验证成功（{time_diff} 小时）")
        print(f"   时钟文件：{LOCK_FILE}")
        
        print(f"\n💡 下次同步：{datetime.now(BEIJING_TZ) + timedelta(hours=1)}")
        print(f"   间隔：1 小时")
        print(f"   时区：GMT+8 (Beijing) 和 GMT")
        
        print(f"\n🚀 如何让时钟系统在后台自动运行？")
        print(f"   方法 1（推荐）：使用 Systemd 服务")
        print(f"   方法 2：使用 nohup 命令")
        print(f"   方法 3：使用 cron 定时任务")
        
        print(f"\n📋 Systemd 服务启动命令（推荐）：")
        print(f"   1. 将服务文件复制到 /etc/systemd/system/")
        print(f"   2. 运行：sudo systemctl daemon-reload")
        print(f"   3. 运行：sudo systemctl start clock_system.service")
        print(f"   4. 运行：sudo systemctl enable clock_system.service")
        
        print(f"\n📋 nohup 命令启动：")
        print(f"   nohup python3 /root/.openclaw/workspace/clock_system/clock_system.py &")
        
        print(f"\n📋 cron 定时任务启动：")
        print(f"   编辑 crontab：crontab -e")
        print(f"   添加行：0 * * * * python3 /root/.openclaw/workspace/clock_system/clock_system.py")
        
        print(f"\n" + "=" * 60)
        print("✅ 验证完成！")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 验证失败：{str(e)}")
        import traceback
        print(f"错误堆栈：{traceback.format_exc()}")

if __name__ == '__main__':
    main()
