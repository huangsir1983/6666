# 🚀 QUICK_STARTS - 快速开始指南

**最后更新：** 2026-02-02 12:50（北京时间）
**会话ID：** session-20260202-0655
**目的：** 快速开始常用任务

---

## 📚 快速开始目录

1. [AI 工具箱](#-ai-工具箱)
2. [快速变现项目](#-快速变现项目)
3. [GitHub 使用](#-github-使用)
4. [平台发布](#-平台发布)
5. [记忆系统使用](#-记忆系统使用)

---

## 🛠️ AI 工具箱

### 启动 AI 工具箱（5 分钟）

```bash
# 克隆项目
git clone https://github.com/huangsir1983/6666.git
cd 6666

# 安装依赖
pip install flask requests

# 启动服务
python3 proxy_server_v2.py &    # 代理服务（8080）
python3 auth_system.py &        # 认证系统（8082）
python3 -m http.server 8081 & # HTTP 服务（8081）

# 访问应用
open http://localhost:8081/
```

### 注册用户（2 分钟）

```bash
curl -X POST http://localhost:8082/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "测试用户"
  }'
```

**返回：**
```json
{
  "message": "注册成功",
  "user_id": "uuid",
  "api_key": "your-api-key",
  "plan": "free"
}
```

---

## 💰 快速变现项目

### AI 邮件营销工具

```bash
# 进入项目目录
cd /root/.openclaw/workspace/ai_email_toolkit

# 启动服务
python3 app.py

# 访问工具
open http://localhost:8083/
```

### AI 产品描述生成器

```bash
# 进入项目目录
cd /root/.openclaw/workspace/ai_product_desc_toolkit

# 启动服务
python3 app.py

# 访问工具
open http://localhost:8084/
```

### AI 会议记录总结工具

```bash
# 进入项目目录
cd /root/.openclaw/workspace/ai_meeting_toolkit

# 启动服务
python3 app.py

# 访问工具
open http://localhost:8085/
```

### AI 社交媒体内容生成器

```bash
# 进入项目目录
cd /root/.openclaw/workspace/ai_social_toolkit

# 启动服务
python3 app.py

# 访问工具
open http://localhost:8086/
```

### AI SEO 内容生成器

```bash
# 进入项目目录
cd /root/.openclaw/workspace/ai_seo_toolkit

# 启动服务
python3 app.py

# 访问工具
open http://localhost:8087/
```

---

## 🌐 GitHub 使用

### 克隆仓库

```bash
# 克隆主项目
git clone https://github.com/huangsir1983/6666.git

# 克隆到指定目录
git clone https://github.com/huangsir1983/6666.git project-name
```

### 提交更改

```bash
# 添加所有文件
git add .

# 提交更改
git commit -m "feat: 添加新功能"

# 推送到远程
git push origin main
```

### 创建 Tag 和 Release

```bash
# 查看提交历史
git log --oneline

# 创建 Tag（使用完整的 SHA）
git tag v1.0.0 4bd4ff1349d8f9cf36ebd965b272fe7f06c7adac

# 推送 Tag
git push origin v1.0.0

# 创建 Release（使用 API）
python3 /tmp/create_github_release.py
```

### 使用 GitHub API

```python
import requests

# 认证
headers = {
    "Authorization": "token YOUR_TOKEN",
    "Accept": "application/vnd.github.v3+json"
}

# 获取用户信息
response = requests.get('https://api.github.com/user', headers=headers)
user = response.json()
print(f"用户名：{user.get('login')}")

# 获取仓库列表
response = requests.get('https://api.github.com/user/repos', headers=headers)
repos = response.json()
print(f"仓库数量：{len(repos)}")

# 创建 Release
release_data = {
    "tag_name": "v1.0.0",
    "target_commitish": "main",
    "name": "Release v1.0.0",
    "body": "Release notes",
    "draft": False,
    "prerelease": False
}
response = requests.post('https://api.github.com/repos/owner/repo/releases', headers=headers, json=release_data)
print(f"Release 状态码：{response.status_code}")
```

---

## 📢 平台发布

### 掘金发布文章（10 分钟）

**手动发布：**
1. 打开 https://juejin.cn/
2. 登录（完成图形验证码）
3. 点击 "+" → "发布文章"
4. 输入标题和内容
5. 选择分类和标签
6. 点击 "发布文章"

**自动化（需要 Cookie）：**
```python
import requests

url = 'https://api.juejin.cn/content_api/v1/article/publish'
headers = {
    'Cookie': 'YOUR_COOKIE',
    'Content-Type': 'application/json'
}
data = {
    'title': 'AI 工具箱 - 降低 AI 使用门槛',
    'content': '文章内容...',
    'category': '前端',
    'tags': ['Python', 'AI', 'Web 开发']
}
response = requests.post(url, headers=headers, json=data)
print(f"发布状态码：{response.status_code}")
```

### V2EX 发布帖子（5 分钟）

**手动发布：**
1. 打开 https://www.v2ex.com/
2. 登录
3. 点击 "+" → "写新帖"
4. 输入标题和内容
5. 选择节点
6. 点击 "发布"

**自动化（需要 Cookie）：**
```python
import requests

url = 'https://www.v2ex.com/api/topics/create'
headers = {
    'Cookie': 'YOUR_COOKIE',
    'Content-Type': 'application/x-www-form-urlencoded'
}
data = {
    'title': 'AI 工具箱 - 开源项目',
    'content': '帖子内容...',
    'node_name': 'python'
}
response = requests.post(url, headers=headers, data=data)
print(f"发布状态码：{response.status_code}")
```

### 知乎回答问题（10 分钟）

**手动回答：**
1. 打开 https://www.zhihu.com/
2. 搜索相关问题
3. 点击 "写回答"
4. 输入回答内容
5. 点击 "发布回答"

**自动化（需要 Cookie）：**
```python
import requests

url = 'https://www.zhihu.com/api/v4/answers'
headers = {
    'Cookie': 'YOUR_COOKIE',
    'Content-Type': 'application/json'
}
data = {
    'question_id': 'question-id',
    'content': '回答内容...',
    'anonymous': False
}
response = requests.post(url, headers=headers, json=data)
print(f"回答状态码：{response.status_code}")
```

---

## 🧠 记忆系统使用

### 新会话恢复（5 分钟）

```bash
# 进入工作目录
cd /root/.openclaw/workspace/memory_system/core

# 读取核心记忆
cat SESSION_MEMORY.md
cat TASKS.md
cat CONTEXT.md
cat DECISIONS.md
```

### 查看知识库

```bash
# 进入知识库目录
cd /root/.openclaw/workspace/memory_system/knowledge

# 查看知识库
cat KNOWLEDGE_BASE.md
cat LESSONS_LEARNED.md
```

### 查看技能库

```bash
# 进入技能库目录
cd /root/.openclaw/workspace/memory_system/skills

# 查看技能清单
cat SKILLS.md
cat CHEATSHEETS.md
cat QUICK_STARTS.md
```

### 备份记忆到 GitHub

```bash
# 运行备份脚本
python3 /root/.openclaw/workspace/backup_to_github.py

# 或者手动提交
cd /root/.openclaw/workspace/memory_system
git add .
git commit -m "Daily backup - YYYY-MM-DD"
git push origin main
```

---

## 📊 服务管理

### 启动所有服务（10 分钟）

```bash
# 启动代理服务
nohup python3 proxy_server_v2.py > proxy_v2.log 2>&1 &

# 启动认证系统
nohup python3 auth_system.py > auth_system.log 2>&1 &

# 启动 HTTP 服务
nohup python3 -m http.server 8081 > http_server.log 2>&1 &

# 启动调度器
nohup python3 daily_scheduler_v2.py > daily_scheduler.log 2>&1 &

# 启动快速变现项目
cd /root/.openclaw/workspace/ai_email_toolkit
nohup python3 app.py > ai_email.log 2>&1 &

cd /root/.openclaw/workspace/ai_meeting_toolkit
nohup python3 app.py > ai_meeting.log 2>&1 &

cd /root/.openclaw/workspace/ai_social_toolkit
nohup python3 app.py > ai_social.log 2>&1 &

cd /root/.openclaw/workspace/ai_seo_toolkit
nohup python3 app.py > ai_seo.log 2>&1 &
```

### 检查服务状态

```bash
# 检查所有 Python 服务
ps aux | grep -E "python3.*app.py|python3.*server" | grep -v grep

# 检查端口占用
netstat -tuln | grep -E "808[0-7]"

# 查看日志
tail -50 proxy_v2.log
tail -50 auth_system.log
tail -50 http_server.log
```

### 重启服务

```bash
# 找到进程 ID
PID=$(ps aux | grep "proxy_server_v2.py" | grep -v grep | awk '{print $2}')

# 杀死进程
kill $PID

# 重新启动
python3 proxy_server_v2.py &
```

---

## 🎯 推广流程

### 第一天：启动（2 小时）

1. **上午（1 小时）**
   - [ ] 发布 GitHub Release（已完成）
   - [ ] 发布 1 篇掘金文章
   - [ ] 发布 1 个 V2EX 帖子

2. **下午（1 小时）**
   - [ ] 回答 1 个知乎问题
   - [ ] 发布 1 篇掘金文章
   - [ ] 在社区分享项目链接

---

### 第一周：优化（5 小时）

1. **周一（1 小时）**
   - [ ] 回复所有评论和问题
   - [ ] 优化文章标题和内容
   - [ ] 发布第 2 篇掘金文章

2. **周二（1 小时）**
   - [ ] 发布第 2 个 V2EX 帖子
   - [ ] 回答 1 个知乎问题
   - [ ] 社交媒体分享项目

3. **周三（1 小时）**
   - [ ] 发布第 3 篇掘金文章
   - [ ] 优化项目 README
   - [ ] 录制短视频演示

4. **周四（1 小时）**
   - [ ] 回答 1 个知乎问题
   - [ ] 发布到其他平台（CSDN、简书）
   - [ ] 分析流量数据

5. **周五（1 小时）**
   - [ ] 总结本周数据
   - [ ] 收集用户反馈
   - [ ] 规划下周任务

---

## 💡 效率提升

### 时间管理

1. **番茄钟工作法** - 工作 25 分钟，休息 5 分钟
2. **批量处理** - 集中处理相似任务
3. **优先级排序** - 先做重要紧急的任务
4. **避免多任务** - 一次只做一件事

### 自动化

1. **脚本化重复任务** - 用脚本替代手动操作
2. **使用 Cron 定时** - 定时任务自动化
3. **使用 Git 自动化** - 版本控制和发布自动化
4. **使用 GitHub Actions** - CI/CD 自动化

---

## 📞 获取帮助

### 遇到问题？

1. **查看故障排查指南**
   ```bash
   cat /root/.openclaw/workspace/TROUBLESHOOTING.md
   ```

2. **查看常见问题**
   ```bash
   cat /root/.openclaw/workspace/FAQ.md
   ```

3. **查看知识库**
   ```bash
   cat /root/.openclaw/workspace/memory_system/knowledge/KNOWLEDGE_BASE.md
   ```

4. **查看经验教训**
   ```bash
   cat /root/.openclaw/workspace/memory_system/knowledge/LESSONS_LEARNED.md
   ```

---

## 📝 备注

### 重要提醒
1. **服务保持运行** - 确保所有服务正常运行
2. **定期备份** - 每天备份记忆系统到 GitHub
3. **及时更新** - 遇到新问题时更新知识库和经验库
4. **保持同步** - 使用 Git 保持代码和文档同步

### 成功指标
- **第 1 周：** GitHub Stars 50+, 文章阅读量 5,000+, 注册用户 20+
- **第 1 月：** GitHub Stars 200+, 文章阅读量 20,000+, 注册用户 100+
- **第 3 月：** GitHub Stars 500+, 文章阅读量 100,000+, 注册用户 500+

---

**最后更新：** 2026-02-02 12:50（北京时间）
**会话ID：** session-20260202-0655
**状态：** 🟢 快速开始指南完成
