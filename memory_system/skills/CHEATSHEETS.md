# 📋 CHEATSHEETS - 速查表

**最后更新：** 2026-02-02 12:45（北京时间）
**会话ID：** session-20260202-0655
**目的：** 常用命令和代码片段的快速参考

---

## 🐍 Python

### Flask Web 开发

```python
# 快速启动
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    return jsonify({'success': True, 'data': data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### Requests HTTP 请求

```python
import requests

# GET 请求
response = requests.get('https://api.example.com/data')
data = response.json()

# POST 请求（JSON）
payload = {'key': 'value'}
response = requests.post('https://api.example.com/data', json=payload)

# POST 请求（表单）
payload = {'key1': 'value1', 'key2': 'value2'}
response = requests.post('https://api.example.com/data', data=payload)

# 带请求头的请求
headers = {'Authorization': 'Bearer token', 'Content-Type': 'application/json'}
response = requests.get('https://api.example.com/data', headers=headers)

# 超时设置
response = requests.get('https://api.example.com/data', timeout=10)

# 会话管理
session = requests.Session()
response = session.get('https://api.example.com/login')
response = session.get('https://api.example.com/data')  # 使用 Cookie
```

### JSON 处理

```python
import json

# 读取 JSON 文件
with open('data.json', 'r') as f:
    data = json.load(f)

# 写入 JSON 文件
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# JSON 字符串转对象
data = json.loads('{"key": "value"}')

# 对象转 JSON 字符串
json_str = json.dumps(data, ensure_ascii=False)

# 美化 JSON 输出
print(json.dumps(data, indent=2))
```

### 日期时间处理

```python
from datetime import datetime, timedelta

# 当前时间
now = datetime.now()
print(f"当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}")

# 时间计算
tomorrow = now + timedelta(days=1)
last_week = now - timedelta(weeks=1)

# 字符串转时间
date_str = '2026-02-02'
date_obj = datetime.strptime(date_str, '%Y-%m-%d')

# 时间转字符串
date_str = date_obj.strftime('%Y-%m-%d')
```

### 文件操作

```python
# 读取文件
with open('file.txt', 'r') as f:
    content = f.read()

# 写入文件
with open('file.txt', 'w') as f:
    f.write('Hello World!')

# 追加写入
with open('file.txt', 'a') as f:
    f.write('\nNew line')

# 文件是否存在
import os
if os.path.exists('file.txt'):
    print("文件存在")

# 删除文件
os.remove('file.txt')

# 遍历目录
for root, dirs, files in os.walk('/path/to/dir'):
    for file in files:
        print(os.path.join(root, file))
```

---

## 🌐 Git

### 常用命令

```bash
# 初始化仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Commit message"

# 查看状态
git status

# 查看日志
git log
git log --oneline  # 简洁的日志
git log --graph    # 图形化日志

# 查看分支
git branch

# 创建分支
git branch new-branch

# 切换分支
git checkout new-branch

# 合并分支
git merge other-branch

# 删除分支
git branch -d old-branch

# 拉取更新
git pull origin main

# 推送更新
git push origin main

# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin https://github.com/username/repo.git
```

### 高级操作

```bash
# 回退到特定版本
git reset --hard commit-id

# 撤销最后一次提交（保留更改）
git reset --soft HEAD~1

# 修改最后一次提交
git commit --amend

# 标签管理
git tag v1.0.0  # 创建标签
git tag -a v1.0.0 -m "Version 1.0.0"  # 带注释的标签
git push origin v1.0.0  # 推送标签
git push origin --tags  # 推送所有标签

# 储藏更改
git stash
git stash pop

# 变基操作
git rebase main

# 清理未追踪的文件
git clean -f
```

---

## 🐳 Docker

### 常用命令

```bash
# 构建 Docker 镜像
docker build -t image-name .

# 运行容器
docker run -d -p 8080:8080 image-name

# 查看运行中的容器
docker ps

# 查看所有容器
docker ps -a

# 停止容器
docker stop container-id

# 删除容器
docker rm container-id

# 查看容器日志
docker logs container-id

# 进入容器
docker exec -it container-id /bin/bash

# 停止并删除所有容器
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

# 删除所有镜像
docker rmi $(docker images -q)

# 查看镜像
docker images

# 删除未使用的镜像
docker image prune
```

### Dockerfile 示例

```dockerfile
# Python Web 应用
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "app.py"]
```

---

## 🖥️ Linux 系统管理

### 进程管理

```bash
# 查看所有进程
ps aux

# 查看特定进程
ps aux | grep python3

# 查看进程树
pstree

# 杀死进程
kill pid
kill -9 pid  # 强制杀死

# 后台运行
nohup command &

# 后台运行并记录日志
nohup command > log.txt 2>&1 &
```

### 服务管理

```bash
# Systemd 服务
systemctl start service-name
systemctl stop service-name
systemctl restart service-name
systemctl status service-name
systemctl enable service-name  # 开机自启
systemctl disable service-name # 禁用开机自启

# 查看服务日志
journalctl -u service-name
```

### 文件和目录操作

```bash
# 查看文件大小
du -sh filename
du -sh directory

# 查找文件
find . -name "*.py"

# 统计文件数量
find . -name "*.md" | wc -l

# 查找并删除
find . -name "*.log" -delete

# 修改权限
chmod 755 script.sh  # rwxr-xr-x
chmod +x script.sh  # 添加执行权限

# 修改所有者
chown user:group filename
```

---

## 🌐 网络

### 端口查看

```bash
# 查看端口占用
netstat -tuln | grep 8080
ss -tuln | grep 8080
lsof -i :8080
```

### 网络测试

```bash
# Ping 测试
ping google.com

# 测试端口连接
telnet host port
nc -zv host port

# 下载速度测试
curl -o /dev/null -s -w "%{speed_download}\n" http://example.com/file
```

### 防火墙

```bash
# firewalld 防火墙
firewall-cmd --state
firewall-cmd --list-all
firewall-cmd --add-port=8080/tcp --permanent
firewall-cmd --reload
```

---

## 📊 数据处理

### 文本处理

```bash
# 查看文件内容
cat file.txt

# 查看文件前 N 行
head -n 10 file.txt

# 查看文件后 N 行
tail -n 10 file.txt

# 实时查看文件
tail -f file.txt

# 搜索文本
grep "keyword" file.txt

# 统计行数
wc -l file.txt

# 统计字数
wc -w file.txt
```

### 数据转换

```bash
# JSON 格式化
python3 -m json.tool file.json

# 转换编码
iconv -f utf-8 -t gbk input.txt > output.txt

# Base64 编码
echo "text" | base64

# Base64 解码
echo "text" | base64 -d
```

---

## 🔄 定时任务

### Cron 定时任务

```bash
# 编辑 Crontab
crontab -e

# 每小时整点执行
0 * * * * /path/to/script.sh

# 每天 2:00 执行
0 2 * * * /path/to/script.sh

# 每周一 9:00 执行
0 9 * * 1 /path/to/script.sh

# 每 15 分钟执行
*/15 * * * * /path/to/script.sh

# 查看 Cron 任务
crontab -l

# 删除所有 Cron 任务
crontab -r
```

---

## 🔍 调试技巧

### Python 调试

```python
# 使用 print 调试
print(f"Variable value: {variable}")
print(f"Variable type: {type(variable)}")

# 使用 pdb 调试器
import pdb; pdb.set_trace()

# 查看异常信息
import traceback
try:
    # code that may raise exception
except Exception as e:
    traceback.print_exc()
```

### 日志查看

```bash
# 查看日志文件
tail -f log.txt

# 搜索日志
grep "error" log.txt
grep "error" log.txt | tail -20  # 最后 20 个错误

# 统计错误数量
grep "error" log.txt | wc -l
```

---

## 📝 备注

### 快速查找
- 使用 `Ctrl + F` 在浏览器中查找
- 使用 `grep` 在文件中查找
- 使用 `which` 和 `where` 查找命令路径

### 效率提升
- 使用 Tab 自动补全
- 使用历史命令（`↑` `↓`）
- 使用别名简化长命令

---

**最后更新：** 2026-02-02 12:45（北京时间）
**会话ID：** session-20260202-0655
**状态：** 🟢 速查表完成
