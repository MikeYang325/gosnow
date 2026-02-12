# 追雪项目规则文档

## 📌 重要：每次接手项目必读

### 第一步：阅读文档
1. **必须先��读** `WORKLOG.md` - 了解项目历史和当前状态
2. **必须先阅读** 本文件 `PROJECT_RULES.md` - 了解项目规则
3. **必须先阅读** 最新的待办事项

### 第二步：记录工作
每次开始工作时，在 `WORKLOG.md` 中添加新的日期条目：
```markdown
## YYYY-MM-DD - 工作标题

### 完成的工作
- [ ] 任务1
- [ ] 任务2

### 遇到的问题
- 问题描述和解决方案

### 用户反馈
- 用户的要求和反馈
```

### 第三步：更新状态
工作结束时，更新：
- 完成的任务状态（改为 ✅）
- 待办事项列表
- 最后更新时间

---

## 🚫 禁止事项

### 1. 不要随意更改文件名
- `index.html` 必须是首页
- 详情页格式：`detail_{雪场名}.html`
- 不要在 index.html 和 index_mobile.html 之间切换

### 2. 不要破坏现有功能
- 修改前先测试
- 保持移动端优先设计
- 不要删除已有的数据字段

### 3. 不要跳过部署步骤
- 本地生成后必须部署到服务器
- 部署前先验证本地文件
- 记录部署结果

---

## ✅ 必须遵守的规则

### 1. 代码修改规则
- **修改Python脚本后**，必须重新运行生成HTML
- **修改数据文件后**，必须重新生成页面
- **添加新功能前**，先在 WORKLOG.md 中记录计划

### 2. 数据更新规则
- 天气数据每天至少更新一次
- 更新命令：`python3 fetch_openweather_forecast.py`
- 更新后必须重新生成页面并部署

### 3. 部署规则
- 本地测试通过后才能部署
- 部署方式：`git push origin main`（GitHub Pages 自动部署）
- 部署后验证：访问 https://gosnow.site
- 在 WORKLOG.md 中记录部署时间和结果

### 4. 用户反馈处理规则
- 所有用户反馈必须记录在 WORKLOG.md
- 完成后标记 ✅
- 重大修改需要用户确认

---

## 📂 关键文件说明

### 数据文件（不要手动编辑）
- `resort_details_full.json` - 雪场主数据
- `forecast_7day.json` - 天气预报（自动更新）
- `xiaohongshu_reviews.json` - 用户评价

### 生成脚本（修改后必须重新运行）
- `generate_mobile_version.py` - 生成首页
- `generate_detail_pages.py` - 生成详情页
- `fetch_openweather_forecast.py` - 获取天气

### 输出文件（自动生成，不要手动编辑）
- `index.html` - 首页
- `detail_*.html` - 详情页

---

## 🔄 标准工作流程

### 日常维护
```bash
# 1. 进入项目目录
cd /Users/mac/Documents/cc/gosnow/

# 2. 更新天气数据
python3 fetch_openweather_forecast.py

# 3. 重新生成页面
python3 generate_mobile_version.py
python3 generate_detail_pages.py

# 4. 部署到 GitHub Pages
git add .
git commit -m "更新内容"
git push origin main

# 5. 验证
curl http://gosnow.site

# 6. 记录到 WORKLOG.md
```

### 添加新功能
```bash
# 1. 在 WORKLOG.md 中记录计划
# 2. 修改相应的 Python 脚本
# 3. 本地测试
python3 generate_mobile_version.py
python3 generate_detail_pages.py
open index.html  # 浏览器查看

# 4. 确认无误后部署
# 5. 在 WORKLOG.md 中标记完成
```

### 修改数据
```bash
# 1. 修改 JSON 数据文件
# 2. 重新生成页面
python3 generate_mobile_version.py
python3 generate_detail_pages.py

# 3. 部署
# 4. 记录修改内容到 WORKLOG.md
```

---

## 🔐 敏感信息

### API密钥
- OpenWeatherMap: `***REMOVED***`
- 不要泄露到公开仓库

### 服务器信息
- 域名: `gosnow.site`
- 部署: GitHub Pages（自动部署）

---

## 📝 记录模板

### 每次工作开始时
```markdown
## YYYY-MM-DD HH:MM - [工作内容简述]

### 接手时的状态
- 上一次更新：[日期]
- 待办事项：[列出]
- 已知问题：[列出]

### 本次工作计划
- [ ] 任务1
- [ ] 任务2
```

### 每��工作结束时
```markdown
### 完成的工作
- ✅ 任务1 - 详细说明
- ✅ 任务2 - 详细说明

### 遇到的问题
- 问题1：描述 + 解决方案
- 问题2：描述 + 解决方案

### 新增的待办事项
- [ ] 待办1
- [ ] 待办2

### 交接说明
- 下一步需要：[说明]
- 注意事项：[说明]

**工作结束时间**: YYYY-MM-DD HH:MM
**项目状态**: [正常/有问题/等待部署等]
```

---

## ⚠️ 特别注意

1. **每次接手项目，第一件事就是阅读 WORKLOG.md 的最新条目**
2. **每次完成工作，必须更新 WORKLOG.md**
3. **遇到问题必须记录，即使没解决也要写明**
4. **不要假设之前的工作者做了什么，一切以文档为准**
5. **有疑问时，查看 WORKLOG.md 的历史记录**

---

**规则版本**: v1.0
**创建时间**: 2026-02-07
**最后更新**: 2026-02-07
