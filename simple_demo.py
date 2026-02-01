#!/usr/bin/env python3
"""
简单的 AI 工具箱演示
"""

import requests
import json

def test_services():
    """测试所有服务"""
    print("🚀 AI 工具箱 - 服务测试\n")

    # 1. 测试代理服务
    print("1️⃣ 测试代理服务...")
    try:
        r = requests.get('http://localhost:8080/health', timeout=5)
        if r.status_code == 200:
            print("   ✅ 代理服务正常")
        else:
            print("   ❌ 代理服务异常")
    except Exception as e:
        print(f"   ❌ 代理服务失败: {e}")

    # 2. 测试认证服务
    print("\n2️⃣ 测试认证服务...")
    try:
        r = requests.get('http://localhost:8082/auth/health', timeout=5)
        if r.status_code == 200:
            print("   ✅ 认证服务正常")
        else:
            print("   ❌ 认证服务异常")
    except Exception as e:
        print(f"   ❌ 认证服务失败: {e}")

    # 3. 测试 HTTP 服务
    print("\n3️⃣ 测试 HTTP 服务...")
    try:
        r = requests.get('http://localhost:8081/', timeout=5)
        if r.status_code == 200:
            print("   ✅ HTTP 服务正常")
        else:
            print("   ❌ HTTP 服务异常")
    except Exception as e:
        print(f"   ❌ HTTP 服务失败: {e}")

    # 4. 测试用户注册
    print("\n4️⃣ 测试用户注册...")
    import time
    email = f"test_{int(time.time())}@example.com"
    data = {
        "email": email,
        "password": "test123456",
        "name": "测试用户"
    }
    try:
        r = requests.post(
            'http://localhost:8082/auth/register',
            json=data,
            timeout=5
        )
        if r.status_code == 201:
            result = r.json()
            api_key = result['api_key']
            print(f"   ✅ 注册成功")
            print(f"      API Key: {api_key}")
        else:
            print(f"   ❌ 注册失败: {r.text}")
    except Exception as e:
        print(f"   ❌ 注册异常: {e}")

    # 5. 测试 API 调用
    print("\n5️⃣ 测试 API 调用...")
    if 'api_key' in locals():
        data = {
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 100,
            "messages": [
                {"role": "user", "content": "你好，请用一句话介绍你自己"}
            ]
        }
        try:
            print("   发送请求...")
            r = requests.post(
                'http://localhost:8080/v1/messages',
                json=data,
                headers={"X-API-Key": api_key},
                timeout=10
            )
            if r.status_code == 200:
                result = r.json()
                content = result['content'][0]['text']
                print(f"   ✅ API 调用成功")
                print(f"      AI 响应: {content[:100]}...")
            else:
                print(f"   ❌ API 调用失败: {r.text}")
        except Exception as e:
            print(f"   ❌ API 调用异常: {e}")
    else:
        print("   ⏭️  跳过（未获取到 API Key）")

    print("\n✅ 测试完成！")
    print("\n💡 访问 http://localhost:8081 查看完整应用")

if __name__ == "__main__":
    test_services()
