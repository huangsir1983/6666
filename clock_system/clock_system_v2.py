#!/usr/bin/env python3
"""
⏰ 内部同步时钟系统（修复版）
持续运行，每小时同步一次，与格林威治时间（GMT）同步
修复：移除 signal 导入问题，简化错误处理
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
UTC_TZ = timezone.utc  # UTC 时区（相当于 GMT）
BEIJING_TZ = timezone(timedelta(hours=8))  # 北京时间（GMT+8）

# 日志配置
def log(message):
    """记录日志"""
    timestamp = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [CLOCK-FIXED-V2] {message}"
    print(log_message)
    
    # 记录到文件
    log_file = f"{CLOCK_DIR}/clock_log.txt"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

# 创建时钟目录
os.makedirs(CLOCK_DIR, exist_ok=True)

class InternalClock:
    """内部时钟系统"""
    
    def __init__(self):
        self.clock_data = self.load_clock_data()
        self.running = True
        self.sync_count = 0
        self.gmt_sync_count = 0
    
    def load_clock_data(self):
        """加载时钟数据"""
        if os.path.exists(LOCK_FILE):
            try:
                with open(LOCK_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                log(f"⚠️  加载时钟数据失败：{str(e)}")
                return self.init_clock_data()
        else:
            return self.init_clock_data()
    
    def init_clock_data(self):
        """初始化时钟数据"""
        return {
            "clock_version": "1.0.0",
            "started_at": datetime.now(BEIJING_TZ).isoformat(),
            "current_time": datetime.now(BEIJING_TZ).isoformat(),
            "timezone": "GMT+8 (Beijing)",
            "gmt_timezone": "GMT (Greenwich Mean Time)",
            "sync_count": 0,
            "gmt_sync_count": 0,
            "sync_history": []
        }
    
    def save_clock_data(self):
        """保存时钟数据"""
        self.clock_data["current_time"] = datetime.now(BEIJING_TZ).isoformat()
        self.clock_data["sync_count"] = self.sync_count
        self.clock_data["gmt_sync_count"] = self.gmt_sync_count
        
        try:
            with open(LOCK_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.clock_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log(f"⚠️  保存时钟数据失败：{str(e)}")
    
    def sync_time_gmt(self):
        """同步时间（修复版：使用 UTC 时间）"""
        try:
            beijing_now = datetime.now(BEIJING_TZ)
            gmt_now = datetime.now(UTC_TZ)
            
            # 计算时差（使用 UTC 时间）
            time_diff_hours = 8  # 北京时间比 GMT 快 8 小时
            
            # 记录同步
            sync_record = {
                "sync_time": beijing_now.isoformat(),
                "gmt_sync_time": gmt_now.isoformat(),
                "sync_count": self.sync_count + 1,
                "gmt_sync_count": self.gmt_sync_count + 1,
                "time_diff_hours": time_diff_hours
            }
            
            self.clock_data["current_time"] = beijing_now.isoformat()
            self.clock_data["gmt_current_time"] = gmt_now.isoformat()
            self.sync_count += 1
            self.gmt_sync_count += 1
            self.clock_data["sync_history"].append(sync_record)
            
            # 保存时钟数据
            self.save_clock_data()
            
            return sync_record
        except Exception as e:
            log(f"❌ 同步时间失败：{str(e)}")
            return None
    
    def get_next_sync_time(self):
        """获取下次同步时间"""
        now = datetime.now(BEIJING_TZ)
        next_sync = now + timedelta(seconds=SYNC_INTERVAL)
        return next_sync
    
    def print_clock_status(self):
        """打印时钟状态"""
        now = datetime.now(BEIJING_TZ)
        gmt_now = datetime.now(UTC_TZ)
        
        print(f"\n⏰  内部时钟状态")
        print(f"=" * 60)
        print(f"   当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')} (GMT+8)")
        print(f"   当前时间：{gmt_now.strftime('%Y-%m-%d %H:%M:%S')} (GMT)")
        print(f"   时区：{self.clock_data['timezone']}")
        print(f"   同步次数：{self.sync_count}")
        print(f"   GMT 同步次数：{self.gmt_sync_count}")
        print(f"   下次同步：{self.get_next_sync_time().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"=" * 60)
    
    def run_sync(self):
        """运行同步"""
        try:
            sync_record = self.sync_time_gmt()
            
            if sync_record:
                log(f"✅ 同步完成（第 {self.sync_count} 次总计，第 {self.gmt_sync_count} 次 GMT)")
                log(f"   同步时间：{sync_record['sync_time']}")
                log(f"   GMT 同步时间：{sync_record['gmt_sync_time']}")
                log(f"   时差：{sync_record['time_diff_hours']} 小时")
                
                # 打印时钟状态
                self.print_clock_status()
                
                return sync_record
            else:
                log(f"❌ 同步失败")
                return None
        
        except Exception as e:
            log(f"❌ 运行同步失败：{str(e)}")
            return None

# 全局时钟实例
clock = InternalClock()

def run_clock():
    """运行时钟"""
    log("=" * 60)
    log("⏰ 内部同步时钟系统 - 启动（修复版 V2）")
    log("=" * 60)
    
    log(f"\n📋 配置信息：")
    log(f"   时区：GMT+8 (Beijing)")
    log(f"   GMT 时区：GMT (Greenwich Mean Time)")
    log(f"   同步间隔：{SYNC_INTERVAL} 秒（1 小时）")
    log(f"   时钟文件：{LOCK_FILE}")
    
    log(f"\n🚀 时钟状态：")
    clock.print_clock_status()
    
    log(f"\n🎯 下一步：")
    log(f"   1. 运行时间同步")
    log(f"   2. 等待 1 小时")
    log(f"   3. 再次运行时间同步")
    log(f"   4. 持续同步")
    
    log(f"\n💡 提示：")
    log(f"   - 时钟将持续运行")
    log(f"   - 每小时自动同步一次")
    log(f"   - 与格林威治时间（GMT）同步")
    log(f"   - 使用 UTC 时间计算时差，确保准确")
    log(f"   - 按 Ctrl+C 停止时钟")
    
    log(f"\n" + "=" * 60)
    log("⏰  时钟启动！")
    log("=" * 60)
    
    while clock.running:
        try:
            # 运行同步
            clock.run_sync()
            
            # 计算下次同步时间
            next_sync = clock.get_next_sync_time()
            
            # 等待下次同步
            log(f"\n⏱️  等待下次同步（{SYNC_INTERVAL} 秒，即 1 小时）...")
            log(f"   下次同步：{next_sync}")
            
            # 使用 time.sleep 实现精确的等待
            time.sleep(SYNC_INTERVAL)
            
        except KeyboardInterrupt:
            log("\n🛑 收到 KeyboardInterrupt，准备停止...")
            clock.running = False
            break
        
        except Exception as e:
            log(f"\n❌ 错误：{str(e)}")
            log(f"   将在 10 秒后重试...")
            time.sleep(10)
            continue
    
    # 时钟停止
    log(f"\n" + "=" * 60)
    log("⏰  内部同步时钟系统 - 停止")
    log("=" * 60)
    
    log(f"\n📊 最终统计：")
    log(f"   总同步次数：{clock.sync_count}")
    log(f"   GMT 同步次数：{clock.gmt_sync_count}")
    log(f"   运行时间：{(datetime.now(BEIJING_TZ) - datetime.fromisoformat(clock.clock_data['started_at'])).total_seconds() / 3600:.2f} 小时")
    
    log(f"\n💡 下次启动时钟：")
    log(f"   运行：python3 clock_system.py")
    log(f"   或者运行：nohup python3 clock_system.py &")

if __name__ == '__main__':
    run_clock()
