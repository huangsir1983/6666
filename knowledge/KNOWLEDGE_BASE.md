# 📚 KNOWLEDGE_BASE - 知识库

**最后更新：** 2026-02-02 12:30（北京时间）
**会话ID：** session-20260202-0655
**目的：** 记录技术和业务知识

---

## 🐍 技术知识

### Python Web 开发

**Flask 框架**
- **快速开始：** `from flask import Flask, render_template, request, jsonify`
- **路由定义：** `@app.route('/')` 装饰器
- **请求处理：** `request.form`, `request.json`, `request.args`
- **模板渲染：** `render_template('index.html')`
- **JSON 响应：** `jsonify({'success': True})`

**最佳实践：**
- 使用蓝图（Blueprint）组织大型应用
- 使用环境变量管理配置
- 使用 .flaskenv 文件存储敏感信息
- 使用 g 对象在请求间共享数据

---

### Git 版本控制

**常用命令：**
- `git init` - 初始化仓库
- `git add .` - 添加所有文件
- `git commit -m "message"` - 提交更改
- `git push origin main` - 推送到远程
- `git pull origin main` - 从远程拉取

**分支管理：**
- `git branch` - 查看所有分支
- `git branch new-branch` - 创建新分支
- `git checkout new-branch` - 切换到新分支
- `git merge other-branch` - 合并分支
- `git branch -d old-branch` - 删除分支

**历史查看：**
- `git log` - 查看提交历史
- `git log --oneline` - 简洁的提交历史
- `git show commit-id` - 查看特定提交
- `git diff` - 查看未提交的更改

---

### Docker 容器化

**常用命令：**
- `docker build -t image-name .` - 构建镜像
- `docker run -p 8080:8080 image-name` - 运行容器
- `docker ps` - 查看运行中的容器
- `docker stop container-id` - 停止容器
- `docker logs container-id` - 查看容器日志

**Dockerfile：**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "app.py"]
```

---

### Systemd 服务管理

**常用命令：**
- `systemctl start service-name` - 启动服务
- `systemctl stop service-name` - 停止服务
- `systemctl restart service-name` - 重启服务
- `systemctl status service-name` - 查看服务状态
- `systemctl enable service-name` - 开机自启

**Service 文件：**
```ini
[Unit]
Description=My Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

### HTTP 请求

**Requests 库：**
- `requests.get('url')` - GET 请求
- `requests.post('url', json=data)` - POST 请求（JSON）
- `requests.put('url', data=data)` - PUT 请求
- `requests.delete('url')` - DELETE 请求

**请求头：**
```python
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token',
    'User-Agent': 'My App'
}
response = requests.get('url', headers=headers)
```

**超时和重试：**
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount('https://', adapter)
```

---

## 🌐 工具知识

### GitHub API

**认证：**
- `Authorization: token YOUR_TOKEN`
- `Authorization: Bearer YOUR_TOKEN`

**常用端点：**
- `GET /user` - 获取用户信息
- `GET /user/repos` - 获取仓库列表
- `POST /repos/:owner/:repo/git/tags` - 创建 Tag
- `POST /repos/:owner/:repo/releases` - 创建 Release

**示例：**
```python
import requests

headers = {
    'Authorization': 'token YOUR_TOKEN',
    'Accept': 'application/vnd.github.v3+json'
}

# 获取用户信息
response = requests.get('https://api.github.com/user', headers=headers)

# 创建 Release
data = {
    'tag_name': 'v1.0.0',
    'name': 'Release v1.0.0',
    'body': 'Release notes',
    'draft': False,
    'prerelease': False
}
response = requests.post(url, headers=headers, json=data)
```

---

### 掘金 API

**基础 URL：** `https://api.juejin.cn/content_api`

**常用端点：**
- `POST /v1/article/query_list` - 查询文章列表
- `POST /v1/article/publish` - 发布文章
- `POST /v1/article/draft` - 创建草稿
- `GET /v1/article/query_detail` - 获取文章详情

**示例：**
```python
import requests

base_url = 'https://api.juejin.cn/content_api'
headers = {
    'Content-Type': 'application/json'
}

# 发布文章
url = f"{base_url}/v1/article/publish"
data = {
    'title': '文章标题',
    'content': '文章内容',
    'cover_image': '封面图片 URL',
    'category': '前端',
    'tags': ['Python', 'Web 开发']
}
response = requests.post(url, headers=headers, json=data)
```

---

### V2EX API

**基础 URL：** `https://www.v2ex.com/api`

**常用端点：**
- `POST /login` - 登录
- `POST /create` - 创建主题
- `POST /reply` - 回复主题
- `GET /member/:username` - 获取用户信息

**示例：**
```python
import requests

base_url = 'https://www.v2ex.com/api'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# 创建主题
url = f"{base_url}/create"
data = {
    'title': '主题标题',
    'content': '主题内容',
    'node_name': 'python'
}
response = requests.post(url, headers=headers, data=data)
```

---

### 知乎 API

**基础 URL：** `https://www.zhihu.com/api`

**常用端点：**
- `POST /oauth2/sign_in` - 登录
- `POST /comments` - 添加评论
- `POST /answers` - 添加回答

**示例：**
```python
import requests

base_url = 'https://www.zhihu.com/api'
headers = {
    'Content-Type': 'application/json'
}

# 添加回答
url = f"{base_url}/answers"
data = {
    'question_id': 'question-id',
    'content': '回答内容'
}
response = requests.post(url, headers=headers, json=data)
```

---

## 💡 开发经验

### 调试技巧

1. **使用 print 调试：**
   - 在关键位置添加 `print()` 语句
   - 打印变量值、类型、长度
   - 确认代码执行流程

2. **使用 logging：**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   logging.debug('Debug message')
   ```

3. **使用 try-except：**
   ```python
   try:
       # 可能出错的代码
       pass
   except Exception as e:
       print(f"Error: {e}")
   ```

4. **使用 pdb 调试器：**
   ```bash
   python3 -m pdb script.py
   ```

---

### 性能优化

1. **使用缓存：**
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def expensive_function(x):
       return x * x
   ```

2. **使用并发：**
   ```python
   from concurrent.futures import ThreadPoolExecutor
   
   with ThreadPoolExecutor(max_workers=4) as executor:
       results = list(executor.map(function, range(10)))
   ```

3. **优化数据库查询：**
   - 使用索引
   - 避免全表扫描
   - 使用批量查询

---

### 错误处理

1. **HTTP 请求错误：**
   ```python
   try:
       response = requests.get('https://api.example.com')
       response.raise_for_status()
   except requests.exceptions.RequestException as e:
       print(f"Request failed: {e}")
   ```

2. **JSON 解析错误：**
   ```python
   try:
       data = json.loads(response.text)
   except json.JSONDecodeError as e:
       print(f"JSON decode error: {e}")
   ```

3. **文件操作错误：**
   ```python
   try:
       with open('file.txt', 'r') as f:
           content = f.read()
   except IOError as e:
       print(f"File read error: {e}")
   ```

---

## 🎯 快速参考

### Python 快速开始
```python
# Flask 应用
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({'message': 'Hello World'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### Git 快速开始
```bash
# 初始化仓库
git init

# 提交所有文件
git add .
git commit -m "Initial commit"

# 添加远程仓库
git remote add origin https://github.com/username/repo.git

# 推送到远程
git push -u origin main
```

### Docker 快速开始
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## 📝 备注

### 重要提示
1. **定期更新知识库** - 每次遇到新问题都记录
2. **分类清晰** - 按技术栈、工具、平台分类
3. **实用优先** - 只记录常用的知识
4. **示例丰富** - 每个知识都附带示例代码

### 知识来源
- 官方文档
- 技术博客
- Stack Overflow
- GitHub Issues
- 实际开发经验

---

**最后更新：** 2026-02-02 12:30（北京时间）
**会话ID：** session-20260202-0655
**状态：** 🟢 知识库完成
