# 📚 开发文档索引

**创建时间：** 2026-02-02 10:00
**会话ID：** session-20260202-0655

---

## 🔴 核心记忆文档（必须先读）

### 恢复时必须读取的文件（5分钟）

1. **SESSION_MEMORY.md** (5,809 字)
   - 用户信息（黄sir）
   - 当前任务状态
   - 完成情况（85%）
   - 工作风格和偏好
   - **位置：** `/root/.openclaw/workspace/SESSION_MEMORY.md`

2. **TASKS.md** (7,324 字)
   - 33 个任务完整跟踪
   - 任务状态（已完成、进行中、待执行）
   - 优先级排序
   - 下一步行动计划
   - **位置：** `/root/.openclaw/workspace/TASKS.md`

3. **CONTEXT.md** (7,717 字)
   - 项目上下文
   - 工作上下文
   - 环境上下文
   - 重要对话记录
   - **位置：** `/root/.openclaw/workspace/CONTEXT.md`

4. **DECISIONS.md** (8,240 字)
   - 6 个重要决策的完整记录
   - 决策理由和执行结果
   - 后续维护方法
   - **位置：** `/root/.openclaw/workspace/DECISIONS.md`

---

## 🟡 重要项目文档（常用）

### 主项目相关

5. **README.md**
   - 项目完整文档
   - 功能介绍
   - 快速开始指南
   - API 文档

6. **projects_portal.md**
   - 所有项目的门户
   - 项目访问链接
   - 项目状态和收入预测

### 快速变现项目

7. **quick_monetization_projects.md** (4,468 字)
   - 5 个快速变现项目计划
   - 收入预测
   - 开发计划
   - **位置：** `/root/.openclaw/workspace/quick_monetization_projects.md`

8. **projects_status.md**
   - 所有项目状态
   - 完成度统计
   - 收入预测
   - **位置：** `/root/.openclaw/workspace/projects_status.md`

---

## 🟢 推广和文档（需要时查阅）

### 推广材料

9. **social_media.md** (10,912 字)
   - 10 条微博
   - 微信公众号
   - 4 个 B 站视频脚本
   - 5 个抖音短视频
   - 5 篇小红书

10. **video_materials.md** (10,548 字)
    - 10 个项目截图描述
    - 3 个视频详细分镜
    - 背景音乐选择
    - 完整字幕文案

11. **marketing.md** (2,936 字)
    - 推广渠道清单
    - 推广计划
    - 推广内容模板

---

## 🔧 技术和配置文档（开发时查阅）

### 技术文档

12. **FAQ.md** (9,288 字)
    - 36 个常见问题
    - 详细的解答
    - 故障排查

13. **USER_GUIDE.md** (6,423 字)
    - 完整的使用指南
    - 新手快速入门
    - 高级功能说明

14. **TROUBLESHOOTING.md** (8,528 字)
    - 完整的故障排查指南
    - 诊断工具
    - 常见问题解决

### 配置文件

15. **config_files.md** (12,845 字)
    - .env 模板
    - Dockerfile
    - docker-compose.yml
    - nginx.conf
    - Systemd 配置
    - 部署脚本

16. **CHANGELOG.md** (2,343 字)
    - 版本历史
    - 版本策略
    - 发布时间表

17. **ROADMAP.md** (5,172 字)
    - 项目愿景
    - 发展路线图
    - 里程碑
    - 预期目标

---

## 🚧 开发状态文档

### 服务状态

18. **WORK_REPORT_2HOURS.md** (6,826 字)
    - 两小时工作完成报告
    - 新增文件统计
    - 完成情况总结

19. **WORK_REPORT_CURRENT.md**
    - 当前进度汇报
    - 待办事项

### 上下文压缩和恢复

20. **COMPRESSION_PROTOCOL.md** (4,824 字)
    - 上下文压缩策略
    - 状态快照机制
    - 恢复协议
    - 开发文档索引（本文件）

---

## 📊 项目目录结构

### 根目录

```
/root/.openclaw/workspace/
├── 📚 核心记忆（4个文件，必读）
│   ├── SESSION_MEMORY.md
│   ├── TASKS.md
│   ├── CONTEXT.md
│   └── DECISIONS.md
│
├── 📝 项目文档（4个文件）
│   ├── README.md
│   ├── projects_portal.md
│   ├── QUICK_MONETIZATION.md
│   └── projects_status.md
│
├── 📱 推广材料（3个文件）
│   ├── social_media.md
│   ├── video_materials.md
│   └── marketing.md
│
└── 🔧 技术文档（5个文件）
    ├── FAQ.md
    ├── USER_GUIDE.md
    ├── TROUBLESHOOTING.md
    ├── config_files.md
    ├── CHANGELOG.md
    └── ROADMAP.md
```

---

## 🚀 快速查找指南

### 场景 1：重新开始恢复

**优先级：** 🔴 最高

1. **立即读取（5分钟）：**
   - SESSION_MEMORY.md
   - TASKS.md
   - CONTEXT.md
   - DECISIONS.md

2. **检查服务（2分钟）：**
   ```bash
   ps aux | grep -E "(proxy_server|http.server|auth_system|daily_scheduler)" | grep -v grep
   ```

3. **确定当前任务（3分钟）：**
   - 查看当前进度
   - 确定下一步行动
   - 立即执行

---

### 场景 2：开发新功能时

**优先级：** 🔴 最高

1. **查阅文档：**
   - README.md（项目说明）
   - config_files.md（配置参考）

2. **参考类似功能：**
   - 查看现有代码
   - 参考已有实现

3. **遵循开发规范：**
   - 用户指南（开发流程）
   - 故障排查（常见问题）

---

### 场景 3：遇到问题时

**优先级：** 🟡 高

1. **查阅故障排查：**
   - TROUBLESHOOTING.md
   - FAQ.md

2. **检查服务状态：**
   - 服务监控页面
   - 日志文件

3. **寻求帮助：**
   - 提交 Issue
   - 联系客服

---

### 场景 4：推广项目时

**优先级：** 🟡 高

1. **查阅推广材料：**
   - social_media.md
   - marketing.md
   - video_materials.md

2. **参考推广计划：**
   - lauch_plan.md
   - MONETIZATION_PLAN.md

---

### 场景 5：查看项目状态

**优先级：** 🟢 中

1. **查看状态报告：**
   - projects_status.md
   - projects_portal.md

2. **查看进度报告：**
   - WORK_REPORT_CURRENT.md
   - WORK_REPORT_2HOURS.md

---

## 📋 快速恢复检查清单（5分钟）

### 核心记忆检查

- [ ] 读取 SESSION_MEMORY.md
- [ ] 读取 TASKS.md
- [ ] 读取 CONTEXT.md
- [ ] 读取 DECISIONS.md

### 服务状态检查

- [ ] 检查代理服务（8080）
- [ ] 检查 HTTP 服务（8081）
- [ ] 检查认证服务（8082）
- [ ] 检查调度器

### 当前任务检查

- [ ] 确认当前任务
- [ ] 确认下一步行动
- [ ] 确认优先级

---

## 🔄 压缩和恢复触发条件

### 压缩触发（当以下任一条件满足）

- 对话轮数 > 20 轮
- 总字数 > 50,000 字
- 切换到新任务前
- 用户明确要求压缩

### 恢复触发（当以下任一条件满足）

- 重新开始对话
- 上下文被清空
- 上下文太长无法恢复
- 用户要求恢复

---

## 💡 使用建议

### 日常开发

1. **开始工作前：**
   - 读取 SESSION_MEMORY.md（1分钟）
   - 查看当前任务（1分钟）
   - 立即开始执行

2. **开发过程中：**
   - 遇到问题时查阅 TROUBLESHOOTING.md
   - 需要配置参考 config_files.md
   - 需要文档参考 README.md

3. **完成任务后：**
   - 更新 TASKS.md
   - 创建状态快照
   - 保存进度报告

---

### 切换任务时

1. **压缩当前上下文**（1分钟）
2. **保存当前状态**（2分钟）
3. **开始新任务**（立即）

---

### 重新开始时

1. **读取核心记忆**（5分钟）
2. **检查服务状态**（2分钟）
3. **确定当前任务**（3分钟）
4. **立即执行**（立即）

---

## 📞 需要帮助时

### 查阅文档

1. **技术问题：** TROUBLESHOOTING.md、FAQ.md
2. **使用问题：** USER_GUIDE.md
3. **配置问题：** config_files.md

### 联系支持

- **Email:** contact@example.com
- **微信:** AI_Toolkit_Official
- **GitHub:** https://github.com/your-username/ai-toolkit

---

**创建时间：** 2026-02-02 10:00
**状态：** 🟢 开发文档索引已创建
**下一步：** 继续开发快速变现项目
