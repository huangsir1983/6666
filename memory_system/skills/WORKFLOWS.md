# 🔄 WORKFLOWS - 工作流程

**最后更新：** 2026-02-02 12:55（北京时间）
**会话ID：** session-20260202-0655
**目的：** 记录常用的工作流程

---

## 🛠️ 开发工作流程

### Flask Web 应用开发

**阶段 1：需求分析和设计（30 分钟）**

1. **需求分析**
   - [ ] 明确功能需求
   - [ ] 确定用户场景
   - [ ] 定义 API 端点
   - [ ] 确定数据结构

2. **技术选型**
   - [ ] 选择框架（Flask）
   - [ ] 选择数据库（SQLite/MySQL/PostgreSQL）
   - [ ] 选择认证方案（JWT/Session）
   - [ ] 确定部署方式（Docker/裸机）

3. **架构设计**
   - [ ] 设计项目结构
   - [ ] 设计数据库模型
   - [ ] 设计 API 接口
   - [ ] 设计前端页面

**阶段 2：快速开发（2-4 小时）**

1. **后端开发**
   ```bash
   # 创建虚拟环境
   python3 -m venv venv
   source venv/bin/activate

   # 安装依赖
   pip install flask requests

   # 创建项目结构
   mkdir -p templates static/css static/js

   # 开发主应用
   vim app.py
   ```

2. **API 端点开发**
   ```python
   from flask import Flask, request, jsonify

   app = Flask(__name__)

   @app.route('/api', methods=['GET', 'POST'])
   def api():
       if request.method == 'POST':
           data = request.json
           # 处理数据
           return jsonify({'success': True, 'data': data})
       else:
           # 返回数据
           return jsonify({'success': True, 'data': 'result'})
   ```

3. **前端开发**
   ```html
   <!-- templates/index.html -->
   <form id="apiForm">
       <input type="text" name="key" placeholder="Key">
       <input type="text" name="value" placeholder="Value">
       <button type="submit">提交</button>
   </form>

   <script>
   const form = document.getElementById('apiForm');
   form.addEventListener('submit', async (e) => {
       e.preventDefault();
       const formData = new FormData(form);
       const response = await fetch('/api', {
           method: 'POST',
           body: JSON.stringify(Object.fromEntries(formData))
       });
       const result = await response.json();
       alert(JSON.stringify(result, null, 2));
   });
   </script>
   ```

**阶段 3：测试和优化（1-2 小时）**

1. **功能测试**
   - [ ] 测试所有 API 端点
   - [ ] 测试前端交互
   - [ ] 测试错误处理
   - [ ] 测试边界情况

2. **性能优化**
   - [ ] 数据库查询优化
   - [ ] 响应时间优化
   - [ ] 内存使用优化
   - [ ] 并发处理优化

3. **安全加固**
   - [ ] 输入验证
   - [ ] SQL 注入防护
   - [ ] XSS 防护
   - [ ] CORS 配置

---

## 🌐 API 开发工作流程

### REST API 设计

**阶段 1：API 设计（1 小时）**

1. **确定资源和端点**
   ```
   GET    /api/articles          # 获取文章列表
   POST   /api/articles          # 创建文章
   GET    /api/articles/:id       # 获取单篇文章
   PUT    /api/articles/:id       # 更新文章
   DELETE /api/articles/:id       # 删除文章
   ```

2. **定义请求和响应格式**
   ```json
   // 请求格式（POST /api/articles）
   {
     "title": "文章标题",
     "content": "文章内容",
     "author": "作者"
   }

   // 响应格式
   {
     "success": true,
     "data": {
       "id": "article-id",
       "title": "文章标题",
       "content": "文章内容",
       "author": "作者",
       "created_at": "2026-02-02T12:55:00Z"
     }
   }
   ```

**阶段 2：API 实现（2-3 小时）**

1. **使用 Flask 蓝图**
   ```python
   from flask import Blueprint, request, jsonify
   from flask_restx import Api, Resource, fields

   api = Blueprint('articles', __name__)

   # 定义数据模型
   article_model = api.model('Article', {
       'id': fields.String,
       'title': fields.String,
       'content': fields.String,
       'author': fields.String,
       'created_at': fields.DateTime
   })

   # 定义资源
   class ArticleResource(Resource):
       @api.doc('get articles')
       def get(self):
           # 获取文章列表
           pass

       @api.doc('create article')
       @api.expect(article_model)
       def post(self):
           # 创建文章
           data = request.json
           # 保存到数据库
           return {'success': True}
   ```

2. **使用 Flask 原生路由**
   ```python
   from flask import Flask, request, jsonify

   app = Flask(__name__)

   @app.route('/api/articles', methods=['GET', 'POST'])
   def articles():
       if request.method == 'POST':
           data = request.json
           # 保存到数据库
           return jsonify({'success': True, 'id': 'new-id'})
       else:
           # 获取文章列表
           return jsonify({'articles': []})
   ```

---

## 📦 项目发布工作流程

### GitHub Release 创建

**阶段 1：准备（10 分钟）**

1. **更新版本号**
   ```bash
   # 更新 README.md 中的版本号
   vim README.md

   # 提交更改
   git add README.md
   git commit -m "Update version to v1.0.1"
   ```

2. **更新 CHANGELOG.md**
   ```markdown
   ## [1.0.1] - 2026-02-02

   ### 新增
   - 新增功能 1
   - 新增功能 2

   ### 修复
   - 修复 Bug 1
   - 修复 Bug 2

   ### 优化
   - 优化性能 1
   - 优化性能 2
   ```

3. **更新代码**
   ```bash
   # 提交所有更改
   git add .
   git commit -m "Release v1.0.1"
   ```

**阶段 2：创建 Tag（2 分钟）**

1. **创建 Tag**
   ```bash
   # 获取最新的完整 SHA
   git log -1 --format=%H

   # 创建 Tag
   git tag v1.0.1 <full-sha>
   ```

2. **推送 Tag**
   ```bash
   git push origin v1.0.1
   ```

**阶段 3：创建 Release（5 分钟）**

1. **手动创建**（推荐）
   - 访问：https://github.com/huangsir1983/6666/releases/new
   - 选择 Tag：v1.0.1
   - 填写标题：Release v1.0.1
   - 填写描述：发布说明
   - 点击 "Publish release"

2. **自动创建**（使用 GitHub API）
   ```python
   import requests

   headers = {
       "Authorization": "token YOUR_TOKEN",
       "Accept": "application/vnd.github.v3+json"
   }

   url = "https://api.github.com/repos/huangsir1983/6666/releases"
   data = {
       "tag_name": "v1.0.1",
       "target_commitish": "main",
       "name": "Release v1.0.1",
       "body": "Release notes",
       "draft": False,
       "prerelease": False
   }

   response = requests.post(url, headers=headers, json=data)
   print(f"Release 状态码：{response.status_code}")
   ```

---

## 📝 文档编写工作流程

### README.md 编写

**阶段 1：确定内容结构（5 分钟）**

1. **基本信息**
   - 项目名称和简介
   - 项目特点
   - 技术栈
   - 快速开始指南

2. **详细文档**
   - 安装说明
   - 使用说明
   - API 文档
   - 配置说明
   - 故障排查

**阶段 2：编写内容（30 分钟）**

1. **使用 Markdown**
   ```markdown
   # 项目名称

   简短的介绍...

   ## 特性

   - 特性 1
   - 特性 2

   ## 安装

   ```bash
   git clone https://github.com/username/repo.git
   cd repo
   pip install -r requirements.txt
   ```

   ## 使用

   快速使用指南...

   ## API 文档

   ### 端点 1

   **方法：** GET
   **URL：** /api/endpoint
   **参数：**
   - param1 (required): 参数说明
   - param2 (optional): 参数说明

   **响应：**
   ```json
   {
     "success": true,
     "data": {}
   }
   ```

   ## 配置

   环境变量配置说明...

   ## 故障排查

   常见问题和解决方案...
   ```

**阶段 3：优化和美化（10 分钟）**

1. **添加徽章**
   ```markdown
   ![License](https://img.shields.io/badge/license-MIT-green)
   ![Python](https://img.shields.io/badge/python-3.7+-yellow)
   ![Stars](https://img.shields.io/github/stars/username/repo)
   ```

2. **添加截图**
   ```markdown
   ![Screenshot](https://github.com/username/repo/raw/main/screenshot.png)
   ```

3. **添加目录**
   ```markdown
   - [特性](#特性)
   - [安装](#安装)
   - [使用](#使用)
   ```

---

## 🎯 问题排查工作流程

### 调试步骤

**阶段 1：收集信息（5 分钟）**

1. **收集错误信息**
   - [ ] 错误消息
   - [ ] 错误代码
   - [ ] 发生时间
   - [ ] 操作步骤

2. **收集环境信息**
   - [ ] 操作系统版本
   - [ ] Python 版本
   - [ ] 依赖版本
   - [ ] 系统资源使用

**阶段 2：分析问题（10 分钟）**

1. **搜索类似问题**
   ```bash
   # 在 GitHub 上搜索类似问题
   https://github.com/search?q=error+message

   # 在 Stack Overflow 上搜索
   https://stackoverflow.com/search?q=error+message

   # 在项目 Issues 中搜索
   https://github.com/username/repo/issues?q=error+keyword
   ```

2. **查阅文档**
   ```bash
   # 查看官方文档
   https://docs.python.org/

   # 查看项目文档
   cat README.md
   cat FAQ.md
   ```

3. **使用调试工具**
   ```python
   # 使用 print 调试
   print(f"Variable: {variable}")
   print(f"Type: {type(variable)}")

   # 使用 logging 调试
   import logging
   logging.basicConfig(level=logging.DEBUG)
   logging.debug(f"Debug info")

   # 使用 pdb 调试器
   import pdb
   pdb.set_trace()
   ```

**阶段 3：解决问题（15-30 分钟）**

1. **尝试常见解决方案**
   - [ ] 重启服务
   - [ ] 清除缓存
   - [ ] 检查网络连接
   - [ ] 更新依赖版本

2. **回退到已知好的版本**
   ```bash
   # Git 回退
   git revert HEAD
   git revert HEAD~1

   # 检出特定版本
   git checkout v1.0.0
   ```

3. **寻求帮助**
   - [ ] 查看项目 Issues
   - [ ] 提交新的 Issue
   - [ ] 社区论坛提问
   - [ ] Stack Overflow 提问

---

## 📊 流程优化建议

### 提高效率

1. **批量处理** - 一次处理多个相似任务
2. **使用快捷键** - 掌握常用工具的快捷键
3. **自动化脚本** - 自动化重复性任务
4. **使用模板** - 使用代码和文档模板

### 减少错误

1. **类型检查** - 使用 mypy 进行类型检查
2. **代码审查** - 定期进行代码审查
3. **单元测试** - 编写和运行单元测试
4. **集成测试** - 测试整个应用流程

---

## 📝 备注

### 工作流程记录
1. **记录新流程** - 遇到新的工作流程时记录
2. **定期优化** - 定期回顾和优化工作流程
3. **分享经验** - 把优化后的工作流程分享给团队
4. **持续改进** - 持续改进工作流程

### 流程版本管理
1. **版本控制** - 对工作流程进行版本控制
2. **变更记录** - 记录流程的变更
3. **回退机制** - 如果新的流程有问题，可以回退到旧流程
4. **A/B 测试** - 对不同流程进行 A/B 测试

---

**最后更新：** 2026-02-02 12:55（北京时间）
**会话ID：** session-20260202-0655
**状态：** 🟢 工作流程文档完成
