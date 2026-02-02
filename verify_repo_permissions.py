#!/usr/bin/env python3
"""
🔑 仓库与权限验证器
目标：
1. 验证目标仓库是否存在
2. 验证 Token 是否有访问该仓库的权限
3. 如果存在且有权限，尝试创建一个文件来确认写入权限
4. 如果不存在或无权限，建议用户创建新仓库
"""

import requests
from datetime import datetime, timezone, timedelta

# 配置
GITHUB_TOKEN = "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"
GITHUB_API = "https://api.github.com"
TARGET_USER = "huangsir1983"
TARGET_REPO = "6666"  # 假设仓库名称

BEIJING_TZ = timezone(timedelta(hours=8))

def log(message):
    """记录日志"""
    timestamp = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [REPO-VERIFY] {message}"
    print(log_message)

print("=" * 60)
print("🔑 仓库与权限验证 - 开始")
print("=" * 60)

# 1. 验证仓库是否存在
print("\n📋 第一步：验证仓库是否存在")
repo_url = f"{GITHUB_API}/repos/{TARGET_USER}/{TARGET_REPO}"
headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

try:
    response = requests.get(repo_url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        print(f"   ✅ 仓库存在：https://github.com/{TARGET_USER}/{TARGET_REPO}")
    elif response.status_code == 404:
        print(f"   ❌ 仓库不存在：{TARGET_USER}/{TARGET_REPO}")
        print(f"\n💡 建议：")
        print(f"   1. 请确认仓库名称是否正确")
        print(f"   2. 如果仓库确实不存在，请新建一个仓库")
        print(f"   3. 新建仓库后，更新本地 Git 配置的远程仓库地址")
    else:
        print(f"   ❌ 验证失败，状态码：{response.status_code}")
except Exception as e:
    print(f"   ❌ 验证失败：{str(e)}")

# 2. 验证 Token 是否有写入权限
print("\n📋 第二步：验证 Token 权限")
try:
    # 尝试获取仓库信息（这需要读取权限）
    response = requests.get(repo_url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        print(f"   ✅ Token 有读取权限")
        
        # 检查权限 (push, pull, admin)
        permissions = response.json().get('permissions', {})
        can_push = permissions.get('push', False)
        
        print(f"   权限列表：{list(permissions.keys())}")
        print(f"   推送权限：{'有' if can_push else '无'}")
        
        if can_push:
            print(f"\n💡 建议：")
            print(f"   Token 有推送权限，应该可以成功推送")
            print(f"   如果仍然失败，可能是网络问题或 Git 配置问题")
        else:
            print(f"\n💡 建议：")
            print(f"   Token 无推送权限，无法推送到该仓库")
            print(f"   请检查 Token 权限：https://github.com/settings/tokens")
            print(f"   或者，请新建一个属于你的仓库")
    elif response.status_code == 404:
        print(f"   ⚠️  仓库不存在，无法验证权限")
    else:
        print(f"   ❌ 权限验证失败，状态码：{response.status_code}")
except Exception as e:
    print(f"   ❌ 权限验证失败：{str(e)}")

# 3. 尝试创建一个测试文件（验证写入权限）
print("\n📋 第三步：验证写入权限（创建测试文件）")
try:
    # 尝试创建一个测试文件（使用 GitHub API Contents）
    test_file_path = "PERMISSION_TEST_001.txt"
    test_content = f"Test file created at {datetime.now(BEIJING_TZ).isoformat()}\nTest content: Token has write permission.\n"
    
    content_url = f"{GITHUB_API}/repos/{TARGET_USER}/{TARGET_REPO}/contents/{test_file_path}"
    put_data = {
        "message": f"Test file: Token permission verification",
        "content": test_content
    }
    
    put_response = requests.put(content_url, headers=headers, json=put_data)
    
    if put_response.status_code in [200, 201]:
        print(f"   ✅ 测试文件创建成功：{test_file_path}")
        print(f"   ✅ Token 有写入权限")
        print(f"   ✅ 仓库地址正确：https://github.com/{TARGET_USER}/{TARGET_REPO}")
    elif put_response.status_code == 404:
        print(f"   ❌ 仓库不存在或路径错误：{test_file_path}")
    elif put_response.status_code == 403:
        print(f"   ❌ Token 无写入权限")
    else:
        print(f"   ❌ 测试文件创建失败，状态码：{put_response.status_code}")
        print(f"   响应：{put_response.text}")
except Exception as e:
    print(f"   ❌ 测试文件创建失败：{str(e)}")

# 最终总结
print(f"\n" + "=" * 60)
print("✅ 仓库与权限验证 - 完成")
print("=" * 60)

print(f"\n💡 下一步行动建议：")

# 根据验证结果提供建议
print("方案 1：如果仓库存在且有推送权限")
print("   - 检查网络连接和 Git 配置")
print("   - 尝试使用 HTTPS 而不是 SSH")
print("   - 手动推送（在本地终端执行 git push）")

print("方案 2：如果仓库不存在或无推送权限")
print("   - 请你手动在 GitHub 上创建一个新仓库（例如：huangsir1983/my-ai-workspace）")
print("   - 新建仓库后，更新本地 Git 配置：")
print("     git remote remove origin")
print("     git remote add origin https://github.com/huangsir1983/my-ai-workspace.git")
print("     git push origin master")

print("方案 3：如果上述方案都失败")
print("   - 请检查 GitHub Token 权限：https://github.com/settings/tokens")
print("   - 请确认 Token 对应的用户是你自己")
print("   - 确保 Token 有推送权限（repo scope）")
