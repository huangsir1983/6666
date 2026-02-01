#!/usr/bin/env python3
"""
用户认证系统 - API Key 管理
支持用户注册、登录、API Key 生成和使用量统计
"""

import json
import uuid
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# 数据库文件
USERS_DB = "users.json"
API_USAGE_DB = "api_usage.json"

# 定价配置
PRICING = {
    "free": {"daily_limit": 100, "monthly_limit": 1000, "price": 0},
    "basic": {"daily_limit": 500, "monthly_limit": 10000, "price": 99},
    "pro": {"daily_limit": 2000, "monthly_limit": 100000, "price": 299},
    "enterprise": {"daily_limit": -1, "monthly_limit": -1, "price": 999}  # -1 表示无限制
}


def load_json(filename):
    """加载 JSON 文件"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_json(filename, data):
    """保存 JSON 文件"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def hash_password(password):
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_api_key():
    """生成 API Key"""
    return str(uuid.uuid4()).replace('-', '')


@app.route('/auth/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name', '')

    if not email or not password:
        return jsonify({"error": "邮箱和密码不能为空"}), 400

    users = load_json(USERS_DB)

    if email in users:
        return jsonify({"error": "邮箱已注册"}), 400

    # 创建用户
    user_id = str(uuid.uuid4())
    api_key = generate_api_key()

    users[email] = {
        "user_id": user_id,
        "email": email,
        "name": name,
        "password": hash_password(password),
        "api_key": api_key,
        "plan": "free",  # 默认免费版
        "created_at": datetime.now().isoformat(),
        "api_usage": {
            "daily": {"count": 0, "date": datetime.now().strftime("%Y-%m-%d")},
            "monthly": {"count": 0, "month": datetime.now().strftime("%Y-%m")}
        }
    }

    save_json(USERS_DB, users)

    return jsonify({
        "message": "注册成功",
        "user_id": user_id,
        "api_key": api_key,
        "plan": "free"
    }), 201


@app.route('/auth/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "邮箱和密码不能为空"}), 400

    users = load_json(USERS_DB)

    if email not in users:
        return jsonify({"error": "用户不存在"}), 401

    user = users[email]

    if user['password'] != hash_password(password):
        return jsonify({"error": "密码错误"}), 401

    return jsonify({
        "message": "登录成功",
        "user_id": user['user_id'],
        "api_key": user['api_key'],
        "plan": user['plan'],
        "name": user['name']
    }), 200


@app.route('/auth/api-key', methods=['POST'])
def regenerate_api_key():
    """重新生成 API Key"""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    users = load_json(USERS_DB)

    if email not in users:
        return jsonify({"error": "用户不存在"}), 401

    user = users[email]

    if user['password'] != hash_password(password):
        return jsonify({"error": "密码错误"}), 401

    # 重新生成 API Key
    new_api_key = generate_api_key()
    users[email]['api_key'] = new_api_key

    save_json(USERS_DB, users)

    return jsonify({
        "message": "API Key 已更新",
        "api_key": new_api_key
    }), 200


@app.route('/auth/usage', methods=['GET'])
def get_usage():
    """获取使用量统计"""
    api_key = request.headers.get('X-API-Key')

    if not api_key:
        return jsonify({"error": "缺少 API Key"}), 401

    users = load_json(USERS_DB)
    user = None

    for email, u in users.items():
        if u['api_key'] == api_key:
            user = u
            break

    if not user:
        return jsonify({"error": "无效的 API Key"}), 401

    plan = PRICING[user['plan']]
    usage = user['api_usage']

    return jsonify({
        "plan": user['plan'],
        "daily_limit": plan['daily_limit'],
        "daily_used": usage['daily']['count'],
        "daily_remaining": plan['daily_limit'] - usage['daily']['count'] if plan['daily_limit'] > 0 else "无限制",
        "monthly_limit": plan['monthly_limit'],
        "monthly_used": usage['monthly']['count'],
        "monthly_remaining": plan['monthly_limit'] - usage['monthly']['count'] if plan['monthly_limit'] > 0 else "无限制"
    }), 200


@app.route('/auth/upgrade', methods=['POST'])
def upgrade_plan():
    """升级套餐"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    plan = data.get('plan')

    if plan not in PRICING:
        return jsonify({"error": "无效的套餐"}), 400

    users = load_json(USERS_DB)

    if email not in users:
        return jsonify({"error": "用户不存在"}), 401

    user = users[email]

    if user['password'] != hash_password(password):
        return jsonify({"error": "密码错误"}), 401

    # 更新套餐
    users[email]['plan'] = plan
    save_json(USERS_DB, users)

    return jsonify({
        "message": f"已升级到 {plan} 套餐",
        "plan": plan,
        "price": PRICING[plan]['price']
    }), 200


@app.route('/auth/plans', methods=['GET'])
def get_plans():
    """获取所有套餐信息"""
    return jsonify(PRICING), 200


@app.route('/auth/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({"status": "ok", "service": "auth"}), 200


if __name__ == '__main__':
    print("=" * 60)
    print("用户认证系统启动中...")
    print(f"端口: 8082")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8082, debug=False)
