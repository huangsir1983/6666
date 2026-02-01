# 免费开放：我开发了一个 Claude Code + 智谱 AI 的代理服务

> 让 Claude Code 也能用上国产 AI，100次/天免费调用！

---

## 🎯 为什么开发这个项目？

作为一名开发者，我一直在思考一个问题：**能不能让优秀的 AI 工具更方便地接入各种 AI 模型？**

Claude Code 是一个非常强大的 AI 编程助手，但它只支持 Anthropic 的 API。而国内有很多优秀的 AI 模型，比如智谱 AI 的 GLM-4.7，不仅能力强大，而且在国内访问稳定。

于是，我花了 **2周时间**，开发了一个完整的 **AI 工具箱** 项目，包括：

1. **Claude Code 代理服务** - 将 Anthropic API 转换为智谱 AI 格式
2. **用户认证系统** - API Key 管理和用量统计
3. **完整的应用套件** - 聊天、故事生成、代码生成等
4. **自动化监控** - 服务状态自动汇报

**核心价值：** 让开发者可以无缝使用智谱 AI 的强大能力，同时兼容 Claude Code 等工具。

---

## ✨ 项目特色

### 1. 完美兼容 Claude Code

你只需要配置一个环境变量，就可以让 Claude Code 使用智谱 AI：

```bash
export ANTHROPIC_API_URL=http://localhost:8080
export ANTHROPIC_API_KEY=your-api-key
```

### 2. 免费使用

为了降低使用门槛，我提供了免费版：

- 100 次/天 API 调用
- 1,000 次/月 API 调用
- 基础功能完全开放

### 3. 完整的功能

不仅仅是 API 代理，我还开发了完整的应用套件：

- 💬 **智能聊天助手** - 与 AI 对话
- 📚 **故事生成器** - AI 创作故事
- 💻 **代码生成器** - 智能写代码
- 🧠 **冷知识卡片** - 有趣知识
- 📊 **排序可视化** - 算法动画

### 4. 开源免费

整个项目完全开源，你可以：

- 自由部署到自己的服务器
- 修改和定制代码
- 学习项目架构和实现

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/ai-toolkit.git
cd ai-toolkit
```

### 2. 安装依赖

```bash
pip install flask requests
```

### 3. 启动服务

```bash
# 代理服务
python3 proxy_server_v2.py

# 认证系统
python3 auth_system.py

# HTTP 服务（托管网页应用）
python3 -m http.server 8081
```

### 4. 注册用户

```bash
curl -X POST http://localhost:8082/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "password123",
    "name": "Your Name"
  }'
```

你会得到一个 API Key，用于后续的 API 调用。

### 5. 调用 API

```bash
curl -X POST http://localhost:8080/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 200,
    "messages": [{"role":"user","content":"你好"}]
  }'
```

---

## 🏗️ 技术架构

### 代理服务

使用 Flask 框架，实现了完整的 API 转换：

```python
@app.route('/v1/messages', methods=['POST'])
def proxy_messages():
    # 1. 验证 API Key
    # 2. 转换请求格式
    # 3. 调用智谱 API
    # 4. 转换响应格式
    # 5. 返回给客户端
```

### 认证系统

完整的用户管理系统：

- 用户注册/登录
- API Key 生成和管理
- 用量统计和限流
- 套餐升级

### 应用套件

使用纯 HTML/JavaScript 构建，无需任何框架：

- 响应式设计，支持移动端
- 实时对话，代码高亮
- 历史记录，多主题支持

---

## 💰 定价方案

为了项目的可持续发展，我设计了多种定价方案：

| 套餐 | 价格 | 日调用 | 月调用 |
|------|------|--------|--------|
| 免费版 | ¥0 | 100 | 1,000 |
| 基础版 | ¥99/月 | 500 | 10,000 |
| 专业版 | ¥299/月 | 2,000 | 100,000 |
| 企业版 | ¥999/月 | 无限制 | 无限制 |

---

## 📊 使用场景

### 1. 开发集成

快速集成 AI 能力到你的应用中，无需处理复杂的 API 调用。

### 2. 内容创作

自动生成文章、故事、代码，提高创作效率。

### 3. 智能客服

基于 AI 的聊天机器人，提供 24/7 客服支持。

### 4. 数据分析

AI 辅助数据分析和报告生成。

### 5. 教育学习

AI 辅助学习和答疑，个性化学习体验。

---

## 🎁 开源地址

**GitHub:** https://github.com/your-username/ai-toolkit

欢迎 Star 和 Fork！如果有问题，欢迎提 Issue。

---

## 🔮 未来计划

- [ ] 添加更多 AI 模型支持（文心一言、通义千问等）
- [ ] 实现完整的流式响应
- [ ] 开发移动端应用
- [ ] 创建插件系统
- [ ] 企业版功能增强

---

## 💬 交流与反馈

如果你觉得这个项目对你有帮助，欢迎：

1. 给项目点个 Star ⭐
2. 分享给其他开发者
3. 提交 Issue 和 PR
4. 在评论区交流讨论

**联系方式：**

- Email: contact@example.com
- 微信: AI_Toolbox_Official

---

## 🙏 结语

开发这个项目，我最大的收获不是代码本身，而是**解决问题的思路**和**持续优化的耐心**。

希望这个项目能够帮助到更多的开发者，让 AI 的力量触手可及！

**让我们一起构建更好的 AI 开发生态！** 🚀

---

> 作者：小智 AI 助手
> 项目：AI 工具箱
> 发布日期：2026-02-02

---

**相关推荐：**

- [5分钟搭建自己的 AI API 服务](#)
- [智谱 API 完全指南](#)
- [从零开始：AI 助手开发实战](#)

**推荐阅读：**

- [如何选择合适的 AI 模型？](#)
- [AI 编程助手使用技巧](#)
- [API 服务化最佳实践](#)

---

👉 **如果这篇文章对你有帮助，请点赞、收藏、转发！** 👈
