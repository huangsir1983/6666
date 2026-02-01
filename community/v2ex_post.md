# V2EX 发帖内容

## 标题
[开源] Claude Code + 智谱 AI 代理服务，免费 API 调用

## 正文

大家好！

花了 2 周时间开发了一个 **AI 工具箱** 项目，今天开源出来给大家使用。

## 📦 项目简介

这是一个完整的 AI API 服务解决方案，核心功能包括：

### 1. Claude Code 代理服务
- 将 Anthropic API 转换为智谱 AI 格式
- 让 Claude Code 也能用上国产 AI
- 支持 Claude 所有模型

### 2. 用户认证系统
- 用户注册/登录
- API Key 管理
- 用量统计和限流

### 3. 完整的应用套件
- 💬 智能聊天助手
- 📚 故事生成器
- 💻 代码生成器
- 🧠 冷知识卡片

## 🎯 为什么开发这个？

作为开发者，我一直觉得：
1. Claude Code 很好用，但只支持 Anthropic API
2. 国产 AI 模型越来越强，但接入不方便
3. 现成的 API 服务太贵，个人用不起

所以决定自己做一个，降低大家的 AI 使用门槛。

## 🚀 快速开始

```bash
# 克隆项目
git clone https://github.com/your-username/ai-toolkit.git
cd ai-toolkit

# 安装依赖
pip install flask requests

# 启动服务
python3 proxy_server_v2.py    # 代理服务
python3 auth_system.py         # 认证系统
python3 -m http.server 8081    # HTTP 服务
```

## 💰 免费额度

- 免费版：100 次/天
- 基础版：500 次/天（¥99/月）
- 专业版：2,000 次/天（¥299/月）
- 企业版：无限制（¥999/月）

## 🌐 在线体验

如果你不想自己部署，可以体验我的在线版本：

- 🏠 主页：http://your-server:8081/
- 💬 聊天：http://your-server:8081/glm_chat.html
- 📚 故事：http://your-server:8081/ai_story.html

## 📊 项目地址

**GitHub:** https://github.com/your-username/ai-toolkit

欢迎 Star 和 Fork！如果有问题，欢迎提 Issue。

## 💬 求反馈

目前项目还比较基础，欢迎大家：

1. 试用并反馈问题
2. 提出功能建议
3. 贡献代码
4. 分享给其他开发者

## 🔮 未来计划

- [ ] 添加更多 AI 模型支持（文心一言、通义千问等）
- [ ] 实现流式响应
- [ ] 开发管理后台
- [ ] 移动端应用

---

如果这个项目对你有帮助，请给个 Star ⭐

**联系方式：**
- Email: contact@example.com
- 微信: AI_Toolbox_Official

---

谢谢大家！🙏

---

**标签：** AI, API, Python, 开源, Claude, 智谱AI, Claude Code
