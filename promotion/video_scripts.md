# 🎥 视频脚本库

**用途：** 演示视频、教程视频的完整脚本
**安全：** 不含任何敏感信息，可安全使用

---

## 📹 视频 1：5分钟功能演示

**时长：** 5分钟
**类型：** 功能演示 + 项目介绍
**平台：** B站、YouTube、视频号

### 开场（0:00-0:30）
**画面：** 动态 Logo，背景音乐
**旁白：**
"大家好，欢迎来到小智的频道！
今天给大家介绍一个我花了2周时间开发的项目：AI 工具箱"

**画面：** 项目 Logo + 标题
**旁白：**
"AI 工具箱是一个完整的 AI API 服务解决方案
让你可以方便地使用智谱 AI，甚至兼容 Claude Code"

---

### 项目介绍（0:30-1:30）
**画面：** 电脑屏幕，展示项目主页
**旁白：**
"首先，让我介绍一下这个项目的核心功能

第一个是 Claude Code 代理服务
你可以直接在 Claude Code 中使用智谱 AI
不需要复杂的配置"

**画面：** 演示 Claude Code 配置
**旁白：**
"只需要设置两个环境变量
就可以让 Claude Code 完美支持智谱 AI"

**画面：** 展示代码
```bash
export ANTHROPIC_API_URL=http://localhost:8080
export ANTHROPIC_API_KEY=your-api-key
```

**旁白：**
"就这么简单！"

---

### 核心功能演示（1:30-3:30）
**画面：** 切换到聊天界面
**旁白：**
"第二个功能是用户认证系统
你可以注册账号，获取自己的 API Key
支持用量统计和套餐升级"

**画面：** 演示注册流程
**旁白：**
"注册非常简单，只需要邮箱和密码
注册后就能得到 API Key，免费版每天可以调用 100 次"

**画面：** 演示聊天功能
**旁白：**
"第三个功能是完整的应用套件
包括智能聊天助手、故事生成器、代码生成器等"

**画面：** 与 AI 对话
**旁白：**
"你看，这是智能聊天助手
我可以问它任何问题，它都能给出很好的回答"

**画面：** 展示故事生成器
**旁白：**
"这是故事生成器，AI 可以帮你创作各种类型的故事"

**画面：** 展示代码生成器
**旁白：**
"这是代码生成器，需要写代码的时候，AI 可以帮你快速完成"

---

### 快速开始（3:30-4:30）
**画面：** 终端界面
**旁白：**
"那么，如何开始使用呢？

首先，克隆项目到本地
然后安装依赖，启动服务
最后注册用户，就可以开始使用了"

**画面：** 演示命令
```bash
git clone https://github.com/your-username/ai-toolkit.git
cd ai-toolkit
pip install flask requests
python3 proxy_server_v2.py
```

**旁白：**
"整个过程不到 5 分钟，非常简单"

---

### 项目亮点（4:30-5:00）
**画面：** 总结页面
**旁白：**
"最后，让我总结一下这个项目的亮点

第一，完全开源，你可以自由部署和修改
第二，免费版每天可以调用 100 次
第三，国内访问稳定，不需要翻墙
第四，兼容 Claude Code，降低使用门槛"

**画面：** GitHub 页面
**旁白：**
"项目已经开源在 GitHub
链接在视频下方
如果你觉得这个项目对你有帮助
欢迎给个 Star ⭐

如果喜欢这个视频，请点赞、收藏、转发
关注我，获取更多 AI 开发相关内容

我们下期再见，拜拜！"

---

## 📹 视频 2：API 调用教程

**时长：** 8分钟
**类型：** 教程，详细讲解
**平台：** B站、CSDN视频

### 开场（0:00-0:45）
**画面：** 录屏，展示项目结构
**旁白：**
"大家好，今天我要详细讲解如何使用 AI 工具箱的 API

首先，确保你已经克隆了项目并安装了依赖
如果还没有，可以看上一个视频"

**画面：** README.md
**旁白：**
"详细的使用说明都在 README.md 里
我会在视频里一步步讲解"

---

### 注册用户（0:45-2:00）
**画面：** 终端，启动认证服务
**旁白：**
"首先，启动认证系统
这个服务负责用户管理和 API Key 管理"

**画面：** 演示注册
```bash
curl -X POST http://localhost:8082/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**旁白：**
"使用这个命令注册用户
你会得到一个 API Key，保存好这个 Key"

**画面：** 响应结果
```json
{
  "message": "Registration successful",
  "api_key": "your-api-key-here"
}
```

**旁白：**
"这个 API Key 就是你后续调用 API 时的凭证
注意保护好它，不要泄露给其他人"

---

### API 调用基础（2:00-4:00）
**画面：** 终端，启动代理服务
**旁白：**
"接下来，启动代理服务
这个服务负责将请求转换并发送到智谱 AI"

**画面：** 展示 API 端点
**旁白：**
"主要的 API 端点是 /v1/messages
这个端点兼容 Anthropic API 的格式"

**画面：** 最简单的调用
```bash
curl -X POST http://localhost:8080/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 100,
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  }'
```

**旁白：**
"这是一个最基本的 API 调用
你需要提供：
1. X-API-Key 请求头，包含你的 API Key
2. 模型名称，这里使用 claude-sonnet-4-5-20250929
3. max_tokens，限制响应长度
4. messages，对话历史"

---

### 参数详解（4:00-6:00）
**画面：** 分屏展示代码和解释
**旁白：**
"现在详细解释每个参数

model 参数支持所有 Claude 模型：
- claude-haiku-4-5-20251001
- claude-sonnet-4-5-20250929
- claude-opus-4-5-20250929

这些模型会自动映射到智谱 AI 的 GLM-4.7"

**画面：** messages 结构
**旁白：**
"messages 是一个数组，包含对话历史
每个消息都有 role 和 content
role 可以是：user、assistant、system
content 就是消息内容"

**画面：** 系统提示词示例
```json
{
  "messages": [
    {"role": "system", "content": "你是一个专业的程序员"},
    {"role": "user", "content": "帮我写一个快速排序"}
  ]
}
```

**旁白：**
"你可以添加 system 角色的消息来设置系统提示词
这会影响 AI 的回答风格"

---

### Python 调用示例（6:00-7:00）
**画面：** VS Code，编写 Python 代码
**旁白：**
"接下来，演示如何在 Python 中调用 API"

**画面：** 完整代码
```python
import requests

API_KEY = "your-api-key"
API_URL = "http://localhost:8080/v1/messages"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

data = {
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 200,
    "messages": [
        {"role": "user", "content": "你好，请介绍一下你自己"}
    ]
}

response = requests.post(API_URL, headers=headers, json=data)
result = response.json()

print(result['content'][0]['text'])
```

**旁白：**
"使用 requests 库非常简单
首先设置请求头，包含 API Key
然后构造请求数据
最后发送请求并处理响应"

---

### 错误处理（7:00-8:00）
**画面：** 错误处理代码
```python
try:
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        content = result['content'][0]['text']
        print(content)
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

except Exception as e:
    print(f"Exception: {e}")
```

**旁白：**
"一定要做好错误处理
检查响应状态码
捕获可能的异常
这样你的应用会更稳定"

**画面：** 总结页面
**旁白：**
"以上就是 API 调用的完整教程
更多细节可以查看项目文档

如果你有任何问题，欢迎在评论区留言
或提交 GitHub Issue

下期视频我会讲解如何部署到生产环境
敬请期待！

感谢观看，别忘了点赞和订阅！"

---

## 📹 视频 3：部署教程

**时长：** 10分钟
**类型：** 实战教程
**平台：** B站、YouTube

### 开场（0:00-1:00）
**画面：** 云服务器控制台
**旁白：**
"大家好，今天我要讲解如何将 AI 工具箱部署到服务器上

我以阿里云为例，其他云服务器类似

首先，你需要准备：
1. 一台云服务器（推荐 2核4G）
2. 一个域名（可选）
3. 基本的 Linux 操作能力"

---

### 服务器准备（1:00-2:30）
**画面：** SSH 连接
**旁白：**
"首先，连接到你的服务器
使用 SSH 命令"

**画面：** 安装依赖
```bash
# 更新系统
sudo apt update

# 安装 Python 和 pip
sudo apt install python3 python3-pip

# 安装 Git
sudo apt install git

# 创建项目目录
mkdir ~/ai-toolkit
cd ~/ai-toolkit
```

**旁白：**
"安装必要的软件包
Python、pip、Git 都需要"

---

### 项目部署（2:30-4:00）
**画面：** 克隆项目
```bash
# 克隆项目
git clone https://github.com/your-username/ai-toolkit.git
cd ai-toolkit

# 安装依赖
pip3 install flask requests gunicorn
```

**旁白：**
"克隆项目到服务器
安装 Python 依赖
gunicorn 用于生产环境"

**画面：** 配置文件
**旁白：**
"创建配置文件 config.py
设置你的智谱 API Key"

```python
# config.py
ZHIPU_API_KEY = "your-zhipu-api-key"
```

---

### 使用 Gunicorn 启动（4:00-5:30）
**画面：** 启动命令
```bash
# 启动代理服务
gunicorn -w 4 -b 0.0.0.0:8080 proxy_server_v2:app

# 启动认证服务
gunicorn -w 4 -b 0.0.0.0:8082 auth_system:app

# 启动 HTTP 服务
nohup python3 -m http.server 8081 > http.log 2>&1 &
```

**旁白：**
"使用 gunicorn 启动服务
-w 4 表示使用 4 个工作进程
-b 指定绑定的地址和端口"

---

### Systemd 自动启动（5:30-7:00）
**画面：** 创建 service 文件
**旁白：**
"为了让服务自动启动，使用 systemd

创建 /etc/systemd/system/ai-api.service"

```ini
[Unit]
Description=AI API Proxy Service
After=network.target

[Service]
User=www-data
WorkingDirectory=/home/user/ai-toolkit
ExecStart=/usr/bin/gunicorn -w 4 -b 0.0.0.0:8080 proxy_server_v2:app
Restart=always

[Install]
WantedBy=multi-user.target
```

**旁白：**
"配置服务
启动和开机自启"

```bash
sudo systemctl enable ai-api
sudo systemctl start ai-api
```

---

### Nginx 反向代理（7:00-8:00）
**画面：** Nginx 配置
**旁白：**
"使用 Nginx 做反向代理
这样可以使用 80/443 端口"

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

    location / {
        proxy_pass http://127.0.0.1:8081/;
    }
}
```

---

### 监控和日志（8:00-9:00）
**画面：** 日志文件
**旁白：**
"配置日志记录
所有服务的日志都会写入文件

使用 journalctl 查看 systemd 服务日志"
```bash
sudo journalctl -u ai-api -f
```

**画面：** 监控脚本
**旁白：**
"可以设置定时任务，定期检查服务状态
我已经提供了 scheduler.py 自动监控脚本"

---

### SSL 证书（9:00-10:00）
**画面：** Certbot
**旁白：**
"如果你有域名，可以使用 Let's Encrypt 免费 SSL 证书

使用 certbot 工具自动配置"

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

**旁白：**
"证书会自动续期
你的服务就支持 HTTPS 了"

**画面：** 总结
**旁白：**
"部署完成！
现在你可以通过域名访问你的 AI API 服务

如果有任何问题，欢迎留言
下期视频我会讲解更多高级功能

感谢观看，别忘了点赞订阅！"

---

**创建时间：** 2026-02-02
**用途：** 视频拍摄和制作
**状态：** 可安全使用
