# 💰 GitHub 消费分析（$0.1）

**分析时间：** 2026-02-03 20:40
**目的：** 分析 GitHub $0.1 消费的原因，并提供避免消费和付费方案

---

## 📊 GitHub 计费模式

### 免费额度（Free Plan）

**价格：** $0/月

**免费额度：**
- ✅ 公共仓库：无限制
- ✅ 私有仓库：无限制（2020 年起）
- ✅ GitHub Pages：1GB 存储
- ✅ GitHub Actions：2000 分钟/月
- ✅ GitHub Packages：500MB 存储
- ✅ GitHub Codespaces：60 小时/月
- ✅ GitHub API：5000 请求/小时

**限制：**
- ⚠️ GitHub Actions 超出 2000 分钟/月会按使用量计费
- ⚠️ GitHub Packages 超出 500MB 存储会按存储量计费
- ⚠️ GitHub Codespaces 超出 60 小时/月会按使用量计费

---

## 🚨 $0.1 消费可能的原因

### 原因 1：GitHub Actions 时间消费（最可能）

**场景：** GitHub Actions 自动化任务超出了免费额度

**免费额度：** 2000 分钟/月

**超出计费：** $0.008/分钟（Linux/Windows）

**计算：**
```
$0.1 / $0.008/分钟 = 12.5 分钟
```

**结论：** 可能超出了 2000 分钟/月的免费额度，额外使用了约 12.5 分钟的 Actions 时间。

**可能触发的原因：**
- CI/CD 自动化测试
- 自动部署
- 定时任务（Scheduled Jobs）
- 工作流自动化（Workflow Automations）

---

### 原因 2：GitHub Packages 存储消费

**场景：** GitHub Packages 存储超出了免费额度

**免费额度：** 500MB 存储

**超出计费：** $0.25/GB/月

**计算：**
```
$0.1 / $0.25/GB/月 = 0.4 GB/月
```

**结论：** 可能超出了 500MB 的免费存储，额外使用了约 0.4GB 的存储空间。

**可能触发的原因：**
- 发布 NPM 包
- 发布 Docker 镜像
- 发布其他包

---

### 原因 3：GitHub Codespaces 时间消费

**场景：** GitHub Codespaces 云开发环境超出了免费额度

**免费额度：** 60 小时/月

**超出计费：** $0.18/小时

**计算：**
```
$0.1 / $0.18/小时 = 0.56 小时 ≈ 33 分钟
```

**结论：** 可能超出了 60 小时/月的免费额度，额外使用了约 33 分钟的 Codespaces 时间。

**可能触发的原因：**
- 使用 GitHub Codespaces 云开发
- 远程开发环境
- 临时测试环境

---

### 原因 4：GitHub Copilot 订阅

**场景：** GitHub Copilot 订阅费用

**价格：** $10/月（或 $100/年）

**计算：**
```
$0.1 < $10/月
```

**结论：** 不太可能是 GitHub Copilot 订阅，因为 $0.1 远低于 $10/月。

**可能触发的原因：**
- 试用期或部分退款

---

### 原因 5：GitHub Pro 订阅

**场景：** GitHub Pro 订阅费用

**价格：** $4/月（或 $48/年）

**计算：**
```
$0.1 < $4/月
```

**结论：** 不太可能是 GitHub Pro 订阅，因为 $0.1 远低于 $4/月。

**可能触发的原因：**
- 试用期或部分退款

---

### 原因 6：其他付费功能

**场景：** 其他 GitHub 付费功能

**可能的付费功能：**
- GitHub Sponsors（赞助）
- GitHub Advanced Security（高级安全）
- GitHub Team 或 Enterprise（团队或企业版）

**结论：** 不太可能是这些功能，因为 $0.1 的金额很小。

---

## 🎯 最可能的原因

### 结论：GitHub Actions 时间消费（最可能）

**原因：**
1. **金额匹配：** $0.1 大约等于 12.5 分钟的 GitHub Actions 时间消费
2. **常见场景：** GitHub Actions 是最容易超出的免费额度
3. **计费模式：** GitHub Actions 按使用量计费（超出免费额度）

**验证：**
1. 访问：https://github.com/settings/billing
2. 查看 "Usage-based billing" 部分
3. 查看 "GitHub Actions" 的使用记录

---

## 📋 查看消费详情

### 步骤 1：访问计费页面

**访问：** https://github.com/settings/billing

**查看内容：**
- "Usage-based billing"（基于使用量的计费）
- "Monthly usage"（月度使用情况）
- "Payment history"（支付历史）

---

### 步骤 2：查看 GitHub Actions 使用情况

**访问：** https://github.com/settings/billing

**查看内容：**
- "GitHub Actions" 部分
- "Usage minutes"（使用分钟数）
- "Billable minutes"（可计费分钟数）

---

### 步骤 3：查看消费明细

**访问：** https://github.com/settings/billing

**查看内容：**
- "Payment history"（支付历史）
- "Invoices"（账单）
- "Receipts"（收据）

---

## 💡 避免不必要消费的方法

### 方法 1：减少 GitHub Actions 使用

**优化策略：**
- 减少 CI/CD 测试频率
- 优化工作流，减少不必要的步骤
- 取消定时任务（Scheduled Jobs）

**实施：**
```yaml
# 优化 GitHub Actions 工作流
name: Optimized Workflow

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10  # 限制 10 分钟
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: npm run build
      - name: Test
        run: npm test
```

---

### 方法 2：使用 GitHub Actions 缓存

**优化策略：**
- 缓存 npm 依赖
- 缓存构建结果
- 减少重复下载和构建

**实施：**
```yaml
# 使用 GitHub Actions 缓存
name: Cached Workflow

on:
  push:
    branches: [master]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      # 缓存 npm 依赖
      - name: Cache node modules
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-
      
      - name: Install dependencies
        run: npm ci
      
      # 缓存构建结果
      - name: Cache build
        uses: actions/cache@v3
        with:
          path: dist
          key: ${{ runner.os }}-build-${{ github.sha }}
      
      - name: Build
        run: npm run build
```

---

### 方法 3：使用付费方案（如果需要）

**方案 1：GitHub Team（$4/用户/月）**

**价格：** $4/用户/月

**优势：**
- GitHub Actions：3000 分钟/月（+50%）
- GitHub Packages：2GB 存储（+300%）
- 团队管理和协作

**适用场景：**
- 小型团队
- 需要 Actions 更多时间
- 需要 Packages 更多存储

**购买：**
1. 访问：https://github.com/settings/billing
2. 点击 "Change plan"
3. 选择 "Team" 或 "Enterprise"

---

**方案 2：GitHub Pro（$4/月）**

**价格：** $4/月

**优势：**
- GitHub Actions：3000 分钟/月（+50%）
- GitHub Pages：无限制
- GitHub Packages：2GB 存储（+300%）
- GitHub Codespaces：无限制

**适用场景：**
- 个人开发者
- 需要 Actions 更多时间
- 需要 Pages 无限制
- 需要 Packages 更多存储

**购买：**
1. 访问：https://github.com/settings/billing
2. 点击 "Change plan"
3. 选择 "Pro"

---

**方案 3：GitHub Enterprise（$21/用户/月）**

**价格：** $21/用户/月

**优势：**
- GitHub Actions：50000 分钟/月（无限制）
- GitHub Packages：无限制
- GitHub Pages：无限制
- GitHub Codespaces：无限制
- SSO（单点登录）
- 审计日志

**适用场景：**
- 大型企业
- 政府机构
- 需要合规性管理

**购买：**
1. 访问：https://github.com/settings/billing
2. 点击 "Change plan"
3. 选择 "Enterprise"

---

## 🎯 单独付费步骤

### 步骤 1：访问计费页面

**访问：** https://github.com/settings/billing

**查看内容：**
- 当前计划（Free、Pro、Team、Enterprise）
- 月度消费（$0.1）
- 支付方式

---

### 步骤 2：查看消费明细

**访问：** https://github.com/settings/billing

**查看内容：**
- "Usage-based billing"（基于使用量的计费）
- "Monthly usage"（月度使用情况）
- "Payment history"（支付历史）

---

### 步骤 3：选择付费方案

**选项 1：升级到 GitHub Pro**

**步骤：**
1. 访问：https://github.com/settings/billing
2. 点击 "Change plan"
3. 选择 "Pro"
4. 添加支付方式（信用卡、PayPal）
5. 确认升级

**效果：**
- GitHub Actions：3000 分钟/月（+50%）
- GitHub Pages：无限制
- GitHub Packages：2GB 存储（+300%）
- GitHub Codespaces：无限制

---

**选项 2：升级到 GitHub Team**

**步骤：**
1. 访问：https://github.com/settings/billing
2. 点击 "Change plan"
3. 选择 "Team"
4. 添加支付方式（信用卡、PayPal）
5. 确认升级

**效果：**
- GitHub Actions：3000 分钟/月（+50%）
- GitHub Packages：2GB 存储（+300%）
- 团队管理和协作

---

**选项 3：单独付费（按使用量）**

**步骤：**
1. 访问：https://github.com/settings/billing
2. 查看 "Usage-based billing"
3. 设置 "Payment limit"（支付限制）
4. 添加支付方式（信用卡、PayPal）

**效果：**
- 按实际使用量付费
- 没有固定月费
- 适合偶发使用

---

## 💡 推荐方案

### 短期：减少 GitHub Actions 使用

**原因：** $0.1 是很小的金额，可能是偶发消费

**方法：**
- 减少 CI/CD 测试频率
- 优化工作流，减少不必要的步骤
- 取消定时任务

**实施：**
- 查看仓库的 Actions 使用记录
- 识别高消耗的工作流
- 优化或取消高消耗的工作流

---

### 中期：升级到 GitHub Pro（如果需要）

**原因：** 如果 GitHub Actions 使用频繁，升级到 GitHub Pro 更划算

**价格：** $4/月

**优势：**
- GitHub Actions：3000 分钟/月（+50%）
- GitHub Pages：无限制
- GitHub Packages：2GB 存储（+300%）
- GitHub Codespaces：无限制

**实施：**
1. 访问：https://github.com/settings/billing
2. 点击 "Change plan"
3. 选择 "Pro"
4. 添加支付方式
5. 确认升级

---

### 长期：单独付费（按使用量）

**原因：** 如果 GitHub Actions 使用不频繁，按使用量付费更划算

**价格：** 按实际使用量付费

**优势：**
- 没有固定月费
- 只为使用的分钟数付费
- 适合偶发使用

**实施：**
1. 访问：https://github.com/settings/billing
2. 查看 "Usage-based billing"
3. 设置 "Payment limit"（如 $5/月）
4. 添加支付方式

---

## 📊 消费对比

### 免费版 vs GitHub Pro

| 指标 | 免费版 | GitHub Pro ($4/月) | 改进 |
|------|--------|------------------|------|
| GitHub Actions | 2000 分钟/月 | 3000 分钟/月 | +50% |
| GitHub Pages | 1GB | 无限制 | ∞ |
| GitHub Packages | 500MB | 2GB | +300% |
| GitHub Codespaces | 60 小时/月 | 无限制 | ∞ |
| 月费 | $0 | $4 | +$4 |

**对比：** GitHub Pro 提供 50% 的 Actions 时间，但需要 $4/月的固定月费。

---

### 按使用量付费

**计费模式：** 超出免费额度后按使用量计费

**GitHub Actions：** $0.008/分钟（Linux/Windows）

**计算：**
```
超出 12.5 分钟 = $0.1
超出 100 分钟 = $0.8
超出 500 分钟 = $4
超出 1000 分钟 = $8
```

**对比：**
- 超出 500 分钟（$4）等于 GitHub Pro 的价格（$4/月）
- 如果超出少于 500 分钟/月，按使用量付费更划算
- 如果超出多于 500 分钟/月，GitHub Pro 更划算

---

## 🎯 结论

### $0.1 消费的最可能原因

**最可能的原因：** GitHub Actions 时间消费（超出免费额度 2000 分钟/月，额外使用了约 12.5 分钟）

**其他可能的原因：**
- GitHub Packages 存储消费（超出 500MB，额外使用了约 0.4GB）
- GitHub Codespaces 时间消费（超出 60 小时/月，额外使用了约 33 分钟）

---

### 如何避免不必要消费

**方法 1：减少 GitHub Actions 使用**
- 减少 CI/CD 测试频率
- 优化工作流，减少不必要的步骤
- 取消定时任务

**方法 2：使用 GitHub Actions 缓存**
- 缓存 npm 依赖
- 缓存构建结果
- 减少重复下载和构建

**方法 3：升级到 GitHub Pro**
- 如果 GitHub Actions 使用频繁
- GitHub Actions：3000 分钟/月（+50%）
- 价格：$4/月

**方法 4：按使用量付费**
- 如果 GitHub Actions 使用不频繁
- 按实际使用量付费
- 没有固定月费

---

### 如何单独付费

**步骤 1：访问计费页面**
**访问：** https://github.com/settings/billing

**步骤 2：选择付费方案**
- **GitHub Pro：** $4/月（固定月费）
- **GitHub Team：** $4/用户/月（固定月费）
- **按使用量：** $0.008/分钟（超出免费额度）

**步骤 3：添加支付方式**
- 信用卡
- PayPal
- 其他支付方式

**步骤 4：确认升级**
- 确认付费方案
- 确认支付方式
- 确认升级

---

## 📚 参考资料

### GitHub 官方文档
- [GitHub Billing](https://docs.github.com/billing/managing-billing-for-github-products)
- [GitHub Actions Billing](https://docs.github.com/billing/managing-billing-for-github-actions)
- [GitHub Pricing](https://github.com/pricing)

### 第三方资源
- [GitHub Actions 优化](https://docs.github.com/actions/optimization)
- [GitHub Actions 最佳实践](https://docs.github.com/actions/best-practices)

---

**分析完成时间：** 2026-02-03 20:50
**状态：** ✅ 已分析

---

*"GitHub $0.1 消费的最可能原因是 GitHub Actions 时间消费（超出免费额度 2000 分钟/月，额外使用了约 12.5 分钟）。如果 GitHub Actions 使用频繁，建议升级到 GitHub Pro（$4/月）；如果使用不频繁，建议按使用量付费。同时，可以通过减少 Actions 使用、使用缓存等方式避免不必要消费。"* — 小智
