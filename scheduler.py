#!/usr/bin/env python3
"""
实时任务调度器
整点自动汇报进度
"""

import time
import json
from datetime import datetime
import subprocess
import requests

PROGRESS_FILE = '/root/.openclaw/workspace/progress.json'

def load_progress():
    try:
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_progress(data):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_status(service, status):
    data = load_progress()
    data[service] = {
        'status': status,
        'timestamp': datetime.now().isoformat()
    }
    save_progress(data)

def check_services():
    """检查所有服务状态"""
    results = {}

    # 检查代理服务
    try:
        resp = requests.get('http://localhost:8080/health', timeout=5)
        results['proxy'] = {
            'status': 'running' if resp.status_code == 200 else 'error',
            'response': resp.json()
        }
    except:
        results['proxy'] = {'status': 'stopped', 'error': 'Connection failed'}

    # 检查 HTTP 服务器
    try:
        resp = requests.get('http://localhost:8081/', timeout=5)
        results['http_server'] = {
            'status': 'running' if resp.status_code == 200 else 'error'
        }
    except:
        results['http_server'] = {'status': 'stopped', 'error': 'Connection failed'}

    return results

def generate_report():
    """生成汇报报告"""
    services = check_services()

    report = f"""
# 🎮 创意开发整点汇报

**时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📊 服务状态

### 代理服务 (端口 8080)
- **状态：** {'✅ 运行中' if services['proxy'].get('status') == 'running' else '❌ 已停止'}
- **响应：** {json.dumps(services['proxy'], ensure_ascii=False, indent=2)}

### HTTP 服务器 (端口 8081)
- **状态：** {'✅ 运行中' if services['http_server'].get('status') == 'running' else '❌ 已停止'}

---

## 📁 已创建文件

1. **GLM 智能助手** - `/root/.openclaw/workspace/glm_chat.html`
2. **AI 故事生成器** - `/root/.openclaw/workspace/ai_story.html`
3. **冒泡排序可视化** - `/root/.openclaw/workspace/bubble_sort.html`
4. **Claude Code 代理** - `/root/.openclaw/workspace/proxy_server_v2.py`

---

## 💡 当前想法

- [ ] 完成 Claude Code 代理集成
- [ ] 添加 AI 驱动的代码编辑器
- [ ] 创建实时协作白板
- [ ] 实现智能日程助手
- [ ] 开发音乐生成器

---

**下次汇报：** {datetime.fromtimestamp(time.time() + 3600).strftime('%H:%M')}
"""
    return report

def wait_for_next_hour():
    """等待到下一个整点"""
    now = time.time()
    next_hour = (int(now // 3600) + 1) * 3600
    wait_time = next_hour - now

    print(f"当前时间：{datetime.now().strftime('%H:%M:%S')}")
    print(f"下次汇报：{datetime.fromtimestamp(next_hour).strftime('%H:%M:00')}")
    print(f"等待时间：{wait_time:.0f} 秒\n")

    if wait_time > 0:
        time.sleep(wait_time)

def main():
    print("=" * 60)
    print("🎮 创意开发调度器启动")
    print("=" * 60)

    while True:
        try:
            # 等待到下一个整点
            wait_for_next_hour()

            # 生成报告
            report = generate_report()

            # 保存报告
            report_file = f'/root/.openclaw/workspace/report_{datetime.now().strftime("%Y%m%d_%H%M")}.md'
            with open(report_file, 'w') as f:
                f.write(report)

            print("\n" + "=" * 60)
            print("整点汇报")
            print("=" * 60)
            print(report)

        except KeyboardInterrupt:
            print("\n调度器已停止")
            break
        except Exception as e:
            print(f"错误：{e}")
            time.sleep(60)

if __name__ == '__main__':
    main()
