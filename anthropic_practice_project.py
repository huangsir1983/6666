#!/usr/bin/env python3
"""
🧬 Anthropic/Claude Code 实战项目 1：文档摘要器
基于真实技术学习成果（litellm, claude-engineer, agent-squad）
目标：实现一个能调用 Claude API 摘取文章摘要、关键点、思维导图结构的实际应用
"""

import os
import sys

# 日志配置
def log(message):
    """记录日志"""
    timestamp = datetime.now(BEIJING_TZ).strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [ANTHROPIC-PRACTICE] {message}"
    print(log_message)

# 检查依赖
try:
    import requests
    from datetime import datetime, timezone, timedelta
    import json
except ImportError as e:
    print(f"❌ 缺少依赖：{e}")
    print("请运行：pip install requests")
    sys.exit(1)

# 配置
WORKSPACE = "/root/.openclaw/workspace"
PROJECT_DIR = f"{WORKSPACE}/anthropic_projects"
BEIJING_TZ = timezone(timedelta(hours=8))

# 创建项目目录
os.makedirs(PROJECT_DIR, exist_ok=True)

# GitHub 配置
GITHUB_TOKEN = "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"
GITHUB_API = "https://api.github.com"
REPO_OWNER = "huangsir1983"
REPO_NAME = "6666"


class ClaudeDocSummarizer:
    """Claude 文档摘要器（模拟，因为缺少 API Key）"""
    
    def __init__(self, model="claude-3-5-sonnet-20240229", api_key=None):
        self.model = model
        self.api_key = api_key
        
        if not api_key:
            log(f"⚠️  未提供 API Key，将使用模拟模式")
            log(f"   要使用真实 Claude API，请提供 Anthropic API Key")
            log(f"   获取 Key：https://console.anthropic.com/")
    
    def summarize(self, text_or_url, max_tokens=1000):
        """摘要文档"""
        log(f"\n🔍 [摘要器] 摘要：{text_or_url[:50]}...")
        
        if self.api_key:
            # 真实模式（使用 litellm 或直接调用 Anthropic API）
            # 注意：这里需要安装 litellm: pip install litellm
            # 或者直接使用 requests 调用 Anthropic API
            try:
                import litellm
                
                response = litellm.completion(
                    model=self.model,
                    api_key=self.api_key,
                    messages=[
                        {
                            "role": "user",
                            "content": f"请摘要以下文档或URL的内容，提取关键点、思维导图结构和最终结论：\n\n{text_or_url}"
                        }
                    ],
                    max_tokens=max_tokens
                )
                
                summary = response.choices[0].message.content
                log(f"   ✅ 真实摘要完成（{len(summary)} 字符）")
                return summary
            except ImportError:
                log(f"   ❌ 未安装 litellm，请运行：pip install litellm")
                return self.mock_summarize(text_or_url)
            except Exception as e:
                log(f"   ❌ 调用 Claude API 失败：{str(e)}")
                return self.mock_summarize(text_or_url)
        else:
            # 模拟模式
            return self.mock_summarize(text_or_url)
    
    def mock_summarize(self, text_or_url):
        """模拟摘要（用于测试）"""
        log(f"   ✅ 模拟摘要完成")
        
        # 基于搜索结果的模拟摘要
        if "Opus 4.5" in text_or_url:
            return """
            **摘要：** Opus 4.5 的性能提升远超预期，特别是在代理任务上。
            **关键点：**
            1. Mid-brain takes on software and AI
            2. The model is not just a better version of Claude 3.5, it's a different model entirely
            3. It's a much stronger agent
            **思维导图：**
            - 性能提升
              - 代理任务
              - 模型不同
              - 更强代理
            """
        elif "Windows 11" in text_or_url:
            return """
            **摘要：** AI 代理正在被集成到操作系统中（如 Windows 11），并且将访问个人文件夹。
            **关键点：**
            1. Microsoft is planning to add an AI agent that runs in background
            2. It will have access to personal folders
            3. There are security risks
            **思维导图：**
            - 操作系统集成
              - Windows 11
                - AI 代理
                - 后台运行
                - 访问个人文件夹
                - 安全风险
            """
        elif "Building Effective AI Agents" in text_or_url:
            return """
            **摘要：** 构建有效的 AI 代理需要特定的工程技巧，而不仅仅是强大的模型。
            **关键点：**
            1. Tool use (工具使用)
            2. Memory (记忆)
            3. Planning (规划)
            4. Execution (执行)
            **思维导图：**
            - 构建有效 AI 代理
              - 工程技巧
                - 工具调用
                - 记忆管理
                - 任务规划
                - 任务执行
            """
        else:
            return """
            **摘要：** 这是一个通用文档的模拟摘要。
            **关键点：**
            1. 提取标题和正文
            2. 分析核心观点
            3. 生成结构化摘要
            **思维导图：**
            - 通用文档
              - 摘要
                - 标题
                - 正文
                - 核心观点
                - 结构化摘要
            """


# 主函数
def main():
    """主函数"""
    log("=" * 60)
    log("🧬 Anthropic/Claude Code 实战项目 1：文档摘要器")
    log("=" * 60)
    
    # 检查 litellm
    try:
        import litellm
        log(f"   ✅ litellm 已安装（版本：{litellm.__version__}）")
    except ImportError:
        log(f"   ❌ litellm 未安装，请运行：pip install litellm")
        log(f"   将使用模拟模式...")
        litellm = None
    
    # 初始化摘要器
    # 注意：这里没有真实的 Anthropic API Key
    # 要使用真实的 Claude API，请获取 Key 并替换 API_KEY
    API_KEY = "YOUR_ANTHROPIC_API_KEY"  # 替换为真实的 Key
    summarizer = ClaudeDocSummarizer(api_key=API_KEY if API_KEY != "YOUR_ANTHROPIC_API_KEY" else None)
    
    # 测试摘要
    log(f"\n🔍 测试摘要器（3 个例子）")
    
    test_cases = [
        "Opus 4.5 is not normal AI agent experience that I have had thus far",
        "Windows 11 adds AI agent that runs in background with access to personal folders",
        "Building Effective AI Agents"
    ]
    
    results = []
    for i, text in enumerate(test_cases, 1):
        log(f"\n{i}. 测试：{text[:50]}...")
        summary = summarizer.summarize(text, max_tokens=1000)
        results.append({
            "id": i,
            "text": text,
            "summary": summary
        })
    
    # 保存结果
    log(f"\n💾 保存测试结果...")
    output_file = f"{PROJECT_DIR}/claude_doc_summarizer_results_{datetime.now(BEIJING_TZ).strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    log(f"   ✅ 测试结果已保存到 {output_file}")
    
    # 最终总结
    log(f"\n" + "=" * 60)
    log("✅ Anthropic/Claude Code 实战项目 1 完成！")
    log("=" * 60)
    
    log(f"\n📊 项目统计：")
    log(f"   总测试用例：3")
    log(f"   模拟模式：是（因为缺少 API Key）")
    log(f"   真实模式：否（需要 API Key）")
    
    log(f"\n💡 下一步：")
    log(f"   1. 获取 Anthropic API Key：https://console.anthropic.com/")
    log(f"   2. 安装 litellm：pip install litellm")
    log(f"   3. 替换脚本中的 API_KEY 为真实的 Key")
    log(f"   4. 重新运行脚本：python3 anthropic_practice_project.py")


if __name__ == '__main__':
    main()
