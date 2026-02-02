#!/usr/bin/env python3
"""
AI 社交媒体内容生成器
自动生成社交媒体内容
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
        
        topic = data.get('topic', '')
        platform = data.get('platform', 'weibo')
        content_type = data.get('content_type', 'promotional')
        tone = data.get('tone', 'casual')
        
        if not topic:
            return jsonify({"error": "请输入主题"}), 400
        
        # 生成内容
        content = generate_content(topic, platform, content_type, tone)
        
        return jsonify({
            "success": True,
            "content": content
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch_generate', methods=['POST'])
def batch_generate():
    try:
        data = request.json
        
        topic = data.get('topic', '')
        platforms = data.get('platforms', ['weibo', 'wechat', 'xiaohongshu'])
        content_type = data.get('content_type', 'promotional')
        tone = data.get('tone', 'casual')
        
        if not topic:
            return jsonify({"error": "请输入主题"}), 400
        
        # 批量生成
        contents = []
        for i, platform in enumerate(platforms[:5]):
            content = generate_content(topic, platform, content_type, tone)
            contents.append({
                "id": i + 1,
                "platform": platform,
                "content": content
            })
        
        return jsonify({
            "success": True,
            "contents": contents
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_content(topic, platform, content_type, tone):
    """生成社交媒体内容"""
    
    # 平台描述
    platform_descriptions = {
        'weibo': '微博（简短、吸引人）',
        'wechat': '朋友圈（亲切、生活化）',
        'xiaohongshu': '小红书（详细、分享经验）',
        'douyin': '抖音（简短、有趣）',
        'bilibili': 'B站（技术、教育）'
    }
    
    # 类型描述
    type_descriptions = {
        'promotional': '推广',
        'share': '分享',
        'tutorial': '教程',
        'discussion': '讨论'
    }
    
    # 构建提示词
    prompt = f"""
请为以下主题生成{platform_descriptions[platform]}平台的{type_descriptions[content_type]}内容。

主题：{topic}
平台：{platform_descriptions[platform]}
类型：{type_descriptions[content_type]}
语气：{tone}

要求：
1. 内容要吸引人，能引起兴趣
2. 语言要{tone}，符合平台特点
3. 包含适当的表情符号
4. 长度控制在 100-150 字左右
5. 要有话题标签（#标签）
6. 避免过于推销

请直接输出内容，不需要其他解释。
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
                "max_tokens": 400
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
            return generate_template_content(topic, platform, content_type, tone)
    
    except:
        return generate_template_content(topic, platform, content_type, tone)

def generate_template_content(topic, platform, content_type, tone):
    """生成模板内容（备用）"""
    
    emoji_map = {
        'weibo': ['🚀', '💡', '✨', '🎯', '🔥'],
        'wechat': ['💭', '📝', '✍️', '📷', '🎁'],
        'xiaohongshu': ['💖', '✨', '🎉', '👍', '💡'],
        'douyin': ['🔥', '💃', '🎵', '✨', '🚀'],
        'bilibili': ['🎮', '📺', '📚', '🎥', '👍']
    }
    
    emojis = emoji_map.get(platform, ['✨', '💡'])
    
    if content_type == 'promotional':
        content = f"""{emojis[0]} {topic}：重新定义{platform_descriptions[platform]}！{emojis[1]}

想要体验{topic}的魅力吗？现在就是最好的时机！{emojis[2]}
立即行动，开启全新体验！{emojis[3]}

#话题 #{platform} # {topic.replace(' ', '')}"""
    
    elif content_type == 'share':
        content = f"""{emojis[0]} 发现一个超赞的{topic}！{emojis[1]}

{platform_descriptions[platform]}平台的朋友们，强烈推荐给大家！{emojis[2]}
体验之后你会发现打开了新世界！{emojis[3]]

#话题 #推荐 # {topic.replace(' ', '')} # 分享"""
    
    elif content_type == 'tutorial':
        content = f"""{emojis[0]} {topic}教程来啦！{emojis[1]}

今天教大家如何使用{topic}，简单3步就能上手！{emojis[2]}
新手友好，详细讲解，让你轻松掌握！{emojis[3]}

#话题 #教程 # {topic.replace(' ', '')} # 学习"""
    
    elif content_type == 'discussion':
        content = f"""{emojis[0]} 关于{topic}，大家怎么看？{emojis[1]}

最近{topic}很火，想听听大家的想法！{emojis[2]}
有使用过的朋友吗？体验如何？{emojis[3]}

#话题 #讨论 # {topic.replace(' ', '')} # 交流"""
    
    else:
        content = f"""{emojis[0]} {topic}太棒了！{emojis[1]}

在{platform_descriptions[platform]}平台上发现了{topic}，感觉打开了新世界！{emojis[2]}
强烈推荐给大家，体验一下！{emojis[3]}

#话题 #推荐 # {topic.replace(' ', '')} # 分享"""
    
    return content

if __name__ == '__main__':
    port = 8086
    print(f"AI 社交媒体内容生成器启动中...")
    print(f"端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
