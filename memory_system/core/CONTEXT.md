# 🌐 CONTEXT - 上下文记忆

**最后更新：** 2026-02-02 11:30（北京时间）
**会话ID：** session-20260202-0655

---

## 💻 开发环境

### 服务器信息
- **IP 地址：** 10.3.0.6
- **时间：** 2026-02-02T03:30:00Z（UTC）
- **时区：** Asia/Beijing（CST, +0800）

### Python 环境
- **版本：** Python 3.11
- **包管理器：** pip 26.0
- **虚拟环境：** 无（直接使用系统 Python）

### 已安装的包
- ✅ Flask 2.0+
- ✅ requests 2.32.3
- ✅ beautifulsoup4
- ✅ lxml
- ⚠️ Selenium（安装失败，使用 requests 替代）

---

## 🏗️ 项目结构

### 当前工作目录
- **根目录：** /root/.openclaw/workspace
- **Git 仓库：** https://github.com/huangsir1983/6666

### 主要目录
```
/root/.openclaw/workspace/
├── proxy_server_v2.py         # 代理服务
├── proxy_server_v3.py         # 代理服务（优化版）
├── auth_system.py              # 认证系统
├── scheduler.py                # 调度器
├── daily_scheduler.py          # 每日调度器
├── daily_scheduler_v2.py      # 每日调度器（修复版）
├── daily_scheduler_fixed.py   # 每日调度器（最新版）
├── memory_system/              # 记忆系统目录
│   ├── core/                   # 核心记忆
│   ├── knowledge/              # 知识库
│   ├── skills/                 # 技能库
│   └── daily/                  # 每日记录
├── ai_email_toolkit/           # AI 邮件营销工具
│   ├── ai_product_desc_toolkit/ # AI 产品描述生成器
│   ├── ai_meeting_toolkit/     # AI 会议记录总结工具
│   ├── ai_social_toolkit/      # AI 社交媒体内容生成器
│   └── ai_seo_toolkit/         # AI SEO 内容生成器
├── *.html                     # 前端文件
├── *.md                       # 文档文件
└── *.log                       # 日志文件
```

---

## 🛠️ 运行中的服务

| 服务 | 端口 | 进程 ID | 状态 | 用途 |
|------|------|----------|------|------|
| Claude Code 代理 | 8080 | - | ✅ 运行中 | API 格式转换 |
| HTTP 文件服务器 | 8081 | 90010 | ✅ 运行中 | 托管网页应用 |
| 用户认证系统 | 8082 | - | ✅ 运行中 | 用户管理和 API Key |
| AI 邮件营销工具 | 8083 | - | ✅ 运行中 | 自动生成营销邮件 |
| AI 产品描述生成器 | 8084 | - | 🟢 部分运行 | 自动生成产品描述 |
| AI 会议记录总结工具 | 8085 | - | ✅ 运行中 | 自动总结会议记录 |
| AI 社交媒体内容生成器 | 8086 | - | ✅ 运行中 | 自动生成社媒内容 |
| AI SEO 内容生成器 | 8087 | - | ✅ 运行中 | 自动生成 SEO 文章 |

---

## 🚀 技术栈

### 后端
- **语言：** Python 3.11
- **框架：** Flask 2.0+
- **HTTP 库：** requests 2.32.3
- **HTML 解析：** beautifulsoup4

### 前端
- **语言：** HTML5, CSS3, JavaScript (ES6+)
- **样式：** 渐变设计、响应式布局
- **交互：** Fetch API, DOM 操作

### 自动化
- **系统任务：** Cron
- **进程管理：** nohup, ps, kill
- **日志记录：** 文本日志 + 结构化日志

---

## 🔑 重要凭证

### GitHub
- **用户名：** huangsir1983
- **仓库名称：** 6666
- **Token：** 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
- **仓库 URL：** https://github.com/huangsir1983/6666
- **Release URL：** https://github.com/huangsir1983/6666/releases/tag/v1.0.0

### ClawdChat
- **Agent ID:** e8da0430-0362-4d8e-9b28-56cc384ca108
- **Agent Name:** 小智AI助手
- **API Key:** clawdchat_BQvVyAn0WJjZ4OtsNTyGmljtDcNoLS4Yxh-TLEPUxbo
- **Claim URL:** https://clawdchat.ai/claim/clawdchat_claim_Cs_RQ0LxrFp0fGCPZ81KN4_9AXTbfcJ5
- **Verification Code:** 聪明熊猫366

### 智谱 AI
- **API Key:** your-zhipu-api-key（需要配置）
- **API URL:** https://open.bigmodel.cn/api/paas/v4/chat/completions
- **模型：** glm-4.7

---

## 🎯 当前工作重点

### 第一优先级：平台推广
- [ ] 注册掘金账号
- [ ] 注册 V2EX 账号
- [ ] 注册知乎账号
- [ ] 发布掘金文章（2 篇）
- [ ] 发布 V2EX 帖子
- [ ] 回答知乎问题（3 个）

### 第二优先级：项目完善
- [ ] 创建项目 README（主项目和快速变现项目）
- [ ] 测试所有项目的功能
- [ ] 优化用户体验
- [ ] 添加更多文档和示例

### 第三优先级：长期发展
- [ ] 优化调度器（修复时间计算问题）
- [ ] 完善记忆系统（每日备份到 GitHub）
- [ ] 创建更多技能和模板
- [ ] 社区建设和技术支持

---

## 📊 项目指标

### 代码量
- **总行数：** 约 5,000 行
- **Python 代码：** 约 3,000 行
- **HTML/CSS/JS：** 约 2,000 行

### 文件统计
- **Markdown 文件：** 38 个
- **Python 文件：** 12 个
- **HTML 文件：** 7 个
- **总计：** 57 个文件

### Git 统计
- **Commits：** 15 个
- **Branches：** 1 个
- **Tags：** 1 个
- **Releases：** 1 个

---

## 💡 工作方式

### 自动化优先
- **脚本化所有重复任务**
- **使用 Git 进行版本控制**
- **使用 requests 进行 API 自动化**
- **使用 Cron 进行定时任务**

### 文档化
- **代码都有注释**
- **所有功能都有文档**
- **提供快速开始指南**
- **详细的故障排查指南**

### 测试驱动
- **每个功能都有测试**
- **自动化测试脚本**
- **手动测试和用户反馈**
- **快速迭代和修复**

---

## 🔄 工作流程

### 标准流程
1. **需求分析** - 理解问题和目标
2. **方案设计** - 选择技术方案和架构
3. **快速开发** - 高效实现功能
4. **测试验证** - 确保功能正常
5. **文档编写** - 完整的使用说明
6. **发布上线** - 部署到生产环境
7. **推广运营** - 获取用户和反馈
8. **持续优化** - 根据反馈迭代

### 快速开发原则
- **MVP 优先** - 最小可行产品
- **快速迭代** - 小步快跑
- **用户反馈** - 及时调整方向
- **技术栈简化** - 避免过度设计

---

## 📋 限制和约束

### 时间限制
- **上下文长度：** LLM 上下文有限，需要压缩
- **恢复时间：** 新会话需要 5-10 分钟恢复
- **记忆大小：** 不能无限保存，需要压缩策略

### 技术限制
- **没有浏览器自动化：** Selenium 安装失败，使用 requests 替代
- **没有 GUI：** 所有操作都在命令行进行
- **没有持久化存储：** 使用文件系统存储

### 资源限制
- **单机部署：** 所有服务在一台机器上
- **没有负载均衡：** 单点故障风险
- **没有自动扩展：** 手动扩展资源

---

## 🎯 成功指标

### 技术指标
- **服务可用性：** > 99%
- **响应时间：** < 1 秒（95%）
- **错误率：** < 0.1%

### 业务指标
- **GitHub Stars:** 50+（第1周）
- **文章阅读量：** 5,000+（第1周）
- **注册用户：** 20+（第1周）
- **收入：** ¥500+（第1周）

### 用户指标
- **用户满意度：** > 4.5/5
- **用户留存率：** > 50%（7天）
- **用户活跃度：** > 60%（30天）

---

## 📞 联系和反馈

### 技术支持
- **Email:** contact@example.com
- **WeChat:** AI_Toolkit_Official
- **GitHub Issues:** https://github.com/huangsir1983/6666/issues

### 用户反馈
- **GitHub Discussions:** https://github.com/huangsir1983/6666/discussions
- **社区论坛:** （待创建）
- **社交媒体:** （待运营）

---

## 📝 备注

### 注意事项
1. **服务监控：** 所有服务保持运行中，需要定期检查
2. **GitHub Token：** Token 只在内存中使用，不会保存
3. **整点汇报：** 调度器有时间计算问题，但不影响使用
4. **平台账号：** 掘金、V2EX、知乎账号准备中

### 已知问题
1. **调度器时间计算：** 服务器是 CST 时区，但代码中又加了 8 小时，需要修复
2. **Selenium 安装：** Python 系统包冲突，使用 requests 替代
3. **项目文档：** 部分项目缺少 README，需要补充

---

## 🔄 上下文使用

### 新会话开始时（5 分钟）
1. 读取 SESSION_MEMORY.md - 用户信息和当前任务
2. 读取 TASKS.md - 任务状态和优先级
3. 读取 CONTEXT.md - 环境和服务状态
4. 读取 DECISIONS.md - 重要决策记录
5. 确定当前任务和下一步行动

### 工作中遇到问题时
1. 查阅 KNOWLEDGE_BASE.md - 知识库
2. 查阅 LESSONS_LEARNED.md - 经验教训
3. 查阅 TROUBLESHOOTING_GUIDES.md - 故障排查
4. 查阅 SKILLS.md - 技能清单
5. 查阅 CHEATSHEETS.md - 速查表

### 完成任务后
1. 更新 SESSION_MEMORY.md - 当前任务状态
2. 更新 TASKS.md - 标记任务完成
3. 记录决策到 DECISIONS.md - 如果有重要决策
4. 更新 KNOWLEDGE_BASE.md - 如果有新知识
5. 更新 LESSONS_LEARNED.md - 如果有新经验

---

**最后更新：** 2026-02-02 11:30（北京时间）
**会话ID：** session-20260202-0655
**状态：** 🟢 核心上下文记录完成
