#!/usr/bin/env python3
"""
AI SEO 内容生成器
自动生成 SEO 友好的文章
"""

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# 智谱 API 配置
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
ZHIPU_API_KEY = "your-zhipu-api-key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        
        keyword = data.get('keyword', '')
        article_type = data.get('article_type', 'blog')
        word_count = data.get('word_count', 800)
        tone = data.get('tone', 'professional')
        
        if not keyword:
            return jsonify({"error": "请输入关键词"}), 400
        
        # 生成文章
        article = generate_article(keyword, article_type, word_count, tone)
        
        return jsonify({
            "success": True,
            "article": article
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch_generate', methods=['POST'])
def batch_generate():
    try:
        data = request.json
        
        keyword = data.get('keyword', '')
        article_types = data.get('article_types', ['blog', 'tutorial', 'news'])
        word_count = data.get('word_count', 800)
        tone = data.get('tone', 'professional')
        
        if not keyword:
            return jsonify({"error": "请输入关键词"}), 400
        
        # 批量生成
        articles = []
        for i, article_type in enumerate(article_types[:5]):  # 最多5个
            article = generate_article(keyword, article_type, word_count, tone)
            articles.append({
                "id": i + 1,
                "type": article_type,
                "word_count": word_count,
                "content": article
            })
        
        return jsonify({
            "success": True,
            "articles": articles
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_article(keyword, article_type, word_count, tone):
    """生成 SEO 文章"""
    
    # 类型描述
    type_descriptions = {
        'blog': '博客文章',
        'tutorial': '教程文章',
        'news': '新闻文章',
        'review': '评测文章',
        'list': '列表文章'
    }
    
    # 构建提示词
    prompt = f"""
请为关键词"{keyword}"生成一篇{type_descriptions[article_type]}，文章要 SEO 友好。

关键词：{keyword}
文章类型：{type_descriptions[article_type]}
字数：{word_count}字左右
语气：{tone}

SEO 要求：
1. 标题要包含关键词，吸引人
2. 开头要自然包含关键词
3. 内容要围绕关键词展开
4. 段落清晰，层次分明
5. 要有适当的 LSI 关键词（相关关键词）
6. 结尾要有总结和行动号召
7. 适合发布在网站/博客

请直接输出文章内容，不需要其他解释。
"""
    
    # 调用智谱 API
    try:
        response = requests.post(
            ZHIPU_API_URL,
            json={
                "model": "glm-4.7",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 2000
            },
            headers={
                "Authorization": f"Bearer {ZHIPU_API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return content.strip()
        else:
            return generate_template_article(keyword, article_type, word_count, tone)
    
    except:
        return generate_template_article(keyword, article_type, word_count, tone)

def generate_template_article(keyword, article_type, word_count, tone):
    """生成模板文章（备用）"""
    
    if article_type == 'blog':
        return f"""## {keyword}：重新定义体验

{keyword}是近年来最热门的话题之一，越来越多的人开始关注和使用{keyword}。今天，我们就来深入探讨{keyword}的核心价值和应用场景。

### 为什么选择{keyword}？

{keyword}的优势主要体现在以下几个方面：

1. **高效率**：{keyword}能够显著提高工作效率，节省大量时间
2. **易用性**：简单易用，即使是没有相关经验的用户也能快速上手
3. **功能强大**：功能丰富，能够满足各种复杂的需求
4. **成本低廉**：相比其他解决方案，{keyword}的性价比更高

### {keyword}的核心功能

{keyword}的主要功能包括：

- 功能一：{keyword}的核心功能，提供了强大的支持
- 功能二：辅助功能，让使用体验更佳
- 功能三：高级功能，满足专业用户的需求

### 如何使用{keyword}？

使用{keyword}非常简单，只需要按照以下步骤：

1. 访问官网并注册账号
2. 下载并安装{keyword}
3. 按照教程完成配置
4. 开始使用{keyword}的各种功能

### {keyword}的实际应用

{keyword}在很多领域都有广泛的应用：

- **个人使用**：提高个人效率，简化日常任务
- **团队协作**：促进团队协作，提高团队效率
- **企业应用**：帮助企业实现数字化转型
- **教育领域**：辅助教学，提升学习效果

### 总结

{keyword}是一个非常强大的工具，它能够帮助我们提高效率、简化任务、实现目标。如果你还没有尝试过{keyword}，现在就是最好的时机！

立即行动，体验{keyword}带来的改变！"""
    
    elif article_type == 'tutorial':
        return f"""## {keyword}完全指南：从入门到精通

今天，我将为大家详细介绍如何使用{keyword}，从零基础到精通。

### 前置准备

在开始之前，你需要准备：

- 基础的计算机操作能力
- 对{keyword}的基本了解
- 足够的耐心和实践

### 第一步：认识{keyword}

首先，让我们来了解一下{keyword}的基本概念和原理。

{keyword}是一种...（{keyword}的原理介绍）

### 第二步：安装和配置

接下来，我们需要安装和配置{keyword}：

1. 访问官网下载{keyword}
2. 根据操作系统选择对应的版本
3. 运行安装程序，按照提示完成安装
4. 打开{keyword}，完成基础配置

### 第三步：基础功能

安装完成后，我们来学习{keyword}的基础功能：

- 功能一：...
- 功能二：...
- 功能三：...

### 第四步：进阶功能

掌握了基础功能后，我们来学习{keyword}的进阶功能：

- 进阶功能一：...
- 进阶功能二：...
- 进阶功能三：...

### 第五步：实际应用

最后，我们来学习{keyword}在实际项目中的应用：

- 场景一：...
- 场景二：...
- 场景三：...

### 总结

通过这个教程，你已经掌握了{keyword}从入门到精通的全部内容。现在，你可以开始在实际项目中使用{keyword}了！

如果你有任何问题，欢迎在评论区留言，我会尽快回复。

祝你学习愉快！"""
    
    else:
        return f"""## {keyword}：最新动态和深度分析

最近，{keyword}领域有了很多新的发展和变化，今天我们来深入了解一下。

### 最新动态

{keyword}领域的最新动态包括：

1. **新版本发布**：{keyword}发布了新版本，带来了很多新功能和改进
2. **行业趋势**：{keyword}在行业中的应用越来越广泛
3. **用户反馈**：用户对{keyword}的反馈非常积极

### 深度分析

让我们来深入分析{keyword}的核心价值：

- **技术优势**：{keyword}的技术优势明显，相比竞品有独特的优势
- **用户体验**：{keyword}的用户体验优秀，获得了用户的一致好评
- **市场前景**：{keyword}的市场前景广阔，有很大的发展潜力

### 行业应用

{keyword}在各行业都有广泛的应用：

- **金融行业**：{keyword}帮助金融机构提高效率
- **医疗行业**：{keyword}在医疗领域的应用越来越深入
- **教育行业**：{keyword}改变教育方式，提升学习效果
- **其他行业**：{keyword}在其他行业也有广泛的应用

### 未来展望

{keyword}的未来发展非常值得期待：

- **技术突破**：{keyword}将继续进行技术突破，带来更多创新
- **生态完善**：{keyword}的生态系统将越来越完善
- **市场扩张**：{keyword}将进一步扩大市场影响力
- **用户增长**：{keyword}的用户数量将持续增长

### 总结

{keyword}是一个非常有潜力的领域，值得大家关注和学习。如果你对{keyword}感兴趣，现在就是最好的时机！

立即行动，开始学习{keyword}吧！"""

if __name__ == '__main__':
    port = 8087
    print(f"AI SEO 内容生成器启动中...")
    print(f"端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
