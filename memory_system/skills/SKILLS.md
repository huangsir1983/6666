# 🛠️ SKILLS - 技能清单

**最后更新：** 2026-02-02 12:40（北京时间）
**会话ID：** session-20260202-0655
**目的：** 固化日常经验为可复用的技能

---

## 📋 技能总览

### 编程语言
- **Python:** 熟练（2,000+ 行代码）
- **JavaScript:** 熟练（500+ 行代码）
- **HTML/CSS:** 熟练（1,000+ 行代码）
- **Bash/Shell:** 熟练（100+ 脚本）

### Web 开发框架
- **Flask:** 熟练（API 开发）
- **REST API:** 熟练（设计和实现）
- **HTTP 协议:** 熟练（请求和响应）

### 版本控制
- **Git:** 熟练（日常使用）
- **GitHub:** 熟练（API 自动化）

### 容器化
- **Docker:** 熟练（基础使用）
- **虚拟环境:** 熟练（venv, conda）

### 系统管理
- **Linux:** 熟练（命令行操作）
- **Systemd:** 熟练（服务管理）
- **Cron:** 熟练（定时任务）

### 自动化
- **Requests:** 熟练（HTTP 自动化）
- **Selenium:** 入门（基础使用）
- **脚本开发:** 熟练（Python 脚本）

---

## 📚 技能详情

### 编程技能

#### Python
**熟练度：** 熟练

**掌握的功能：**
- ✅ Flask Web 框架
- ✅ REST API 设计和实现
- ✅ 异步编程（async/await）
- ✅ 类和面向对象编程
- ✅ 模块化开发
- ✅ 错误处理和调试
- ✅ 文件 I/O 和序列化
- ✅ HTTP 请求（requests 库）
- ✅ JSON 处理
- ✅ 正则表达式
- ✅ 日志记录（logging 模块）

**典型任务：**
- 开发 Web API 服务
- 数据处理和分析
- 自动化脚本开发
- 后端服务开发

---

#### JavaScript
**熟练度：** 熟练

**掌握的功能：**
- ✅ ES6+ 语法
- ✅ Fetch API
- ✅ DOM 操作
- ✅ 事件处理
- ✅ 异步编程
- ✅ JSON 处理
- ✅ 模块化开发

**典型任务：**
- 前端交互开发
- AJAX 请求
- 动态页面更新

---

#### HTML/CSS
**熟练度：** 熟练

**掌握的功能：**
- ✅ HTML5 语义化标签
- ✅ 响应式设计
- ✅ CSS Flexbox 和 Grid
- ✅ 动画和过渡
- ✅ 媒体查询
- ✅ 表单和输入控件
- ✅ 用户体验设计

**典型任务：**
- Web 界面开发
- 样式设计
- 响应式布局

---

### Web 开发技能

#### Flask
**熟练度：** 熟练

**掌握的功能：**
- ✅ 路由定义（@app.route）
- ✅ 请求处理（request.form, request.json, request.args）
- ✅ 响应格式（render_template, jsonify）
- ✅ 蓝图
- ✅ 中间件
- ✅ 会话管理
- ✅ 错误处理
- ✅ 模板引擎

**典型任务：**
- 开发 REST API 服务
- 文件服务器
- 用户认证系统
- 完整的 Web 应用

---

#### REST API
**熟练度：** 熟练

**掌握的功能：**
- ✅ RESTful 设计原则
- ✅ HTTP 方法（GET, POST, PUT, DELETE）
- ✅ 状态码（200, 201, 400, 404, 500）
- ✅ JSON 请求和响应
- ✅ 认证和授权
- ✅ 分页和过滤
- ✅ API 版本控制

**典型任务：**
- API 设计和实现
- 接口文档编写
- API 测试和调试

---

### 版本控制技能

#### Git
**熟练度：** 熟练

**掌握的命令：**
- ✅ `git init` - 初始化仓库
- ✅ `git clone` - 克隆仓库
- ✅ `git add` - 添加文件
- ✅ `git commit` - 提交更改
- ✅ `git push` - 推送到远程
- ✅ `git pull` - 拉取更新
- ✅ `git branch` - 分支管理
- ✅ `git checkout` - 切换分支
- ✅ `git merge` - 合并分支
- ✅ `git log` - 查看历史
- ✅ `git diff` - 查看差异
- ✅ `git tag` - 标签管理

**典型任务：**
- 版本控制
- 代码管理
- 协作开发
- 发布管理

---

#### GitHub API
**熟练度：** 熟练

**掌握的功能：**
- ✅ 用户认证（Token）
- ✅ 仓库操作（创建、删除、更新）
- ✅ 文件操作（上传、下载、删除）
- ✅ Issue 管理
- ✅ Release 创建
- ✅ API 请求格式和认证

**典型任务：**
- 自动化 GitHub 操作
- Release 创建
- 文件管理
- Issue 自动化

---

### 容器化技能

#### Docker
**熟练度：** 熟练

**掌握的命令：**
- ✅ `docker build` - 构建镜像
- ✅ `docker run` - 运行容器
- ✅ `docker ps` - 查看运行中的容器
- ✅ `docker stop` - 停止容器
- ✅ `docker logs` - 查看容器日志
- ✅ `docker exec` - 进入容器
- ✅ Dockerfile 编写

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["python", "app.py"]
```

**典型任务：**
- 容器化应用
- 环境部署
- 服务编排

---

### 系统管理技能

#### Linux
**熟练度：** 熟练

**掌握的命令：**
- ✅ 文件操作（ls, cd, cp, mv, rm）
- ✅ 权限管理（chmod, chown）
- ✅ 进程管理（ps, kill, nohup）
- ✅ 服务管理（systemctl）
- ✅ 网络配置（ifconfig, ping）
- ✅ 包管理（apt, yum, pip）
- ✅ 日志查看（tail, grep）

**典型任务：**
- 系统维护
- 服务部署
- 问题排查

---

#### Systemd
**熟练度：** 熟练

**掌握的命令：**
- ✅ `systemctl start` - 启动服务
- ✅ `systemctl stop` - 停止服务
- ✅ `systemctl restart` - 重启服务
- ✅ `systemctl status` - 查看状态
- ✅ `systemctl enable` - 开机自启
- ✅ `systemctl disable` - 禁用开机自启

**Service 文件:**
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

**典型任务：**
- 服务开机自启
- 服务监控
- 自动重启

---

### 自动化技能

#### Requests
**熟练度：** 熟练

**掌握的功能：**
- ✅ GET 请求
- ✅ POST 请求（JSON 和表单）
- ✅ PUT 请求
- ✅ DELETE 请求
- ✅ 请求头处理
- ✅ 会话管理（Session）
- ✅ Cookie 处理
- ✅ 超时设置
- ✅ 错误处理和重试
- ✅ 文件上传

**典型任务：**
- HTTP 自动化
- API 调用
- 网络爬虫

---

#### Selenium
**熟练度：** 入门

**掌握的功能：**
- ✅ 浏览器启动和控制
- ✅ 元素查找（find_element）
- ✅ 元素交互（click, send_keys）
- ✅ 等待元素加载
- ✅ 滚动和截图
- ✅ Cookie 处理

**典型任务：**
- 网页自动化
- 数据抓取
- 自动化测试

---

### 脚本开发

**熟练度：** 熟练

**掌握的功能：**
- ✅ Bash 脚本编写
- ✅ Python 脚本编写
- ✅ 文件处理
- ✅ 文本处理
- ✅ 网络请求
- ✅ 系统调用
- ✅ 错误处理

**典型任务：**
- 自动化脚本
- 数据处理脚本
- 系统管理脚本

---

## 🎯 技能提升计划

### 短期目标（1-2 周）

- [ ] 提高 JavaScript 技能（ES6+ 新特性）
- [ ] 学习 Docker 高级特性（多阶段构建、编排）
- [ ] 学习 Kubernetes（容器编排）
- [ ] 提高 Selenium 技能（高级功能）

### 中期目标（1-2 月）

- [ ] 学习 Node.js（前端开发）
- [ ] 学习 React/Vue（前端框架）
- [ ] 学习 Go/Rust（后端性能）
- [ ] 学习 CI/CD（自动化部署）

### 长期目标（3-6 月）

- [ ] 学习云原生技术（Cloud Native）
- [ ] 学习微服务架构
- [ ] 学习分布式系统
- [ ] 学习大数据处理

---

## 📊 技能评估

### 编程技能
- **Python:** ⭐⭐⭐⭐⭐ (5/5)
- **JavaScript:** ⭐⭐⭐⭐ (4/5)
- **HTML/CSS:** ⭐⭐⭐⭐ (4/5)
- **Bash/Shell:** ⭐⭐⭐⭐ (4/5)

### 开发技能
- **Web 开发:** ⭐⭐⭐⭐⭐ (5/5)
- **API 开发:** ⭐⭐⭐⭐⭐ (5/5)
- **自动化:** ⭐⭐⭐⭐ (4/5)
- **系统管理:** ⭐⭐⭐⭐ (4/5)

### 工具技能
- **Git:** ⭐⭐⭐⭐⭐ (5/5)
- **Docker:** ⭐⭐⭐ (3/5)
- **Selenium:** ⭐⭐ (2/5)
- **GitHub API:** ⭐⭐⭐⭐⭐ (5/5)

---

## 💡 学习资源

### 在线文档
- Python 官方文档: https://docs.python.org/
- Flask 文档: https://flask.palletsprojects.com/
- Git 官方文档: https://git-scm.com/doc

### 实践平台
- LeetCode: https://leetcode.com/
- GitHub: https://github.com/
- Stack Overflow: https://stackoverflow.com/

---

**最后更新：** 2026-02-02 12:40（北京时间）
**会话ID：** session-20260202-0655
**状态：** 🟢 技能清单完成
