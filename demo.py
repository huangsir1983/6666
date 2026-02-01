#!/usr/bin/env python3
"""
AI 工具箱 - 演示脚本
展示所有服务的功能和使用方法
"""

import requests
import json
import time
from datetime import datetime


class AIToolkitDemo:
    def __init__(self):
        self.proxy_url = "http://localhost:8080"
        self.auth_url = "http://localhost:8082"
        self.api_key = None

    def print_header(self, title):
        """打印标题"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)

    def print_success(self, message):
        """打印成功消息"""
        print(f"✅ {message}")

    def print_error(self, message):
        """打印错误消息"""
        print(f"❌ {message}")

    def check_service(self, url, service_name):
        """检查服务状态"""
        try:
            # 认证服务的健康检查端点是 /auth/health
            if service_name == "认证服务":
                health_url = f"{url}/auth/health"
            else:
                health_url = f"{url}/health"

            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                self.print_success(f"{service_name} 运行正常 ({url})")
                return True
            else:
                self.print_error(f"{service_name} 状态异常")
                return False
        except Exception as e:
            self.print_error(f"{service_name} 无法连接: {e}")
            return False

    def register_user(self):
        """注册用户"""
        self.print_header("用户注册")

        email = f"demo_{int(time.time())}@example.com"
        password = "demo123456"

        data = {
            "email": email,
            "password": password,
            "name": "演示用户"
        }

        try:
            response = requests.post(
                f"{self.auth_url}/auth/register",
                json=data,
                timeout=5
            )

            if response.status_code == 201:
                result = response.json()
                self.api_key = result['api_key']
                self.print_success(f"注册成功！")
                print(f"   邮箱: {email}")
                print(f"   API Key: {self.api_key}")
                print(f"   套餐: {result['plan']}")
                return True
            else:
                self.print_error(f"注册失败: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"注册异常: {e}")
            return False

    def send_message(self, message):
        """发送消息到 AI"""
        self.print_header("发送消息到 AI")

        if not self.api_key:
            self.print_error("未获取 API Key")
            return False

        data = {
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 200,
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        try:
            start_time = time.time()
            response = requests.post(
                f"{self.proxy_url}/v1/messages",
                json=data,
                headers={"X-API-Key": self.api_key},
                timeout=30
            )
            elapsed = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                content = result['content'][0]['text']

                self.print_success(f"消息发送成功！")
                print(f"   用户: {message}")
                print(f"   AI: {content}")
                print(f"   响应时间: {elapsed:.2f}秒")
                return True
            else:
                self.print_error(f"发送失败: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"发送异常: {e}")
            return False

    def get_usage(self):
        """获取使用量"""
        self.print_header("使用量统计")

        if not self.api_key:
            self.print_error("未获取 API Key")
            return False

        try:
            response = requests.get(
                f"{self.auth_url}/auth/usage",
                headers={"X-API-Key": self.api_key},
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()
                self.print_success("使用量获取成功！")
                print(f"   当前套餐: {result['plan']}")
                print(f"   日用量: {result['daily_used']}/{result['daily_remaining']}")
                print(f"   月用量: {result['monthly_used']}/{result['monthly_remaining']}")
                return True
            else:
                self.print_error(f"获取失败: {response.text}")
                return False
        except Exception as e:
            self.print_error(f"获取异常: {e}")
            return False

    def run_demo(self):
        """运行完整演示"""
        print("\n" + "🚀" * 30)
        print("  AI 工具箱 - 功能演示")
        print("🚀" * 30)

        # 检查服务状态
        print("\n📊 检查服务状态...")
        services_ok = True
        services_ok &= self.check_service(self.proxy_url, "代理服务")
        services_ok &= self.check_service(self.auth_url, "认证服务")

        if not services_ok:
            self.print_error("部分服务未运行，请先启动服务")
            return

        # 注册用户
        if not self.register_user():
            return

        # 发送测试消息
        test_messages = [
            "你好，请用一句话介绍你自己",
            "写一个 Python 的 Hello World 程序",
            "给我一个有趣的冷知识"
        ]

        for msg in test_messages:
            self.send_message(msg)
            time.sleep(1)

        # 获取使用量
        self.get_usage()

        # 演示完成
        self.print_header("演示完成")
        print(f"   演示时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   使用时间: 约 {len(test_messages) * 2} 秒")
        print("\n💡 提示: 访问 http://localhost:8081 查看完整应用")


if __name__ == "__main__":
    demo = AIToolkitDemo()
    demo.run_demo()
