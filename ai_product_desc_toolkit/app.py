#!/usr/bin/env python3
"""
AI 产品描述生成器
自动生成吸引人的产品描述
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
        
        product_name = data.get('product_name', '')
        product_features = data.get('product_features', '')
        description_type = data.get('description_type', 'product')
        platform = data.get('platform', 'ecommerce')
        tone = data.get('tone', 'professional')
        
        if not product_name:
            return jsonify({"error": "请输入产品名称"}), 400
        
        # 生成产品描述
        description = generate_description(
            product_name, product_features, description_type, platform, tone
        )
        
        return jsonify({
            "success": True,
            "description": description
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch_generate', methods=['POST'])
def batch_generate():
    try:
        data = request.json
        
        product_name = data.get('product_name', '')
        product_features = data.get('product_features', '')
        platforms = data.get('platforms', ['ecommerce', 'website', 'social'])
        description_type = data.get('description_type', 'product')
        tone = data.get('tone', 'professional')
        
        if not product_name:
            return jsonify({"error": "请输入产品名称"}), 400
        
        # 批量生成
        descriptions = []
        for i, platform in enumerate(platforms[:5]):  # 最多5个
            desc = generate_description(
                product_name, product_features, description_type, platform, tone
            )
            descriptions.append({
                "id": i + 1,
                "platform": platform,
                "description": desc
            })
        
        return jsonify({
            "success": True,
            "descriptions": descriptions
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_description(product_name, product_features, description_type, platform, tone):
    """生成产品描述"""
    
    # 平台描述
    platform_descriptions = {
        'ecommerce': '电商平台',
        'website': '官网',
        'social': '社交媒体',
        'app': '移动应用'
    }
    
    # 类型描述
    type_descriptions = {
        'product': '产品描述',
        'feature': '功能特点',
        'marketing': '营销文案',
        'seo': 'SEO 描述'
    }
    
    # 构建提示词
    prompt = f"""
请为一款产品生成吸引人的{type_descriptions[description_type]}，用于{platform_descriptions[platform]}。

产品名称：{product_name}
产品特点：{product_features}
平台：{platform_descriptions[platform]}
语气风格：{tone}

要求：
1. 标题要吸引人，能引起兴趣
2. 内容要突出产品的核心价值
3. 语言要{tone}，不要过于推销
4. 长度控制在 100-150 字左右
5. 要包含行动号召（CTA）
6. 适合{platform_descriptions[platform]}使用

请直接输出描述内容，不需要其他解释。
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
                "max_tokens": 300
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
            # 如果 API 调用失败，返回模板
            return generate_template_description(product_name, product_features, description_type, platform, tone)
    
    except:
        # 如果出现异常，返回模板
        return generate_template_description(product_name, product_features, description_type, platform, tone)

def generate_template_description(product_name, product_features, description_type, platform, tone):
    """生成模板描述（备用）"""
    
    platform_desc = {
        'ecommerce': '电商平台',
        'website': '官网',
        'social': '社交媒体',
        'app': '移动应用'
    }
    
    if description_type == 'product':
        return f"""【{product_name}】重新定义{platform_desc[platform]}体验

{product_features}

{platform_desc[platform]}专为追求{tone}品质的用户打造，带来前所未有的便捷与高效。立即体验，开启全新生活方式！"""
    
    elif description_type == 'feature':
        return f"""✨ {product_name} 核心功能：{product_features}

简单易用，一键上手。{tone}的设计，流畅的体验，让您轻松享受科技带来的便利。立即了解更多！"""
    
    elif description_type == 'marketing':
        return f"""🚀 {product_name} 限时优惠！

{product_features}

{product_name} 是{platform_desc[platform]}上的明星产品，已帮助数万用户实现目标。现在加入，享受专属优惠！"""
    
    elif description_type == 'seo':
        return f"""{product_name} - {platform_desc[platform]}首选

{product_features}。{product_name} 提供{tone}的解决方案，满足您的所有需求。立即了解更多，开启全新体验！"""
    
    else:
        return f"""{product_name} - {platform_desc[platform]}推荐

{product_features}。{product_name} 以{tone}的品质和{tone}的服务，重新定义您的体验。立即加入，发现更多惊喜！"""

if __name__ == '__main__':
    port = 8084
    print(f"AI 产品描述生成器启动中...")
    print(f"端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
