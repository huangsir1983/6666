# 📘 用户使用指南

**项目：** AI 工具箱
**目标：** 帮助新用户快速上手
**安全：** 不含任何敏感信息

---

## 🎯 新手快速入门（5分钟）

### 第一步：了解项目

AI 工具箱是一个完整的 AI API 服务平台，让你可以：

✅ **免费使用 AI API** - 每天 100 次免费调用
✅ **兼容 Claude Code** - 让 Claude Code 使用智谱 AI
✅ **丰富的应用工具** - 聊天、故事、代码生成等
✅ **完整的用户系统** - API Key 管理、用量统计

---

### 第二步：选择使用方式

#### 方式 A：使用在线服务（推荐新手）

**适合：** 不想自己部署，快速体验

**步骤：**
1. 访问主页：http://your-server:8081/
2. 注册账号获取 API Key
3. 开始使用

**优点：**
- ✅ 无需安装任何软件
- ✅ 5 分钟即可开始
- ✅ 自动维护更新

**缺点：**
- ❌ 需要联网
- ❌ 有调用限制

---

#### 方式 B：自己部署（推荐开发者）

**适合：** 需要完全控制，高级使用

**步骤：**
```bash
# 1. 克隆项目
git clone https://github.com/your-username/ai-toolkit.git
cd ai-toolkit

# 2. 安装依赖
pip install flask requests

# 3. 配置智谱 API Key
echo "ZHIPU_API_KEY=your-key" > .env

# 4. 启动服务
python3 proxy_server_v2.py
python3 auth_system.py
```

**优点：**
- ✅ 完全免费（除了智谱 API）
- ✅ 无限调用（受智谱限制）
- ✅ 完全控制

**缺点：**
- ❌ 需要技术基础
- ❌ 需要维护服务器

---

### 第三步：开始使用

#### 使用在线应用（最简单）

1. **智能聊天**
   - 访问：http://your-server:8081/glm_chat.html
   - 直接开始对话

2. **故事生成**
   - 访问：http://your-server:8081/ai_story.html
   - 选择类型，生成故事

3. **代码生成**
   - 访问：http://your-server:8081/code_generator.html
   - 输入需求，生成代码

---

#### 使用 API（开发者）

**注册获取 API Key：**
```bash
curl -X POST http://localhost:8082/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your@email.com",
    "password": "password123"
  }'
```

**调用 API：**
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

#### 配置 Claude Code（高级）

```bash
# 设置环境变量
export ANTHROPIC_API_URL=http://localhost:8080
export ANTHROPIC_API_KEY=YOUR_API_KEY

# 或在配置文件中添加
export ANTHROPIC_API_URL="http://localhost:8080"
export ANTHROPIC_API_KEY="YOUR_API_KEY"
```

现在 Claude Code 会自动调用智谱 AI！

---

## 📚 详细使用教程

### 1. 智能聊天助手

**访问：** http://your-server:8081/glm_chat.html

**功能：**
- ✅ 实时对话
- ✅ 代码高亮
- ✅ 历史记录
- ✅ 多主题支持

**使用技巧：**
1. 可以问任何问题
2. 支持代码生成和解释
3. 可以设置系统提示词
4. 支持多轮对话

**示例：**
```
用户：帮我写一个 Python 函数，计算斐波那契数列
AI：当然可以！这是计算斐波那契数列的 Python 函数：

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

这个函数使用递归方式计算斐波那契数列...
```

---

### 2. AI 故事生成器

**访问：** http://your-server:8081/ai_story.html

**功能：**
- ✅ 多种故事类型（科幻、奇幻、悬疑等）
- ✅ 自定义角色和场景
- ✅ 交互式剧情分支
- ✅ 历史记录

**使用技巧：**
1. 选择故事类型
2. 设置主要角色
3. 选择故事长度
4. 点击生成

**示例：**
```
类型：科幻
角色：小明，一个普通的程序员
长度：中等

生成结果：
公元 2077 年，小明像往常一样坐在办公室里写代码...
```

---

### 3. 代码生成器

**访问：** http://your-server:8081/code_generator.html

**功能：**
- ✅ 支持多种编程语言
- ✅ 多种代码类型（函数、类、算法等）
- ✅ 预设模板
- ✅ 一键复制

**使用技巧：**
1. 选择编程语言
2. 选择代码类型
3. 描述需求
4. 生成代码

**示例：**
```
语言：Python
类型：算法
需求：快速排序

生成结果：
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
```

---

### 4. 冷知识卡片

**访问：** http://your-server:8081/ai_facts.html

**功能：**
- ✅ 随机有趣知识
- ✅ 多分类别（科学、历史、地理等）
- ✅ 卡片翻转动画
- ✅ 分享功能

**使用技巧：**
1. 选择类别
2. 点击生成
3. 翻转卡片查看详情
4. 分享给朋友

---

### 5. 排序可视化

**访问：** http://your-server:8081/bubble_sort.html

**功能：**
- ✅ 可视化冒泡排序
- ✅ 交互式控制
- ✅ 动画演示
- ✅ 算法说明

**使用技巧：**
1. 生成随机数组
2. 点击开始排序
3. 观察排序过程
4. 理解算法原理

---

## 🔧 高级功能

### 1. API 高级用法

#### 系统提示词

```json
{
  "messages": [
    {"role": "system", "content": "你是一个专业的程序员"},
    {"role": "user", "content": "帮我写一个快速排序"}
  ]
}
```

#### 多轮对话

```json
{
  "messages": [
    {"role": "user", "content": "什么是 Python？"},
    {"role": "assistant", "content": "Python 是一种高级编程语言..."},
    {"role": "user", "content": "它有什么特点？"}
  ]
}
```

#### 流式响应

```python
response = requests.post(API_URL, headers=headers, json=data, stream=True)

for chunk in response.iter_content(chunk_size=1024):
    if chunk:
        print(chunk.decode('utf-8'), end='')
```

---

### 2. 用量管理

#### 查看使用量

```bash
curl http://localhost:8082/auth/usage \
  -H "X-API-Key: YOUR_API_KEY"
```

#### 设置限额提醒

在应用中监控 API 调用次数：
```python
response = requests.post(API_URL, ...)
if response.status_code == 429:
    print("API 调用次数已达限制，请升级套餐")
```

---

### 3. 错误处理

#### 基础错误处理

```python
try:
    response = requests.post(API_URL, ...)
    result = response.json()

    if response.status_code == 200:
        print(result['content'][0]['text'])
    else:
        print(f"错误: {result.get('error', '未知错误')}")

except Exception as e:
    print(f"异常: {e}")
```

#### 重试机制

```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_api(data):
    return requests.post(API_URL, headers=headers, json=data)
```

---

### 4. 性能优化

#### 使用缓存

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_chat(content_hash):
    # 调用 API
    pass

# 使用
content_hash = hashlib.md5(content.encode()).hexdigest()
result = cached_chat(content_hash)
```

#### 批量请求

```python
# 并发请求
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(call_api, data) for data in data_list]
    results = [f.result() for f in futures]
```

---

## 🎓 学习路径

### 初学者（第1-3天）

**目标：** 基本使用

1. ✅ 体验在线应用（聊天、故事、代码生成）
2. ✅ 注册账号，获取 API Key
3. ✅ 尝试简单的 API 调用
4. ✅ 了解项目功能

**推荐资源：**
- README.md - 项目介绍
- FAQ.md - 常见问题
- 在线应用 - 直接体验

---

### 进阶用户（第4-7天）

**目标：** API 开发

1. ✅ 学习 API 文档
2. ✅ 实现一个简单应用
3. ✅ 配置 Claude Code
4. ✅ 部署自己的服务

**推荐资源：**
- API 文档
- 视频教程
- 代码示例

---

### 高级用户（第2周+）

**目标：** 深度开发

1. ✅ 自己部署服务
2. ✅ 定制功能
3. ✅ 优化性能
4. ✅ 贡献代码

**推荐资源：**
- 源代码
- 贡献指南
- 技术交流群

---

## 💡 最佳实践

### 1. 安全建议

- ✅ 保护好 API Key，不要泄露
- ✅ 使用 HTTPS 生产环境
- ✅ 实现请求限流
- ✅ 定期更新依赖

---

### 2. 性能建议

- ✅ 使用缓存减少重复调用
- ✅ 批量请求提高效率
- ✅ 合理设置 max_tokens
- ✅ 监控 API 调用次数

---

### 3. 成本建议

- ✅ 充分利用免费额度
- ✅ 缓存常用请求
- ✅ 选择合适的套餐
- ✅ 监控使用量

---

## 📞 获取帮助

### 遇到问题？

1. **查看 FAQ** - FAQ.md
2. **搜索 Issues** - GitHub Issues
3. **提交 Issue** - 创建新的 Issue
4. **联系客服** - contact@example.com

---

### 想要更多功能？

1. **提出建议** - GitHub Discussions
2. **提交 PR** - 直接贡献代码
3. **联系定制** - 企业定制服务

---

## 🎉 总结

恭喜你快速上手 AI 工具箱！

现在你可以：
- ✅ 免费使用 AI API
- ✅ 开发自己的 AI 应用
- ✅ 兼容 Claude Code
- ✅ 体验丰富的 AI 工具

继续探索，发现更多可能！

---

**最后更新：** 2026-02-02
**版本：** 1.0.0
**适合人群：** 所有用戶
