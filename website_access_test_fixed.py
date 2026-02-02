#!/usr/bin/env python3
"""
🌐 公开网站访问测试脚本（修复版）
修复：添加 import json
测试哪些公开的网站可以访问，哪些不能访问
"""

import requests
import json
import os
from datetime import datetime, timezone, timedelta

# 配置
BEIJING_TZ = timezone(timedelta(hours=8))
TEST_TIMEOUT = 10  # 每个网站的超时时间（秒）

# 待测试的网站列表
WEBSITES_TO_TEST = [
    {
        "name": "GitHub",
        "url": "https://github.com/",
        "category": "代码托管",
        "description": "全球最大的代码托管平台"
    },
    {
        "name": "Wikipedia",
        "url": "https://www.wikipedia.org/",
        "category": "百科全书",
        "description": "全球最大的百科全书"
    },
    {
        "name": "Google",
        "url": "https://www.google.com/",
        "category": "搜索引擎",
        "description": "全球最大的搜索引擎"
    },
    {
        "name": "Stack Overflow",
        "url": "https://stackoverflow.com/",
        "category": "技术问答",
        "description": "全球最大的程序员问答社区"
    },
    {
        "name": "Reddit",
        "url": "https://www.reddit.com/",
        "category": "社交新闻",
        "description": "全球最大的社交新闻网站"
    },
    {
        "name": "Medium",
        "url": "https://medium.com/",
        "category": "博客平台",
        "description": "全球最大的博客平台"
    },
    {
        "name": "OpenAI",
        "url": "https://openai.com/",
        "category": "AI 公司",
        "description": "全球领先的 AI 研究公司"
    },
    {
        "name": "V2EX",
        "url": "https://www.v2ex.com/",
        "category": "中文技术社区",
        "description": "全球最大的中文技术社区"
    },
    {
        "name": "掘金",
        "url": "https://juejin.cn/",
        "category": "中文技术社区",
        "description": "全球最大的中文技术社区"
    },
    {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com/",
        "category": "计算机科学新闻",
        "description": "全球最大的计算机科学新闻网站"
    },
    {
        "name": "Python",
        "url": "https://www.python.org/",
        "category": "编程语言",
        "description": "Python 官方网站"
    },
    {
        "name": "Flask",
        "url": "https://flask.palletsprojects.com/",
        "category": "Web 框架",
        "description": "Flask 官方网站"
    },
    {
        "name": "LangChain",
        "url": "https://python.langchain.com/",
        "category": "AI 框架",
        "description": "LangChain 官方网站"
    },
    {
        "name": "知乎",
        "url": "https://www.zhihu.com/",
        "category": "中文问答社区",
        "description": "全球最大的中文问答社区"
    },
    {
        "name": "CSDN",
        "url": "https://www.csdn.net/",
        "category": "中文技术社区",
        "description": "全球最大的中文技术社区"
    }
]

# 日志配置
def log(message):
    """记录日志"""
    timestamp = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [WEBSITE-TEST] {message}"
    print(log_message)
    
    # 记录到文件
    log_file = "/root/.openclaw/workspace/website_access_test_log.txt"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_message + '\n')

# 测试单个网站
def test_website(website_info):
    """测试单个网站"""
    name = website_info.get("name", "")
    url = website_info.get("url", "")
    category = website_info.get("category", "")
    
    try:
        # 发送 GET 请求
        response = requests.get(url, timeout=TEST_TIMEOUT, allow_redirects=True)
        
        # 分析状态码
        status_code = response.status_code
        success = status_code in [200, 301, 302]
        
        return {
            "name": name,
            "url": url,
            "category": category,
            "status_code": status_code,
            "success": success,
            "response_time": response.elapsed.total_seconds(),
            "content_length": len(response.content)
        }
    except Exception as e:
        return {
            "name": name,
            "url": url,
            "category": category,
            "status_code": 0,
            "success": False,
            "error": str(e),
            "response_time": 0,
            "content_length": 0
        }

# 主函数
def main():
    """主函数"""
    log("=" * 60)
    log("🌐 公开网站访问测试 - 开始（修复版）")
    log("=" * 60)
    
    log(f"\n📋 待测试的网站数量：{len(WEBSITES_TO_TEST)}")
    log(f"   超时时间：{TEST_TIMEOUT} 秒/网站")
    
    # 测试所有网站
    log(f"\n📊 开始测试 {len(WEBSITES_TO_TEST)} 个网站...")
    
    results = []
    accessible_websites = []
    inaccessible_websites = []
    
    for i, website_info in enumerate(WEBSITES_TO_TEST, 1):
        name = website_info.get("name", "")
        url = website_info.get("url", "")
        category = website_info.get("category", "")
        
        log(f"\n🔍 [{i}/{len(WEBSITES_TO_TEST)}] 测试 {name} ({category})")
        
        # 测试网站
        result = test_website(website_info)
        results.append(result)
        
        if result["success"]:
            log(f"   ✅ 访问成功（状态码：{result['status_code']}，响应时间：{result['response_time']:.2f} 秒）")
            accessible_websites.append(result)
        else:
            log(f"   ❌ 访问失败（状态码：{result.get('status_code', 'ERROR')}，错误：{result.get('error', 'Unknown error')}）")
            inaccessible_websites.append(result)
    
    # 生成总结报告
    log(f"\n" + "=" * 60)
    log("📊 测试总结")
    log("=" * 60)
    
    log(f"\n✅ 可访问网站：{len(accessible_websites)}/{len(WEBSITES_TO_TEST)}")
    
    if accessible_websites:
        for i, website in enumerate(accessible_websites, 1):
            log(f"   {i}. {website['name']} ({website['category']})")
            log(f"      状态码：{website['status_code']}")
            log(f"      响应时间：{website['response_time']:.2f} 秒")
    
    log(f"\n❌ 不可访问网站：{len(inaccessible_websites)}/{len(WEBSITES_TO_TEST)}")
    
    if inaccessible_websites:
        for i, website in enumerate(inaccessible_websites, 1):
            log(f"   {i}. {website['name']} ({website['category']})")
            log(f"      状态码：{website.get('status_code', 'ERROR')}")
            log(f"      错误：{website.get('error', 'Unknown error')}")
    
    # 保存结果到 JSON 文件
    log(f"\n💾 保存测试结果...")
    
    output_file = "/root/.openclaw/workspace/website_access_test_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_time": datetime.now(BEIJING_TZ).isoformat(),
            "total_websites": len(WEBSITES_TO_TEST),
            "accessible_count": len(accessible_websites),
            "inaccessible_count": len(inaccessible_websites),
            "accessible_websites": accessible_websites,
            "inaccessible_websites": inaccessible_websites
        }, f, ensure_ascii=False, indent=2)
    
    log(f"   ✅ 测试结果已保存到 {output_file}")
    
    # 最终总结
    log(f"\n" + "=" * 60)
    log("✅ 公开网站访问测试完成！")
    log("=" * 60)
    
    log(f"\n📊 测试统计：")
    log(f"   总网站数：{len(WEBSITES_TO_TEST)}")
    log(f"   可访问：{len(accessible_websites)}")
    log(f"   不可访问：{len(inaccessible_websites)}")

if __name__ == '__main__':
    main()
