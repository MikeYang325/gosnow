# 追雪项目工作日志

## 项目概述
日本滑雪场信息聚合网站 - 28个核心雪场，实时天气，多维度排序
- **网站**: gosnow.site
- **部署**: GitHub Pages
- **天气源**: weathernews.jp API（实时数据）

---

## 当前状态 (2026-02-12)

### 已完成功能
- 28个核心雪场数据（坐标、票价、交通、特色、图片）
- 实时天气数据（weathernews.jp API，积雪深度、温度、降雪量）
- 首页：4种排序（积雪深度、当前降雪、雪道数量、雪票价格）
- 排序支持升序/降序切换（点击按钮切换，显示↑↓箭头）
- 详情页：天气图表、7天预报、交通信息、小红书评价
- 所有图片本地化（hero图和雪道图缓存到GitHub）
- GitHub Actions 自动更新天气（每小时一次）
- 统一数据源架构（resorts_unified.json）

### 核心文件
```
index.html                    # 首页（手动维护，天气自动更新）
resorts/*-new.html            # 28个详情页（手动维护，天气自动更新）
resorts_unified.json          # 统一数据源（唯一真相来源）
update_all_weather.py         # 天气更新脚本（带重试机制）
images/                       # 本地图片缓存（56张图片，77MB）
.github/workflows/            # GitHub Actions配置
  - update-weather.yml        # 每小时自动更新天气
  - static.yml                # GitHub Pages部署
```

### 数据架构
- **单一数据源**: `resorts_unified.json` 包含所有静态信息
- **天气数据**: 从weathernews.jp API实时获取
- **更新流程**:
  1. 脚本读取 resorts_unified.json
  2. 调用 weathernews.jp API 获取实时天气
  3. 更新 index.html 和 resorts/*-new.html
  4. GitHub Actions 自动提交推送

---

## 2026-02-12 最新更新

### 图片本地化
- 缓存所有雪场的 hero 图和雪道图到 `images/` 目录
- 更新所有详情页使用本地路径 `../images/`
- 解决外部图片访问不稳定问题

### 数据一致性改造
- 创建 `resorts_unified.json` 作为唯一数据源
- 从详情页提取所有信息到统一JSON
- 重写 `update_all_weather.py` 使用统一数据源
- 确保首页和详情页信息完全一致

### 首页功能增强
- 删除7天降雪预报（数据不准确）
- 添加4种排序：积雪深度、当前降雪、雪道数量、雪票价格
- 实现排序升序/降序切换（点击同一按钮切换）
- 按钮显示排序方向（↓降序 / ↑升序）
- 默认排序：当前降雪（从高到低）
- 价格排序默认从低到高，其他从高到低
- 积雪emoji从📏改为❄️

### 天气更新优化
- 添加重试机制（每个API请求最多3次）
- 超时时间从10秒增加到20秒
- 重试间隔2秒
- 成功率从26/28提升到28/28
- 修复GitHub Actions权限问题（添加 contents: write）

### 技术改进
- weathernews.jp API集成（替代之前的数据源）
- 错误处理增强（空响应、超时、JSON解析错误）
- 数据同步机制（首页和详情页同步更新）

---

## 详情页优化进度 (resorts/*-new.html)

### 已完成 (28个核心雪场)
| 雪场 | 雪道数 | 文件 | 状态 |
|------|-------|------|------|
| 志贺高原 | 84 | shiga-kogen-ski-resort-new.html | ✅ |
| 二世谷联合 | 76 | niseko-united-new.html | ✅ |
| 菅平高原 | 60 | sugadaira-kogen-ski-resort-new.html | ✅ |
| 妙高高原 | 48 | myoko-kogen-ski-resort-new.html | ✅ |
| 野泽温泉 | 44 | nozawa-onsen-ski-resort-new.html | ✅ |
| 留寿都 | 37 | rusutsu-resort-new.html | ✅ |
| 白马八方尾根 | 37 | hakuba-happo-one-ski-resort-new.html | ✅ |
| 神乐 | 31 | kagura-ski-resort-new.html | ✅ |
| 星野Tomamu | 29 | hoshino-resorts-tomamu-new.html | ✅ |
| 苗场 | 28 | naeba-ski-resort-new.html | ✅ |
| 藏王温泉 | 28 | zao-onsen-ski-resort-new.html | ✅ |
| 富良野 | 28 | furano-ski-resort-new.html | ✅ |
| 石打丸山 | 25 | ishiuchi-maruyama-ski-resort-new.html | ✅ |
| 白马栂池 | 24 | hakuba-tsugaike-ski-resort-new.html | ✅ |
| 喜乐乐 | 23 | kiroro-ski-resort-new.html | ✅ |
| 斑尾高原 | 22 | madarao-kogen-ski-resort-new.html | ✅ |
| 岩原 | 22 | iwappara-ski-resort-new.html | ✅ |
| GALA汤泽 | 21 | gala-yuzawa-ski-resort-new.html | ✅ |
| 轻井泽王子 | 21 | karuizawa-prince-ski-resort-new.html | ✅ |
| 安比高原 | 21 | appi-kogen-ski-resort-new.html | ✅ |
| 白马五竜 | 21 | hakuba-goryu-ski-resort-new.html | ✅ |
| 札幌手稻 | 21 | sapporo-teine-ski-resort-new.html | ✅ |
| 白马47 | 20 | hakuba-47-ski-resort-new.html | ✅ |
| LOTTE新井 | 18 | lotte-arai-resort-new.html | ✅ |
| 八海山 | 16 | hakkaisan-ski-resort-new.html | ✅ |
| 神居 | 15 | kamui-ski-links-new.html | ✅ |
| 旭岳 | 12 | asahidake-ski-resort-new.html | ✅ |
| 八甲田 | 野雪 | hakkoda-ski-resort-new.html | ✅ |

---

## 维护命令速查

```bash
# 更新天气数据（本地测试）
python3 update_all_weather.py

# 提取详情页数据到统一JSON
python3 extract_resort_data.py

# 部署
git add . && git commit -m "更新内容" && git push origin main

# 手动触发GitHub Actions
# 访问 https://github.com/ydx123mike/gosnow/actions
# 点击 "Update Weather Data" -> "Run workflow"
```

---

## 开发历史摘要

### 2026-02-12 下午 - 首页功能增强与天气优化
- 删除7天降雪预报（不准确）
- 添加多种排序方式（积雪、降雪、雪道、价格）
- 实现排序升序/降序切换
- 优化天气更新脚本（重试机制）
- 修复GitHub Actions自动更新
- 所有28个雪场天气数据正常

### 2026-02-12 上午 - 数据架构重构
- 创建统一数据源 resorts_unified.json
- 图片本地化（56张图片）
- 数据一致性保证（首页和详情页同步）
- weathernews.jp API集成

### 2026-02-12 早晨 - 代码清理与安全审计
- 删除 98 个实验性脚本
- 移除敏感信息（API密钥、服务器信息）
- .gitignore 优化

### 2026-02-08 - 详情页优化
- 官网链接同步
- 交通信息格式化
- 多维度评价系统

### 2026-02-07 - 项目基础
- 网站架构搭建
- 雪场数据收集
- GitHub Pages 部署

---

## 跨设备工作指南

### 在新设备上开始工作

```bash
# 1. 克隆项目
git clone https://github.com/ydx123mike/gosnow.git
cd gosnow

# 2. 拉取最新代码
git pull origin main

# 3. 查看项目文档
cat CLAUDE.md        # 项目架构和规则
cat WORKLOG.md       # 工作历史
cat resorts_unified.json  # 数据源

# 4. 在 Claude Code 中打开项目
# 访问 claude.ai/code，选择这个目录
```

### 工作流程

1. **开始工作前**: `git pull origin main`
2. **使用 Claude Code**: 打开项目目录，继续对话
3. **Claude 会自动**: 读取 CLAUDE.md 和 WORKLOG.md
4. **提交代码**: Claude 会自动 commit 和 push

---

**最后更新**: 2026-02-12 下午
