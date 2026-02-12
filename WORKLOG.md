# 追雪项目工作日志

## 项目概述
日本滑雪场信息聚合网站 - 71个雪场，实时天气，降雪预报，多维度评价
- **网站**: gosnow.site
- **部署**: GitHub Pages
- **天气源**: Open-Meteo API（免费，无需 key）

---

## 当前状态 (2026-02-12)

### 已完成功能
- 71个雪场数据（坐标、票价、交通、亮点、夜滑）
- 实时天气 + 7天降雪预报（Open-Meteo ECMWF）
- 首页：地区筛选（6区域）+ 排序（降雪/预报）
- 详情页：天气图表、交通信息格式化、官网链接
- 多维度评价系统（20个热门雪场，6维度评分）
- 雪道图静态图片（18个雪场）
- GitHub Actions 定时更新天气（每天 6:00/18:00）

### 核心文件
```
index.html                    # 首页（自动生成）
detail_*.html                 # 71个详情页（自动生成）
resort_details_full.json      # 雪场主数据
weather_data.json             # 天气数据
forecast_7day.json            # 预报数据
xiaohongshu_reviews.json      # 用户评价
reviews_detailed.json         # 多维度评价（20个雪场）
fetch_openmeteo_forecast.py   # 天气获取（主力）
fetch_openweather_forecast.py # 天气获取（备用，需 API key）
fetch_trail_map_images.py     # 雪道图爬取
generate_mobile_version.py    # 首页生成
generate_detail_pages.py      # 详情页生成
```

### 待办事项
- [ ] 补充更多雪场的静态雪道图图片
- [ ] 二世谷子雪场天气显示（4个子区域独立天气）
- [ ] 页面性能优化

---

## 维护命令速查

```bash
# 更新天气数据
python3 fetch_openmeteo_forecast.py

# 重新生成页面
python3 generate_mobile_version.py
python3 generate_detail_pages.py

# 部署
git add . && git commit -m "更新内容" && git push origin main
```

---

## 开发历史摘要

### 2026-02-12 - 代码清理与安全审计
- 删除 98 个实验性脚本，保留 5 个核心脚本
- 移除飞书 API 凭证（APP_ID/SECRET 硬编码）
- 移除服务器 IP、SSH 密码等敏感信息
- .gitignore 添加 .claude/ 防止泄露
- 删除过时文档、实验 HTML、旧数据文件

### 2026-02-08 - 详情页优化
- 官网链接同步（30个雪场：交通、雪票、摄像头、天气）
- 交通信息格式化（图标标识、卡片布局）
- 多维度评价系统（20个雪场，6维度）
- 雪道图静态图片爬取（18个雪场）

### 2026-02-07 - 项目基础
- 网站架构搭建（移动端优先）
- 51个雪场数据 + 天气 API 集成
- 首页筛选排序 + 详情页图表
- GitHub Pages 部署

---

**最后更新**: 2026-02-12
