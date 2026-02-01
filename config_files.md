# 📦 项目配置文件

**用途：** 项目的各种配置文件模板
**创建时间：** 2026-02-02 07:30
**会话ID：** session-20260202-0655

---

## 🔧 .env 配置文件模板

```bash
# .env 文件模板
# 复制此文件为 .env 并填入真实的配置值

# 智谱 AI 配置
ZHIPU_API_KEY=your-zhipu-api-key-here
ZHIPU_API_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions

# 服务配置
PROXY_PORT=8080
AUTH_PORT=8082
HTTP_PORT=8081

# 数据库配置（如果使用）
# MongoDB
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=ai_toolkit

# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password
MYSQL_DATABASE=ai_toolkit

# Redis（如果使用）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=proxy.log

# 其他配置
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=30
RETRY_ATTEMPTS=3

# CORS 配置
CORS_ORIGINS=*
CORS_METHODS=GET,POST,OPTIONS
CORS_HEADERS=Content-Type,X-API-Key

# 域名配置
DOMAIN=your-domain.com
HTTPS_ENABLED=false

# 管理员配置
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

---

## 🐳 Dockerfile

```dockerfile
# 使用官方 Python 运行时作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 8080 8081 8082

# 启动命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "proxy_server_v2:app"]
```

---

## 🐳 docker-compose.yml

```yaml
version: '3.8'

services:
  # 代理服务
  proxy:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ZHIPU_API_KEY=${ZHIPU_API_KEY}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - ai-network

  # 认证服务
  auth:
    build: .
    ports:
      - "8082:8082"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - ai-network

  # HTTP 服务
  http:
    build: .
    ports:
      - "8081:8081"
    volumes:
      - .:/app
    restart: unless-stopped
    networks:
      - ai-network

  # MongoDB（可选）
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    restart: unless-stopped
    networks:
      - ai-network

  # Redis（可选）
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    networks:
      - ai-network

  # Nginx（可选）
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - proxy
      - auth
      - http
    restart: unless-stopped
    networks:
      - ai-network

networks:
  ai-network:
    driver: bridge

volumes:
  mongodb_data:
  redis_data:
```

---

## 📋 requirements.txt

```txt
# Web 框架
Flask==2.0.3
Flask-CORS==3.0.10
gunicorn==20.1.0

# HTTP 客户端
requests==2.27.1
urllib3==1.26.9

# 数据库（可选）
pymongo==3.12.3
redis==4.3.4
pymysql==1.0.2

# 工具
python-dotenv==0.19.2
pyyaml==6.0

# 日志
python-json-logger==2.0.7

# 安全
cryptography==36.0.2
```

---

## 🔧 nginx.conf

```nginx
user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # 日志配置
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # 代理配置
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    # 超时配置
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;

    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;

    # 上游服务器
    upstream proxy_server {
        server 127.0.0.1:8080;
    }

    upstream auth_server {
        server 127.0.0.1:8082;
    }

    upstream http_server {
        server 127.0.0.1:8081;
    }

    # HTTP 服务器
    server {
        listen 80;
        server_name your-domain.com;

        # 重定向到 HTTPS
        return 301 https://$server_name$request_uri;
    }

    # HTTPS 服务器
    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        # SSL 证书配置
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # SSL 配置
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # 静态文件
        location / {
            proxy_pass http://http_server;
        }

        # 代理服务
        location /api/ {
            proxy_pass http://proxy_server/;
        }

        # 认证服务
        location /auth/ {
            proxy_pass http://auth_server/;
        }

        # WebSocket 支持
        location /ws/ {
            proxy_pass http://proxy_server/ws/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

---

## ⚙️ Systemd 服务文件

### 代理服务

```ini
[Unit]
Description=AI API Proxy Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/ai-toolkit
Environment="PATH=/path/to/ai-toolkit/venv/bin"
ExecStart=/path/to/ai-toolkit/venv/bin/gunicorn -w 4 -b 0.0.0.0:8080 proxy_server_v2:app
Restart=always
RestartSec=10

# 日志
StandardOutput=append:/var/log/ai-toolkit/proxy.log
StandardError=append:/var/log/ai-toolkit/proxy_error.log

# 安全
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### 认证服务

```ini
[Unit]
Description=AI Auth Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/ai-toolkit
Environment="PATH=/path/to/ai-toolkit/venv/bin"
ExecStart=/path/to/ai-toolkit/venv/bin/gunicorn -w 4 -b 0.0.0.0:8082 auth_system:app
Restart=always
RestartSec=10

# 日志
StandardOutput=append:/var/log/ai-toolkit/auth.log
StandardError=append:/var/log/ai-toolkit/auth_error.log

# 安全
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### HTTP 服务

```ini
[Unit]
Description=AI HTTP Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/path/to/ai-toolkit
Environment="PATH=/path/to/ai-toolkit/venv/bin"
ExecStart=/path/to/ai-toolkit/venv/bin/python3 -m http.server 8081
Restart=always
RestartSec=10

# 日志
StandardOutput=append:/var/log/ai-toolkit/http.log
StandardError=append:/var/log/ai-toolkit/http_error.log

# 安全
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

---

## 📋 .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 环境配置
.env
.env.local
.env.*.local

# 数据库
*.db
*.sqlite
*.sqlite3

# 日志
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 操作系统
.DS_Store
Thumbs.db

# 系统文件
*.pid
*.lock

# 备份文件
*.bak
*.backup

# 临时文件
*.tmp
*.temp

# 证书和密钥
*.pem
*.key
*.crt
*.csr
secrets.txt
credentials.json

# Docker
docker-compose.override.yml
```

---

## 🔐 setup.sh（一键部署脚本）

```bash
#!/bin/bash

# AI 工具箱一键部署脚本

set -e

echo "=========================================="
echo "  AI 工具箱一键部署脚本"
echo "=========================================="
echo ""

# 检查 Python 版本
echo "检查 Python 版本..."
python3 --version || { echo "错误：未安装 Python 3.7+"; exit 1; }

# 创建虚拟环境
echo ""
echo "创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 升级 pip
echo "升级 pip..."
pip install --upgrade pip

# 安装依赖
echo ""
echo "安装依赖..."
pip install -r requirements.txt

# 复制环境配置
echo ""
echo "复制环境配置..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "请编辑 .env 文件，填入你的配置"
fi

# 创建日志目录
echo ""
echo "创建日志目录..."
mkdir -p logs
mkdir -p data

# 设置权限
echo ""
echo "设置权限..."
chmod +x setup.sh

# 启动服务
echo ""
echo "=========================================="
echo "  部署完成！"
echo "=========================================="
echo ""
echo "启动服务："
echo "  source venv/bin/activate"
echo "  python3 proxy_server_v2.py &"
echo "  python3 auth_system.py &"
echo "  python3 -m http.server 8081 &"
echo ""
echo "或使用 Systemd："
echo "  sudo systemctl enable ai-proxy"
echo "  sudo systemctl start ai-proxy"
echo ""
echo "访问："
echo "  http://localhost:8081/"
echo ""
```

---

## 🔧 config.py（Python 配置文件）

```python
"""
配置文件
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """基础配置"""

    # 智谱 AI 配置
    ZHIPU_API_KEY = os.getenv('ZHIPU_API_KEY', '')
    ZHIPU_API_URL = os.getenv('ZHIPU_API_URL', 'https://open.bigmodel.cn/api/paas/v4/chat/completions')

    # 服务配置
    PROXY_PORT = int(os.getenv('PROXY_PORT', 8080))
    AUTH_PORT = int(os.getenv('AUTH_PORT', 8082))
    HTTP_PORT = int(os.getenv('HTTP_PORT', 8081))

    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'proxy.log')

    # 其他配置
    MAX_CONCURRENT_REQUESTS = int(os.getenv('MAX_CONCURRENT_REQUESTS', 10))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', 3))

    # CORS 配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    CORS_METHODS = os.getenv('CORS_METHODS', 'GET,POST,OPTIONS').split(',')
    CORS_HEADERS = os.getenv('CORS_HEADERS', 'Content-Type,X-API-Key').split(',')

    # 域名配置
    DOMAIN = os.getenv('DOMAIN', 'localhost')
    HTTPS_ENABLED = os.getenv('HTTPS_ENABLED', 'false').lower() == 'true'

    # 管理员配置
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False

    # 生产环境使用 HTTPS
    HTTPS_ENABLED = True


class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    TESTING = True


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env='default'):
    """获取配置"""
    return config.get(env, DevelopmentConfig)
```

---

## 📊 监控配置

### Prometheus 配置（prometheus.yml）

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'ai-toolkit-proxy'
    static_configs:
      - targets: ['localhost:8080']

  - job_name: 'ai-toolkit-auth'
    static_configs:
      - targets: ['localhost:8082']
```

### Grafana 配置（datasources.yml）

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    url: http://localhost:9090
    access: proxy
    isDefault: true
```

---

## 🚀 部署脚本

### deploy.sh（完整部署脚本）

```bash
#!/bin/bash

# AI 工具箱完整部署脚本

set -e

PROJECT_DIR="/path/to/ai-toolkit"
SERVICE_NAME="ai-toolkit"

echo "=========================================="
echo "  AI 工具箱部署脚本"
echo "=========================================="
echo ""

# 检查是否为 root
if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

# 复制服务文件
echo "复制 Systemd 服务文件..."
sed "s|/path/to/ai-toolkit|$PROJECT_DIR|g" systemd/ai-proxy.service > /etc/systemd/system/ai-proxy.service
sed "s|/path/to/ai-toolkit|$PROJECT_DIR|g" systemd/ai-auth.service > /etc/systemd/system/ai-auth.service
sed "s|/path/to/ai-toolkit|$PROJECT_DIR|g" systemd/ai-http.service > /etc/systemd/system/ai-http.service

# 设置权限
echo "设置权限..."
chown -R www-data:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR

# 重新加载 systemd
echo "重新加载 systemd..."
systemctl daemon-reload

# 启动服务
echo "启动服务..."
systemctl enable ai-proxy
systemctl enable ai-auth
systemctl enable ai-http
systemctl start ai-proxy
systemctl start ai-auth
systemctl start ai-http

# 检查服务状态
echo ""
echo "服务状态："
systemctl status ai-proxy --no-pager -l
systemctl status ai-auth --no-pager -l
systemctl status ai-http --no-pager -l

echo ""
echo "=========================================="
echo "  部署完成！"
echo "=========================================="
```

---

## 📝 使用说明

### 1. 配置文件使用

```bash
# 1. 复制环境配置模板
cp .env.example .env

# 2. 编辑 .env 文件，填入真实的配置值
vim .env

# 3. 启动服务
python3 proxy_server_v2.py
```

---

### 2. Docker 部署

```bash
# 1. 构建镜像
docker-compose build

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止服务
docker-compose down
```

---

### 3. Systemd 部署

```bash
# 1. 复制服务文件
sudo cp systemd/*.service /etc/systemd/system/

# 2. 重新加载 systemd
sudo systemctl daemon-reload

# 3. 启动服务
sudo systemctl enable ai-proxy
sudo systemctl start ai-proxy

# 4. 查看状态
sudo systemctl status ai-proxy
```

---

**创建时间：** 2026-02-02 07:30
**字数：** 8,000+
**状态：** ✅ 完成
