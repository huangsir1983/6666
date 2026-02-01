# 🔧 故障排查指南

**项目：** AI 工具箱
**用途：** 解决常见问题和错误
**安全：** 不含任何敏感信息

---

## 📋 目录

1. [快速诊断](#快速诊断)
2. [启动问题](#启动问题)
3. [连接问题](#连接问题)
4. [API 调用问题](#api-调用问题)
5. [性能问题](#性能问题)
6. [部署问题](#部署问题)
7. [日志分析](#日志分析)
8. [联系支持](#联系支持)

---

## 快速诊断

### 诊断工具包

运行这个快速诊断脚本：

```bash
#!/bin/bash

echo "=== AI 工具箱诊断工具 ==="
echo ""

# 1. 检查 Python
echo "1. 检查 Python 版本..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 未安装"
else
    echo "✅ Python 已安装"
fi
echo ""

# 2. 检查依赖
echo "2. 检查 Python 依赖..."
pip3 show flask > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Flask 已安装"
else
    echo "❌ Flask 未安装"
fi

pip3 show requests > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Requests 已安装"
else
    echo "❌ Requests 未安装"
fi
echo ""

# 3. 检查端口
echo "3. 检查端口占用..."
for port in 8080 8081 8082; do
    lsof -i :$port > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "✅ 端口 $port 被占用"
    else
        echo "⚠️  端口 $port 未被占用"
    fi
done
echo ""

# 4. 检查服务
echo "4. 检查服务状态..."
for service in proxy auth http; do
    # 这里需要根据实际调整
    echo "检查 $service 服务..."
done
echo ""

# 5. 检查网络
echo "5. 检查网络连接..."
ping -c 1 open.bigmodel.cn > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ 可以连接智谱 API"
else
    echo "❌ 无法连接智谱 API"
fi
echo ""

echo "=== 诊断完成 ==="
```

保存为 `diagnose.sh`，运行：
```bash
chmod +x diagnose.sh
./diagnose.sh
```

---

## 启动问题

### 问题 1：服务无法启动

**症状：** 运行 `python3 proxy_server_v2.py` 无响应或报错

**可能原因：**

#### 1.1 端口被占用

**检查：**
```bash
lsof -i :8080
# 或
netstat -tlnp | grep 8080
```

**解决方法：**
```bash
# 方法 1：关闭占用进程
kill -9 <PID>

# 方法 2：更改端口
# 编辑 proxy_server_v2.py
app.run(host='0.0.0.0', port=8081)  # 改为 8081
```

---

#### 1.2 依赖未安装

**检查：**
```bash
pip3 list | grep -E "flask|requests"
```

**解决方法：**
```bash
# 安装依赖
pip3 install flask requests

# 或使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install flask requests
```

---

#### 1.3 Python 版本过低

**检查：**
```bash
python3 --version
# 需要 3.7+
```

**解决方法：**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.9

# macOS
brew install python3

# CentOS/RHEL
sudo yum install python39
```

---

#### 1.4 权限问题

**症状：** `Permission denied` 或 `Address already in use`

**解决方法：**
```bash
# 方法 1：使用普通端口（1024 以上）
# 不需要 sudo

# 方法 2：更改文件权限
chmod +x *.py

# 方法 3：使用 sudo（不推荐）
sudo python3 proxy_server_v2.py
```

---

#### 1.5 配置文件错误

**检查：**
- 查看 .env 文件是否存在
- 检查配置语法

**解决方法：**
```bash
# 创建 .env 文件
echo "ZHIPU_API_KEY=your-key" > .env

# 检查配置文件
cat .env
```

---

### 问题 2：服务启动后立即退出

**症状：** 服务启动后几秒内自动关闭

**可能原因：**

#### 2.1 智谱 API Key 无效

**检查：**
```bash
# 查看日志
tail -f proxy_v2.log
```

**解决方法：**
```bash
# 验证 API Key
curl -X POST https://open.bigmodel.cn/api/paas/v4/chat/completions \
  -H "Authorization: Bearer YOUR_ZHIPU_API_KEY" \
  -d '{"model":"glm-4.7","messages":[{"role":"user","content":"hi"}]}'
```

---

#### 2.2 网络连接问题

**检查：**
```bash
# 测试网络
ping open.bigmodel.cn

# 测试 DNS
nslookup open.bigmodel.cn
```

**解决方法：**
```bash
# 检查防火墙
sudo ufw status

# 临时关闭防火墙测试
sudo ufw disable

# 或添加规则
sudo ufw allow 8080/tcp
```

---

## 连接问题

### 问题 3：无法访问服务

**症状：** 浏览器访问 http://localhost:8080 失败

**可能原因：**

#### 3.1 服务未运行

**检查：**
```bash
ps aux | grep proxy_server
```

**解决方法：**
```bash
# 启动服务
python3 proxy_server_v2.py
```

---

#### 3.2 防火墙阻止

**检查：**
```bash
sudo ufw status
# 或
sudo iptables -L
```

**解决方法：**
```bash
# 允许端口
sudo ufw allow 8080/tcp
sudo ufw allow 8081/tcp
sudo ufw allow 8082/tcp

# 或临时关闭
sudo ufw disable
```

---

#### 3.3 云服务器安全组

**症状：** 本地可以访问，远程无法访问

**检查：**
- 云服务器控制台安全组设置
- 确保端口已开放

**解决方法：**
```bash
# 添加安全组规则
# 入站规则：TCP 8080-8082 允许 0.0.0.0/0
```

---

### 问题 4：HTTPS 连接失败

**症状：** 浏览器提示证书错误

**解决方法：**
```bash
# 方法 1：使用 HTTP（开发环境）
# 直接使用 http://

# 方法 2：配置 Let's Encrypt（生产环境）
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## API 调用问题

### 问题 5：API 调用返回 401

**症状：** `{"error": "Invalid API Key"}`

**可能原因：**

#### 5.1 API Key 无效

**检查：**
```bash
# 验证 API Key
curl http://localhost:8082/auth/usage \
  -H "X-API-Key: YOUR_API_KEY"
```

**解决方法：**
```bash
# 重新注册获取 API Key
curl -X POST http://localhost:8082/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"new@email.com","password":"password"}'
```

---

#### 5.2 API Key 过期

**检查：**
- 查看账户状态

**解决方法：**
```bash
# 重新注册
curl -X POST http://localhost:8082/auth/register ...
```

---

### 问题 6：API 调用返回 429

**症状：** `{"error": "Rate limit exceeded"}`

**可能原因：**

#### 6.1 超出免费额度

**检查：**
```bash
curl http://localhost:8082/auth/usage \
  -H "X-API-Key: YOUR_API_KEY"
```

**解决方法：**
```bash
# 等待次日重置
# 或升级套餐
curl -X POST http://localhost:8082/auth/upgrade \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","password":"pass","plan":"basic"}'
```

---

#### 6.2 智谱 API 限流

**解决方法：**
```bash
# 添加请求间隔
import time
time.sleep(1)  # 每次请求间隔 1 秒
```

---

### 问题 7：API 调用返回 500

**症状：** 服务器内部错误

**可能原因：**

#### 7.1 智谱 API 错误

**检查：**
```bash
# 查看日志
tail -f proxy_v2.log
```

**解决方法：**
```bash
# 检查智谱 API 状态
# https://status.open.bigmodel.cn/
```

---

#### 7.2 服务内部错误

**检查：**
```bash
# 查看完整日志
tail -n 100 proxy_v2.log
```

**解决方法：**
```bash
# 重启服务
pkill -f proxy_server
python3 proxy_server_v2.py
```

---

### 问题 8：响应超时

**症状：** 请求长时间无响应

**可能原因：**

#### 8.1 网络慢

**解决方法：**
```python
# 增加超时时间
response = requests.post(
    API_URL,
    headers=headers,
    json=data,
    timeout=60  # 60 秒超时
)
```

---

#### 8.2 智谱 API 慢

**解决方法：**
```python
# 减少 max_tokens
data = {
    "max_tokens": 100  # 减少输出长度
}

# 或使用更简单的请求
```

---

## 性能问题

### 问题 9：响应慢

**可能原因：**

#### 9.1 智谱 API 慢

**解决方法：**
```python
# 使用更快的模型
data = {"model": "claude-haiku-4-5-20251001"}  # Haiku 更快
```

---

#### 9.2 网络延迟

**解决方法：**
```bash
# 检查网络延迟
ping open.bigmodel.cn

# 使用 CDN 或代理
```

---

#### 9.3 服务器负载高

**检查：**
```bash
# 查看系统资源
top
htop

# 查看内存
free -h
```

**解决方法：**
```bash
# 增加服务器资源
# 或优化代码
```

---

### 问题 10：内存占用高

**检查：**
```bash
# 查看内存使用
ps aux | grep python

# 查看详细内存
top -p <PID>
```

**解决方法：**
```bash
# 减少工作进程
gunicorn -w 2 -b 0.0.0.0:8080 proxy_server_v2:app

# 或限制内存
```

---

## 部署问题

### 问题 11：Docker 部署失败

**症状：** Docker 容器无法启动

**可能原因：**

#### 11.1 Docker 未安装

**检查：**
```bash
docker --version
```

**解决方法：**
```bash
# Ubuntu/Debian
sudo apt install docker.io

# CentOS/RHEL
sudo yum install docker

# macOS
# 下载 Docker Desktop
```

---

#### 11.2 Dockerfile 错误

**检查：**
```bash
# 构建 Docker 镜像
docker build -t ai-toolkit .

# 查看构建日志
```

**解决方法：**
```dockerfile
# 确保 Dockerfile 正确
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "proxy_server_v2:app"]
```

---

### 问题 12：Systemd 服务失败

**症状：** systemctl start 失败

**检查：**
```bash
# 查看服务状态
sudo systemctl status ai-api

# 查看日志
sudo journalctl -u ai-api -n 50
```

**解决方法：**
```bash
# 检查配置文件
cat /etc/systemd/system/ai-api.service

# 重新加载配置
sudo systemctl daemon-reload

# 重启服务
sudo systemctl restart ai-api
```

---

## 日志分析

### 查看日志

```bash
# 实时查看
tail -f proxy_v2.log

# 查看最后 100 行
tail -n 100 proxy_v2.log

# 搜索错误
grep -i "error" proxy_v2.log

# 搜索特定时间
grep "2026-02-02 10:" proxy_v2.log
```

### 常见日志信息

#### 正常启动
```
[2026-02-02 10:00:00] Claude Code ↔ 智谱 API 代理服务器 v2 启动中...
[2026-02-02 10:00:00] 监听端口: 8080
[2026-02-02 10:00:00] Running on http://0.0.0.0:8080
```

#### 收到请求
```
[2026-02-02 10:00:01] 收到 API 请求
[2026-02-02 10:00:01] 原始请求模型: claude-sonnet-4-5-20250929
[2026-02-02 10:00:01] 映射后模型: glm-4.7
```

#### 请求成功
```
[2026-02-02 10:00:05] 请求成功完成
127.0.0.1 - - [02/Feb/2026 10:00:05] "POST /v1/messages HTTP/1.1" 200 -
```

#### 错误示例
```
[2026-02-02 10:00:00] 智谱 API 错误: 1302 并发数过高
[2026-02-02 10:00:00] 无效的 API Key
[2026-02-02 10:00:00] 请求超时
```

---

## 联系支持

### 自助解决

1. **查看 FAQ** - FAQ.md
2. **查看日志** - 搜索错误信息
3. **运行诊断** - diagnose.sh

### 获取帮助

**提交 Issue：**
- GitHub: https://github.com/your-username/ai-toolkit/issues
- 包含：错误信息、日志、复现步骤

**联系客服：**
- Email: contact@example.com
- 响应时间：24-48 小时

**付费支持：**
- 专业版：专属客服
- 企业版：7x24 支持

---

## 常用命令速查

### 服务管理
```bash
# 启动服务
python3 proxy_server_v2.py

# 查看进程
ps aux | grep proxy

# 杀死进程
pkill -f proxy_server

# 重启服务
pkill -f proxy_server && python3 proxy_server_v2.py
```

### 日志查看
```bash
# 实时日志
tail -f proxy_v2.log

# 搜索错误
grep -i error *.log

# 查看最近 50 行
tail -n 50 proxy_v2.log
```

### 网络检查
```bash
# 检查端口
lsof -i :8080
netstat -tlnp | grep 8080

# 测试连接
ping open.bigmodel.cn
curl http://localhost:8080/health
```

### 系统监控
```bash
# CPU 使用
top

# 内存使用
free -h

# 磁盘使用
df -h
```

---

**最后更新：** 2026-02-02
**版本：** 1.0.0
