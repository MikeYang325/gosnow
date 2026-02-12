# 追雪 GoSnow

日本滑雪场完全指南 - 71个雪场实时天气与降雪预报

## 项目简介

**追雪**是一个面向中国滑雪爱好者的日本雪场信息聚合网站，提供：
- 71个日本滑雪场的详细信息
- 实时天气与5天降雪预报
- 交通指南（机场直达、JR、巴士）
- 用户真实评价
- 夜场信息与雪票价格

**网站地址**: [gosnow.site](https://gosnow.site)

## 技术栈

- **前端**: 纯 HTML/CSS/JavaScript（无框架，移动端优先）
- **数据生成**: Python 脚本
- **天气数据**: Open-Meteo API
- **部署**: GitHub Pages

## 项目结构

```
gosnow/
├── index.html                    # 首页（自动生成）
├── detail_*.html                 # 71个雪场详情页（自动生成）
├── resort_details_full.json      # 雪场主数据
├── weather_data.json             # 天气数据（自动更新）
├── xiaohongshu_reviews.json      # 用户评价
├── generate_mobile_version.py    # 首页生成脚本
├── generate_detail_pages.py      # 详情页生成脚本
├── fetch_openmeteo.py            # 天气数据获取脚本
├── CLAUDE.md                     # Claude Code 开发指南
├── PLAN.md                       # 功能开发计划
└── WORKLOG.md                    # 工作日志
```

## 快速开始

### 更新天气数据
```bash
python3 fetch_openmeteo.py
```

### 重新生成页面
```bash
python3 generate_mobile_version.py   # 生成首页
python3 generate_detail_pages.py     # 生成详情页
```

### 本地预览
```bash
open index.html
```

## 地区分类

- **北海道**: 二世谷、富良野、留寿都、星野TOMAMU等
- **东北**: 藏王温泉、安比高原、雫石等
- **关东**: 草津温泉、富士山YETI、丸沼高原等
- **中部**: 志贺高原、野泽温泉、白马、苗场、GALA汤泽等
- **关西**: 箱馆山、琵琶湖Valley、六甲山等

## 开发规范

1. **不要手动编辑** `index.html` 和 `detail_*.html`，修改 Python 脚本后重新生成
2. **修改数据后**必须重新运行生成脚本
3. **每次开发**请更新 `WORKLOG.md`
4. **详细开发指南**请参考 `CLAUDE.md`

## 关于命名

本项目使用"滑雪"作为通用术语，涵盖双板滑雪（Ski）和单板滑雪（Snowboard）。我们尊重所有滑雪运动形式，不做区分对待。

## 联系方式

如有问题或建议，请通过网站底部的微信二维码联系站长。

---

**追雪** - 让每一次滑雪之旅都有好雪相伴 ❄️
