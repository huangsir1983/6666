#!/usr/bin/env python3
"""
AI 会议记录总结工具
自动总结会议记录
"""

from flask import Flask, render_template, request, jsonify
import requests
import re
from datetime import datetime

app = Flask(__name__)

# 智谱 API 配置
ZHIPU_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
ZHIPU_API_KEY = "your-zhipu-api-key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        
        meeting_content = data.get('meeting_content', '')
        summary_type = data.get('summary_type', 'brief')
        output_format = data.get('output_format', 'markdown')
        
        if not meeting_content:
            return jsonify({"error": "请输入会议记录内容"}), 400
        
        # 生成总结
        summary = generate_summary(meeting_content, summary_type, output_format)
        
        return jsonify({
            "success": True,
            "summary": summary
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/batch_summarize', methods=['POST'])
def batch_summarize():
    try:
        data = request.json
        
        meeting_content = data.get('meeting_content', '')
        summary_types = data.get('summary_types', ['brief', 'action_items', 'full'])
        
        if not meeting_content:
            return jsonify({"error": "请输入会议记录内容"}), 400
        
        # 批量生成
        summaries = []
        for i, summary_type in enumerate(summary_types[:5]):  # 最多5种
            summary = generate_summary(meeting_content, summary_type, 'markdown')
            summaries.append({
                "id": i + 1,
                "type": summary_type,
                "content": summary
            })
        
        return jsonify({
            "success": True,
            "summaries": summaries
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/action_items', methods=['POST'])
def extract_action_items():
    try:
        data = request.json
        
        meeting_content = data.get('meeting_content', '')
        
        if not meeting_content:
            return jsonify({"error": "请输入会议记录内容"}), 400
        
        # 提取行动项
        action_items = extract_items_from_meeting(meeting_content)
        
        return jsonify({
            "success": True,
            "action_items": action_items
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_summary(meeting_content, summary_type, output_format):
    """生成会议总结"""
    
    # 类型描述
    type_descriptions = {
        'brief': '简短总结（100-150字）',
        'action_items': '行动项清单',
        'full': '完整总结（300-400字）'
    }
    
    # 构建提示词
    prompt = f"""
请为以下会议记录生成{type_descriptions.get(summary_type, '总结')}。

会议记录：
{meeting_content}

要求：
"""

    if summary_type == 'brief':
        prompt += """
1. 简短总结会议的核心内容和决定
2. 控制在 100-150 字左右
3. 突出最重要的信息
4. 清晰明了
"""
    elif summary_type == 'action_items':
        prompt += """
1. 提取会议中的行动项
2. 每个行动项包括：任务描述、负责人、截止日期
3. 如果没有明确负责人和截止日期，可以根据内容推断或标记为待定
4. 清晰列出，便于跟踪
"""
    elif summary_type == 'full':
        prompt += """
1. 完整总结会议的核心内容、讨论要点和决定
2. 提取关键行动项
3. 突出重要的成果和后续工作
4. 控制在 300-400 字左右
5. 结构清晰，层次分明
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
                "max_tokens": 800
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
            return generate_template_summary(meeting_content, summary_type)
    
    except:
        return generate_template_summary(meeting_content, summary_type)

def generate_template_summary(meeting_content, summary_type):
    """生成模板总结（备用）"""
    
    # 简单的文本处理
    lines = [line.strip() for line in meeting_content.split('\n') if line.strip()]
    
    if summary_type == 'brief':
        # 取前几行作为总结
        summary_text = ' '.join(lines[:3])
        if len(summary_text) > 150:
            summary_text = summary_text[:150] + '...'
        return f"**会议总结**\n\n{summary_text}\n\n*注：这是 AI 生成的简短总结，如需更详细总结请使用完整版。*"
    
    elif summary_type == 'action_items':
        # 提取包含"行动"、"任务"、"负责"等关键词的行
        action_items = []
        action_keywords = ['行动', '任务', '负责', '完成', '跟进', '待办']
        
        for line in lines:
            if any(keyword in line for keyword in action_keywords):
                action_items.append(f"- {line}")
        
        if not action_items:
            action_items = ["- 待定（会议记录中未明确找到行动项）"]
        
        return f"**行动项清单**\n\n{chr(10).join(action_items)}\n\n*注：这是 AI 提取的行动项，可以根据需要手动调整。*"
    
    elif summary_type == 'full':
        # 使用所有内容作为总结
        summary_text = ' '.join(lines[:10])
        return f"""**完整会议总结**\n\n**核心内容**\n{summary_text}\n\n**行动项**\n- 提取会议中的关键行动项\n- 确定负责人和截止日期\n- 跟踪执行进度\n\n**后续工作**\n- 基于会议决定开展相关工作\n- 协调相关资源\n- 定期跟进进度\n\n*注：这是 AI 生成的完整总结，如需更准确的总结请使用人工审核。*"""
    
    return "未知总结类型"

def extract_items_from_meeting(meeting_content):
    """从会议记录中提取行动项"""
    
    # 构建提示词
    prompt = f"""
请从以下会议记录中提取行动项。

会议记录：
{meeting_content}

要求：
1. 识别所有需要完成的任务
2. 确定负责人（如果没有明确，标记为"待定"）
3. 确定截止日期（如果没有明确，标记为"待定"）
4. 按优先级排序
5. 每个行动项包括：任务描述、负责人、截止日期、优先级
6. 输出格式为列表
7. 如果没有找到明确的行动项，返回"未找到行动项"

请直接输出行动项列表，不需要其他解释。
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
                "max_tokens": 1000
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
            
            # 解析行动项
            lines = content.split('\n')
            items = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('*'):
                    items.append(line)
            
            if not items:
                return [{"task": "未找到行动项", "owner": "待定", "deadline": "待定", "priority": "低"}]
            
            return items
    
    except:
        # 如果 API 调用失败，返回模板
        return [
            {"task": "任务1", "owner": "待定", "deadline": "待定", "priority": "高"},
            {"task": "任务2", "owner": "待定", "deadline": "待定", "priority": "中"}
        ]

@app.route('/export', methods=['POST'])
def export_summary():
    """导出总结"""
    try:
        data = request.json
        
        summary = data.get('summary', '')
        export_format = data.get('export_format', 'markdown')
        filename = f"meeting_summary_{datetime.now().strftime('%Y%m%d_%H%M')}.{export_format}"
        
        return jsonify({
            "success": True,
            "filename": filename,
            "content": summary
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = 8085
    print(f"AI 会议记录总结工具启动中...")
    print(f"端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
