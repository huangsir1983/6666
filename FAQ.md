# ❓ FAQ 常见问题解答

**项目：** AI 工具箱
**用途：** 用户常见问题解答
**安全：** 不含任何敏感信息

---

## 📋 目录

1. [快速开始](#快速开始)
2. [安装部署](#安装部署)
3. [API 使用](#api-使用)
4. [错误排查](#错误排查)
5. [高级配置](#高级配置)
6. [商业相关](#商业相关)

---

## 快速开始

### Q1: AI 工具箱是什么？

**A:** AI 工具箱是一个完整的 AI API 服务解决方案，包括：

- **Claude Code 代理服务** - 让 Claude Code 使用智谱 AI
- **用户认证系统** - API Key 管理和用量统计
- **应用工具套件** - 聊天、故事、代码生成等
- **自动化监控** - 服务状态监控

**核心价值：** 降低 AI 使用门槛，让开发者更方便地使用 AI 能力。

---

### Q2: 为什么需要 AI 工具箱？

**A:** 解决以下问题：

1. **API 格式不统一** - 不同 AI 厂商 API 格式不同
2. **成本高** - 直接使用商业 API 价格较高
3. **国内访问不稳定** - 国外 AI 在国内访问困难
4. **用户管理复杂** - 需要自己实现用户系统

AI 工具箱提供统一的 API 格式，降低使用门槛。

---

### Q3: 免费版真的免费吗？

**A:** 是的！免费版包括：

- ✅ 每天 100 次 API 调用
- ✅ 每月 1,000 次 API 调用
- ✅ 所有基础功能
- ✅ 无限使用应用工具

永久免费，无需信用卡！

---

## 安装部署

### Q4: 如何快速开始？

**A:** 只需要 3 步：

```bash
# 1. 克隆项目
git clone https://github.com/your-username/ai-toolkit.git
cd ai-toolkit

# 2. 安装依赖
pip install flask requests

# 3. 启动服务
python3 proxy_server_v2.py    # 代理服务
python3 auth_system.py         # 认证系统
python3 -m http.server 8081    # HTTP 服务
```

详细教程请查看文档。

---

### Q5: 需要什么系统要求？

**A:** 最低要求：

- **操作系统：** Linux / macOS / Windows
- **Python：** 3.7+
- **内存：** 512MB+
- **存储：** 100MB+

推荐配置：
- **内存：** 2GB+
- **CPU：** 2 核+
- **存储：** 1GB+

---

### Q6: 需要智谱 API Key 吗？

**A:** 需要！

如果你想自己部署，需要申请智谱 API Key：
1. 访问 https://open.bigmodel.cn
2. 注册账号并实名认证
3. 创建 API Key
4. 配置到项目中

如果你不想自己部署，可以使用我的在线服务（需要注册获取 API Key）。

---

### Q7: 部署到服务器怎么做？

**A:** 两种方式：

**方式 1：简单部署**
```bash
# SSH 到服务器
ssh user@your-server

# 克隆项目
git clone https://github.com/your-username/ai-toolkit.git
cd ai-toolkit

# 启动服务
nohup python3 proxy_server_v2.py > proxy.log 2>&1 &
```

**方式 2：使用 Gunicorn（推荐）**
```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务
gunicorn -w 4 -b 0.0.0.0:8080 proxy_server_v2:app
```

详细部署教程请查看视频教程。

---

### Q8: 如何让服务开机自启？

**A:** 使用 Systemd：

1. 创建 service 文件：
```ini
[Unit]
Description=AI API Proxy Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/project
ExecStart=/usr/bin/gunicorn -w 4 -b 0.0.0.0:8080 proxy_server_v2:app
Restart=always

[Install]
WantedBy=multi-user.target
```

2. 启用并启动：
```bash
sudo systemctl enable ai-api
sudo systemctl start ai-api
```

---

## API 使用

### Q9: 如何获取 API Key？

**A:** 两种方式：

**方式 1：使用我的在线服务**
```bash
curl -X POST http://localhost:8082/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "password123"
  }'
```

**方式 2：自己部署**
不需要 API Key，直接使用自己的智谱 API Key。

---

### Q10: 如何调用 API？

**A:** 使用标准 HTTP 请求：

```bash
curl -X POST http://localhost:8080/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 200,
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  }'
```

Python 示例：
```python
import requests

response = requests.post(
    "http://localhost:8080/v1/messages",
    headers={
        "Content-Type": "application/json",
        "X-API-Key": "YOUR_API_KEY"
    },
    json={
        "model": "claude-sonnet-4-5-20250929",
        "max_tokens": 200,
        "messages": [{"role": "user", "content": "你好"}]
    }
)

result = response.json()
print(result['content'][0]['text'])
```

---

### Q11: 支持哪些模型？

**A:** 支持所有 Claude 模型（映射到智谱 GLM-4.7）：

- `claude-haiku-4-5-20251001`
- `claude-sonnet-4-5-20250929`
- `claude-opus-4-5-20250929`

未来计划支持更多模型（文心一言、通义千问等）。

---

### Q12: 如何设置系统提示词？

**A:** 在 messages 数组中添加 system 角色：

```json
{
  "messages": [
    {"role": "system", "content": "你是一个专业的程序员"},
    {"role": "user", "content": "帮我写一个快速排序"}
  ]
}
```

---

### Q13: 如何控制输出长度？

**A:** 使用 `max_tokens` 参数：

```json
{
  "max_tokens": 100  // 最多 100 个 token
}
```

---

### Q14: 如何设置创造性程度？

**A:** 使用 `temperature` 参数（0-1）：

- `0.1` - 更保守，更确定
- `0.7` - 平衡（推荐）
- `0.9` - 更有创造性，更随机

---

### Q15: 免费版有多少次调用？

**A:** 免费版限制：
- 每天：100 次
- 每月：1,000 次

超过限制后，可以选择升级套餐：
- 基础版：¥99/月（500次/天）
- 专业版：¥299/月（2000次/天）
- 企业版：¥999/月（无限制）

---

### Q16: 如何查看使用量？

**A:** 调用量统计接口：

```bash
curl http://localhost:8082/auth/usage \
  -H "X-API-Key: YOUR_API_KEY"
```

返回：
```json
{
  "plan": "free",
  "daily_limit": 100,
  "daily_used": 50,
  "monthly_limit": 1000,
  "monthly_used": 500
}
```

---

## 错误排查

### Q17: 服务启动失败怎么办？

**A:** 常见原因和解决方法：

**1. 端口被占用**
```bash
# 查看端口占用
lsof -i :8080

# 或
netstat -tlnp | grep 8080

# 解决方法：修改端口或关闭占用进程
```

**2. 依赖未安装**
```bash
# 重新安装依赖
pip install flask requests

# 或使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install flask requests
```

**3. Python 版本过低**
```bash
# 检查 Python 版本
python3 --version

# 需要 3.7+
```

**4. 权限问题**
```bash
# 使用 sudo 运行（不推荐）
sudo python3 proxy_server_v2.py

# 或更改端口为 1024 以上
```

---

### Q18: API 调用失败怎么办？

**A:** 检查以下几点：

**1. API Key 是否正确**
```bash
# 验证 API Key
curl http://localhost:8082/auth/usage \
  -H "X-API-Key: YOUR_API_KEY"
```

**2. 服务是否正常运行**
```bash
# 健康检查
curl http://localhost:8080/health
curl http://localhost:8082/auth/health
```

**3. 网络连接是否正常**
```bash
# 测试连接
ping open.bigmodel.cn

# 测试 API
curl -X POST https://open.bigmodel.cn/api/paas/v4/chat/completions \
  -H "Authorization: Bearer YOUR_ZHIPU_API_KEY" \
  -d '{"model":"glm-4.7","messages":[{"role":"user","content":"hi"}]}'
```

**4. 请求格式是否正确**
- 检查 Content-Type 是否为 application/json
- 检查 X-API-Key 请求头是否存在
- 检查 JSON 格式是否正确

---

### Q19: 收到 401 错误怎么办？

**A:** 401 表示未授权，可能原因：

1. **API Key 无效** - 检查 API Key 是否正确
2. **API Key 过期** - 重新注册获取新的 API Key
3. **未提供 API Key** - 确保请求头包含 X-API-Key

---

### Q20: 收到 429 错误怎么办？

**A:** 429 表示请求过多，可能原因：

1. **超出免费额度** - 查看使用量，考虑升级套餐
2. **智谱 API 限流** - 添加请求间隔或升级智谱套餐

---

### Q21: 收到 500 错误怎么办？

**A:** 500 表示服务器内部错误，请：

1. 查看服务日志：
```bash
tail -f proxy_v2.log
```

2. 检查智谱 API 状态

3. 提交 Issue 或联系支持

---

## 高级配置

### Q22: 如何使用 Docker 部署？

**A:** 创建 Dockerfile：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "proxy_server_v2:app"]
```

构建和运行：
```bash
docker build -t ai-toolkit .
docker run -p 8080:8080 ai-toolkit
```

---

### Q23: 如何使用 Nginx 反向代理？

**A:** 配置 Nginx：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /auth/ {
        proxy_pass http://127.0.0.1:8082/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

### Q24: 如何配置 HTTPS？

**A:** 使用 Let's Encrypt：

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期已配置
```

---

### Q25: 如何使用数据库？

**A:** 支持多种数据库：

**MongoDB:**
```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['ai_api']
users = db['users']
```

**MySQL:**
```python
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    database='ai_api'
)
```

---

### Q26: 如何实现流式响应？

**A:** 修改代理服务：

```python
from flask import Response

@app.route('/v1/messages', methods=['POST'])
def proxy_messages():
    # ... 处理逻辑 ...

    def generate():
        response = requests.post(ZHIPU_API_URL, json=zhipu_data, stream=True)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    return Response(generate(), mimetype='text/event-stream')
```

---

## 商业相关

### Q27: 定价方案是什么？

**A:** 四种套餐：

| 套餐 | 价格 | 日调用 | 月调用 | 特性 |
|------|------|--------|--------|------|
| 免费版 | ¥0 | 100 | 1,000 | 基础功能 |
| 基础版 | ¥99/月 | 500 | 10,000 | 优先响应 |
| 专业版 | ¥299/月 | 2,000 | 100,000 | 专属支持 |
| 企业版 | ¥999/月 | 无限制 | 无限制 | SLA保证 |

---

### Q28: 如何升级套餐？

**A:** 调用升级接口：

```bash
curl -X POST http://localhost:8082/auth/upgrade \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "password",
    "plan": "basic"
  }'
```

或联系客服协助升级。

---

### Q29: 企业版有哪些额外服务？

**A:** 企业版包括：

- ✅ 无限制 API 调用
- ✅ 专用服务器实例
- ✅ 99.9% SLA 保证
- ✅ 7x24 专属客服
- ✅ 定制化开发
- ✅ 技术顾问服务
- ✅ 定期安全审计

---

### Q30: 可以定制开发吗？

**A:** 可以！提供以下服务：

- 企业聊天机器人
- 自动化工作流
- 数据分析工具
- 内容生成系统
- 任何 AI 相关需求

联系客服获取报价：contact@example.com

---

### Q31: 有技术支持吗？

**A:** 不同套餐有不同支持：

- **免费版：** 社区支持（GitHub Issues）
- **基础版：** 邮件支持（48小时内响应）
- **专业版：** 专属客服（24小时内响应）
- **企业版：** 7x24 在线支持

---

### Q32: 可以退款吗？

**A:** 退款政策：

- 7 天内不满意可全额退款
- 企业版支持 30 天退款
- 联系客服申请退款

---

## 其他问题

### Q33: 项目开源吗？

**A:** 是的！项目完全开源，MIT 许可证。

你可以：
- ✅ 自由部署和修改
- ✅ 用于商业项目
- ✅ 分享和分发
- ❌ 不能移除版权声明

GitHub: https://github.com/your-username/ai-toolkit

---

### Q34: 如何贡献代码？

**A:** 欢迎贡献！

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 开启 Pull Request

详细指南请查看 CONTRIBUTING.md。

---

### Q35: 如何联系？

**A:** 多种联系方式：

- **Email:** contact@example.com
- **微信:** AI_Toolbox_Official
- **GitHub Issues:** 项目 Issues 页面
- **QQ群:** 123456789

---

### Q36: 有教程吗？

**A:** 有多种教程：

- 📝 文档教程
- 🎥 视频教程（B站、YouTube）
- 📚 技术文章（掘金、知乎）
- 💬 社区讨论（V2EX）

---

### Q37: 未来有什么计划？

**A:** 未来计划：

- [ ] 更多 AI 模型支持
- [ ] 流式响应
- [ ] 移动端应用
- [ ] 插件系统
- [ ] 管理后台
- [ ] 多语言支持

欢迎提出建议！

---

## 总结

如果这个 FAQ 没有解答你的问题：

1. 查看完整文档
2. 提交 GitHub Issue
3. 联系客服

我们会尽快回复！

---

**最后更新：** 2026-02-02
**版本：** 1.0.0
