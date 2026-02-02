#!/usr/bin/env python3
"""
Flask Web 应用模板
"""

from flask import Flask, render_template, request, jsonify
import logging
import os
from datetime import datetime

# 创建 Flask 应用
app = Flask(__name__)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.route('/')
def home():
    """首页"""
    return render_template('index.html', title='AI 工具箱')

@app.route('/api/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'AI 工具箱'
    })

@app.route('/api', methods=['GET', 'POST'])
def api():
    """API 接口"""
    if request.method == 'POST':
        data = request.json
        # 处理 POST 请求
        return jsonify({
            'success': True,
            'data': data
        })
    else:
        # 处理 GET 请求
        return jsonify({
            'success': True,
            'message': 'API is ready'
        })

@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({
        'success': False,
        'error': 'Not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    logging.error(f"Internal error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # 运行应用
    app.run(host='0.0.0.0', port=8080, debug=False)
