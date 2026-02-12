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

## 详情页优化进度 (resorts/*-new.html)

### 排名规则
- 优先按雪道数量排名，取前30个
- 手动补充4个特色雪场：八海山、神居、旭岳、八甲田
- 共34个雪场

### 优化流程
1. Claude 验证官网4个链接可访问（官网、购票、摄像头、缆车运行）
2. Claude 发送验证后的链接给用户确认
3. 用户提供 hero 图和雪道图
4. Claude 按统一模板生成新版详情页（避免乱码）
5. Claude 发送页面链接给用户审核
6. 审核通过后更新工作记录

### 已完成 (20个)
| 排名 | 雪场 | 雪道数 | 文件 |
|-----|------|-------|------|
| 1 | 志贺高原 | 84 | shiga-kogen-ski-resort-new.html |
| 2 | 二世谷联合 | 76 | niseko-united-new.html |
| 3 | 妙高高原 | 48 | myoko-kogen-ski-resort-new.html |
| 4 | 野泽温泉 | 44 | nozawa-onsen-ski-resort-new.html |
| 5 | 留寿都 | 37 | rusutsu-resort-new.html |
| 6 | 白马八方尾根 | 37 | hakuba-happo-one-ski-resort-new.html |
| 7 | 神乐 | 31 | kagura-ski-resort-new.html |
| 8 | 星野Tomamu | 29 | hoshino-resorts-tomamu-new.html |
| 9 | 苗场 | 28 | naeba-ski-resort-new.html |
| 10 | 藏王温泉 | 28 | zao-onsen-ski-resort-new.html |
| 11 | 石打丸山 | 25 | ishiuchi-maruyama-ski-resort-new.html |
| 12 | 白马栂池 | 24 | hakuba-tsugaike-ski-resort-new.html |
| 13 | 喜乐乐 | 23 | kiroro-ski-resort-new.html |
| 14 | 斑尾高原 | 22 | madarao-kogen-ski-resort-new.html |
| 15 | 岩原 | 22 | iwappara-ski-resort-new.html |
| 16 | GALA汤泽 | 21 | gala-yuzawa-ski-resort-new.html |
| 18 | 轻井泽王子 | 21 | karuizawa-prince-ski-resort-new.html |
| 19 | 安比高原 | 21 | appi-kogen-ski-resort-new.html |
| 20 | 白马五竜 | 21 | hakuba-goryu-ski-resort-new.html |
| 24 | 富良野 | 18 | furano-ski-resort-new.html |

### 待优化 (14个)
| 排名 | 雪场 | 雪道数 |
|-----|------|-------|
| 17 | 札幌手稀 | 21 |
| 21 | 白马47 | 20 |
| 22 | 二世谷比罗夫 | 20 |
| 23 | 佐幌 | 20 |
| 25 | 草津温泉 | 18 |
| 26 | 札幌国际 | 18 |
| 27 | 二世谷村 | 18 |
| 28 | 汤泽高原 | 18 |
| 29 | 猪苗代 | 18 |
| 30 | 乐天新井 | 18 |
| 31 | 八海山 | 16 |
| 32 | 神居 | 15 |
| 33 | 旭岳 | 12 |
| 34 | 八甲田 | 野雪 |

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
