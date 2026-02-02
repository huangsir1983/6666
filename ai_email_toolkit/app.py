#!/usr/bin/env python3
"""
AI 邮件营销工具
自动生成吸引人的营销邮件
"""

from flask import Flask, render_template, request, jsonify
import requests
import random
from datetime import datetime

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
        target_audience = data.get('target_audience', '')
        email_type = data.get('email_type', 'promotional')
        tone = data.get('tone', 'professional')
        
        if not product_name:
            return jsonify({"error": "请输入产品名称"}), 400
        
        # 生成邮件内容
        email_content = generate_email(
            product_name, product_features, target_audience, email_type, tone
        )
        
        return jsonify({
            "success": True,
            "content": email_content
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch_generate', methods=['POST'])
def batch_generate():
    try:
        data = request.json
        
        product_name = data.get('product_name', '')
        product_features = data.get('product_features', '')
        target_audiences = data.get('target_audiences', [])
        email_type = data.get('email_type', 'promotional')
        tone = data.get('tone', 'professional')
        count = data.get('count', 3)
        
        if not product_name:
            return jsonify({"error": "请输入产品名称"}), 400
        
        # 批量生成邮件
        emails = []
        for i in range(min(count, 10)):  # 最多10个
            email = generate_email(
                product_name, product_features, 
                target_audiences[i] if i < len(target_audiences) else '',
                email_type, tone
            )
            emails.append({
                "id": i + 1,
                "content": email
            })
        
        return jsonify({
            "success": True,
            "emails": emails
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_email(product_name, product_features, target_audience, email_type, tone):
    """生成邮件内容"""
    
    # 构建提示词
    prompt = f"""
请为一款产品生成一封{email_type}邮件。

产品名称：{product_name}
产品特点：{product_features}
目标受众：{target_audience}
语气风格：{tone}

要求：
1. 邮件标题要吸引人，能引起兴趣
2. 开头要有问候语
3. 内容要突出产品的核心价值
4. 要有明确的行动号召（CTA）
5. 语言要{tone}，不要过于推销
6. 邮件长度控制在 200-300 字左右

请直接输出邮件内容，不需要其他解释。
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
                "max_tokens": 500
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
            return generate_template_email(product_name, product_features, target_audience, email_type, tone)
    
    except:
        # 如果出现异常，返回模板
        return generate_template_email(product_name, product_features, target_audience, email_type, tone)

def generate_template_email(product_name, product_features, target_audience, email_type, tone):
    """生成模板邮件（备用）"""
    
    titles = {
        'promotional': f"限时优惠！{product_name} 现在入手最佳时机",
        'announcement': f"新品上市：{product_name} 重磅来袭",
        'follow_up': f"关于 {product_name}，想和您分享一些好消息",
        'newsletter': f"本月精选：{product_name} 独家特惠",
        're_engagement': f"好久不见！{product_name} 有新动态了"
    }
    
    title = titles.get(email_type, f"{product_name} - 诚邀您体验")
    
    content = f"""尊敬的客户：

您好！

我们很高兴向您介绍我们的明星产品——{product_name}。

{product_features}

这款产品专为{target_audience}打造，旨在为您提供{tone}的解决方案。

现在购买，尊享限时优惠！

立即行动，开启{product_name}之旅！

此致
敬礼

{product_name} 团队
{datetime.now().strftime('%Y年%m月%d日')}
"""
    
    return f"主题：{title}\n\n{content}"

@app.route('/templates', methods=['GET'])
def get_templates():
    """获取邮件模板"""
    templates = {
        'promotional': '促销邮件',
        'announcement': '新品公告',
        'follow_up': '跟进邮件',
        'newsletter': '电子通讯',
        're_engagement': '重新激活'
    }
    return jsonify(templates)

@app.route('/tones', methods=['GET'])
def get_tones():
    """获取语气选项"""
    tones = {
        'professional': '专业正式',
        'friendly': '亲切友好',
        'casual': '轻松随意',
        'urgent': '紧急促销'
    }
    return jsonify(tones)

if __name__ == '__main__':
    port = 8083  # 使用不同端口
    print(f"AI 邮件营销工具启动中...")
    print(f"端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
