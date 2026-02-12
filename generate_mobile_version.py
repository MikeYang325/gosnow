#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成简洁移动端优先的版本
使用统一数据源: weather_data.json (Open-Meteo)
"""

import json
import re
from datetime import datetime

# 读取数据
with open('resort_details_full.json', 'r', encoding='utf-8') as f:
    resort_data = json.load(f)

# 读取统一天气数据
try:
    with open('weather_data.json', 'r', encoding='utf-8') as f:
        weather_json = json.load(f)
        weather_data = weather_json.get('resorts', {})
except:
    weather_data = {}

# 读取小红书观点
try:
    with open('xiaohongshu_reviews.json', 'r', encoding='utf-8') as f:
        xiaohongshu_reviews = json.load(f)
except:
    xiaohongshu_reviews = {}

# 按地区分组
regions_map = {
    '全部': [],
    '北海道': [],
    '东北': [],
    '关东': [],
    '中部': [],
    '关西': []
}

for resort in resort_data['resorts']:
    address = resort.get('address', '')
    # 北海道
    if '北海道' in address:
        region = '北海道'
    # 东北地区
    elif any(x in address for x in ['青森', '岩手', '秋田', '山形', '宮城', '福島', '福岛']):
        region = '东北'
    # 关东地区
    elif any(x in address for x in ['群馬', '群马', '栃木', '茨城', '埼玉', '千葉', '東京', '神奈川', '静岡', '静冈']):
        region = '关东'
    # 中部地区（长野、新潟、岐阜等）
    elif any(x in address for x in ['長野', '长野', '新潟', '岐阜', '富山', '石川', '福井', '山梨', '愛知']):
        region = '中部'
    # 关西地区
    elif any(x in address for x in ['滋賀', '滋贺', '京都', '大阪', '兵庫', '兵库', '奈良', '和歌山']):
        region = '关西'
    else:
        region = '中部'  # 默认归入中部

    # 从统一数据源获取天气
    resort_name = resort['resort_name']
    resort_weather = weather_data.get(resort_name, {})
    current = resort_weather.get('current', {})
    forecast = resort_weather.get('forecast', {})

    # 当前天气
    snow_24h = current.get('snow_24h', 0)
    temp = current.get('temperature', 0)
    snow_emoji = current.get('snow_emoji', '🌤️')
    weather_text = current.get('weather_text', '未知')

    # 7天预报
    forecast_7day = forecast.get('total_7day_snowfall', 0)

    # 保存到resort对象
    resort['snow_24h'] = snow_24h
    resort['temp'] = temp
    resort['snow_emoji'] = snow_emoji
    resort['weather_text'] = weather_text
    resort['forecast_7day'] = forecast_7day

    # 计算综合评分
    score = 50
    score += min(snow_24h * 2, 30)

    highlights = resort.get('highlights', '')
    if '雪道' in highlights:
        trails = re.search(r'(\d+)\s*雪道', highlights)
        if trails:
            score += min(int(trails.group(1)) // 5, 10)

    if 'm' in highlights:
        elevation = re.search(r'(\d+)-(\d+)m', highlights)
        if elevation:
            diff = int(elevation.group(2)) - int(elevation.group(1))
            score += min(diff // 100, 10)

    if '粉雪' in highlights or 'powder' in highlights.lower():
        score += 5

    resort['score'] = min(score, 100)
    resort['_region'] = region  # 保存区域信息

    regions_map[region].append(resort)
    regions_map['全部'].append(resort)

# 生成HTML
html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" name="viewport"/>
    <title>追雪 - 日本滑雪场完全指南</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
            background: #f5f7fa;
            color: #333;
        }

        /* 固定顶部容器 */
        .sticky-top {
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 15px 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }

        .header-title {
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .header-subtitle {
            font-size: 0.75em;
            opacity: 0.9;
        }

        /* 地区筛选 - 横向滚动 */
        .region-tabs {
            display: flex;
            gap: 8px;
            padding: 12px 15px;
            background: white;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            border-bottom: 1px solid #e0e0e0;
        }

        .region-tabs::-webkit-scrollbar {
            display: none;
        }

        .region-tab {
            flex-shrink: 0;
            padding: 8px 16px;
            background: #f5f5f5;
            border: none;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            color: #666;
            cursor: pointer;
            transition: all 0.3s;
            white-space: nowrap;
        }

        .region-tab.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        /* 排序按钮 */
        .sort-tabs {
            display: flex;
            gap: 8px;
            padding: 12px 15px;
            background: #f8f9fa;
            overflow-x: auto;
            overflow-y: hidden;
            -webkit-overflow-scrolling: touch;
            border-bottom: 1px solid #e0e0e0;
            scrollbar-width: none;
        }

        .sort-tabs::-webkit-scrollbar {
            display: none;
            height: 0;
        }

        .sort-tab {
            flex-shrink: 0;
            padding: 8px 16px;
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 18px;
            font-size: 0.85em;
            font-weight: 600;
            color: #666;
            cursor: pointer;
            transition: all 0.3s;
            white-space: nowrap;
        }

        .sort-tab.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
        }

        /* 内容区 */
        .content {
            padding: 15px;
            max-width: 900px;
            margin: 0 auto;
        }

        .cards-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
        }

        .resort-card {
            background: white;
            border-radius: 12px;
            padding: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            position: relative;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .resort-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
        }

        .resort-card:active {
            transform: translateY(-2px);
        }

        .resort-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 8px;
        }

        .resort-name {
            font-size: 1.1em;
            font-weight: 700;
            color: #2c3e50;
            flex: 1;
            padding-right: 10px;
        }

        .resort-english {
            font-size: 0.7em;
            color: #999;
            margin-top: 2px;
        }

        .score-badge {
            background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
            color: #333;
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 0.75em;
            font-weight: 700;
            white-space: nowrap;
        }

        .resort-info {
            display: flex;
            gap: 12px;
            margin-bottom: 8px;
            font-size: 0.8em;
            color: #666;
            flex-wrap: wrap;
        }

        .info-item {
            display: flex;
            flex-direction: column;
        }

        .info-label {
            font-size: 0.85em;
            color: #999;
            margin-bottom: 2px;
        }

        .info-value {
            font-weight: 600;
            color: #333;
        }

        .snow-info {
            display: flex;
            gap: 6px;
            margin-bottom: 8px;
        }

        .snow-tag {
            flex: 1;
            padding: 8px;
            border-radius: 8px;
            text-align: center;
            font-size: 0.8em;
            font-weight: 600;
        }

        .snow-current {
            background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
            color: white;
        }

        .snow-forecast {
            background: #f3e5f5;
            color: #7b1fa2;
        }

        .xiaohongshu-review {
            background: #fff3e0;
            border-left: 3px solid #ff9800;
            padding: 8px 10px;
            border-radius: 6px;
            font-size: 0.75em;
            color: #666;
            line-height: 1.5;
            margin-bottom: 8px;
        }

        .resort-actions {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
        }

        .action-btn {
            padding: 6px;
            background: #f8f9fa;
            border: none;
            border-radius: 6px;
            font-size: 0.7em;
            font-weight: 600;
            color: #2c3e50;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            text-align: center;
        }

        .action-btn:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
        }

        .action-btn:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
        }

        /* 底部联系 */
        .footer {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 15px;
            text-align: center;
            margin-top: 20px;
        }

        .footer-title {
            font-size: 1em;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .footer-text {
            font-size: 0.85em;
            opacity: 0.9;
            margin-bottom: 12px;
        }

        .show-qr-btn {
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.5);
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            cursor: pointer;
        }

        .qr-code {
            width: 150px;
            height: 150px;
            margin: 15px auto 0;
            background: white;
            padding: 10px;
            border-radius: 10px;
            display: none;
        }

        .qr-code.show {
            display: block;
            animation: fadeIn 0.3s;
        }

        .qr-code img {
            width: 100%;
            height: 100%;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }

        .hidden {
            display: none;
        }

        /* 桌面端适配 */
        @media (min-width: 768px) {
            .header {
                padding: 30px 20px 20px;
            }

            .header-title {
                font-size: 2em;
            }

            .header-subtitle {
                font-size: 0.9em;
            }

            .region-tabs {
                justify-content: center;
                padding: 15px 20px;
            }

            .region-tab {
                padding: 10px 20px;
                font-size: 1em;
            }

            .sort-tabs {
                justify-content: center;
                padding: 12px 20px;
            }

            .sort-tab {
                padding: 8px 16px;
                font-size: 0.9em;
            }

            .content {
                padding: 30px 20px;
            }

            .cards-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
            }

            .resort-card {
                padding: 15px;
            }

            .resort-name {
                font-size: 1.3em;
            }

            .resort-info {
                gap: 20px;
                font-size: 0.9em;
            }

            .snow-info {
                gap: 10px;
            }

            .snow-tag {
                padding: 12px;
                font-size: 0.9em;
            }

            .resort-actions {
                gap: 10px;
            }

            .action-btn {
                padding: 10px;
                font-size: 0.85em;
            }

            .footer {
                padding: 30px 20px;
            }
        }
    </style>
</head>
<body>
    <div class="sticky-top">
        <div class="header">
            <div class="header-title">❄️ 追雪</div>
            <div class="header-subtitle">日本滑雪场指南 · ''' + str(len(resort_data['resorts'])) + '''个雪场 · 实时天气</div>
        </div>

        <div class="region-tabs">
'''

# 添加地区标签
for region, resorts in regions_map.items():
    if resorts:
        active = 'active' if region == '全部' else ''
        html += f'        <button class="region-tab {active}" onclick="filterRegion(\'{region}\')">{region}</button>\n'

html += '''    </div>

    <div class="sort-tabs">
        <button class="sort-tab active" onclick="sortBy('snow')">❄️ 当前降雪</button>
        <button class="sort-tab" onclick="sortBy('forecast')">🔮 未来降雪</button>
    </div>
    </div>

    <div class="content">
        <div class="cards-grid" id="content">
'''

# 生成卡片 - 只遍历一次，使用data-region属性筛选
for resort in regions_map['全部']:
    name = resort['resort_name']
    english = resort.get('english_name', '')
    highlights = resort.get('highlights', '')
    score = resort['score']
    region = resort.get('_region', '中部')  # 获取雪场所属区域

    # 使用已保存的天气数据
    temp = resort.get('temp', 0)
    snow = resort.get('snow_24h', 0)
    snow_emoji = resort.get('snow_emoji', '🌤️')
    weather_text = resort.get('weather_text', '未知')

    forecast_7day = resort.get('forecast_7day', 0)

    # 获取坐标用于天气链接
    coords = resort.get('coordinates', '')
    if coords:
        lon, lat = coords.split(',')
        windy_url = f"https://www.windy.com/{lat}/{lon}?{lat},{lon},10,snow"
    else:
        windy_url = f"https://www.windy.com/?snow"

    # 提取落差和雪道信息
    # 新格式: "落差1000m" 或 "落差974m"
    drop_match = re.search(r'落差(\d+)m', highlights)
    elevation = f"落差{drop_match.group(1)}m" if drop_match else None

    # 新格式: "76雪道" 或 "84雪道"
    trails_match = re.search(r'(\d+)雪道', highlights)
    trails = trails_match.group(1) if trails_match else None

    # 提取年降雪量
    snow_annual_match = re.search(r'年降雪(\d+)m', highlights)
    snow_annual = f"{snow_annual_match.group(1)}m" if snow_annual_match else None

    # 获取票价
    ticket = resort.get('ticket_prices', {})
    ticket_price = ticket.get('one_day_adult', 'N/A')

    detail_link = f"resorts/{english.lower().replace(' ', '-').replace('/', '-')}.html"

    html += f'''
        <div class="resort-card" data-region="{region}" data-snow="{snow}" data-forecast="{forecast_7day}" onclick="window.location.href='{detail_link}'">
            <div class="resort-header">
                <div>
                    <div class="resort-name">{name}</div>
                    <div class="resort-english">{english}</div>
                </div>
            </div>

            <div class="resort-info">'''

    # 动态添加信息项
    if elevation:
        html += f'''
                <div class="info-item">
                    <span class="info-label">落差</span>
                    <span class="info-value">{elevation}</span>
                </div>'''

    if trails:
        html += f'''
                <div class="info-item">
                    <span class="info-label">雪道</span>
                    <span class="info-value">{trails}条</span>
                </div>'''

    if snow_annual:
        html += f'''
                <div class="info-item">
                    <span class="info-label">年降雪</span>
                    <span class="info-value">{snow_annual}</span>
                </div>'''

    # 总是显示票价
    html += f'''
                <div class="info-item">
                    <span class="info-label">一日券</span>
                    <span class="info-value">{ticket_price}</span>
                </div>'''

    html += f'''
            </div>

            <div class="snow-info">
                <a href="{windy_url}" target="_blank" class="snow-tag snow-current" style="text-decoration: none;" onclick="event.stopPropagation()">
                    {snow_emoji} {snow}cm · {temp}°C
                </a>
                <a href="{windy_url}" target="_blank" class="snow-tag snow-forecast" style="text-decoration: none;" onclick="event.stopPropagation()">
                    🔮 未来5天: {forecast_7day:.1f}cm
                </a>
            </div>
'''

    # 添加小红书观点
    xhs_review = xiaohongshu_reviews.get(name, '')
    if xhs_review:
        html += f'''
            <div class="xiaohongshu-review">
                💬 {xhs_review}
            </div>
'''

    html += f'''
            <div class="resort-actions">
                <a href="{detail_link}" class="action-btn" onclick="event.stopPropagation()">📄 详情</a>
                <a href="{resort.get('website', '#')}" target="_blank" class="action-btn" onclick="event.stopPropagation()">🌐 官网</a>
                <a href="{windy_url}" target="_blank" class="action-btn" onclick="event.stopPropagation()">🌤️ 天气</a>
            </div>
        </div>
'''

html += '''
    </div>
    </div>

    <div class="footer">
        <div class="footer-title">💬 联系站长</div>
        <div class="footer-text">有问题或建议？欢迎交流</div>
        <div class="qr-code" style="display: block;">
            <img src="wx.jpg" alt="微信二维码">
        </div>
    </div>

    <script>
        let currentRegion = '全部';
        let currentSort = 'default';

        function filterRegion(region) {
            currentRegion = region;

            // 更新标签状态
            document.querySelectorAll('.region-tab').forEach(tab => {
                tab.classList.remove('active');
                if (tab.textContent === region) {
                    tab.classList.add('active');
                }
            });

            // 显示/隐藏卡片
            document.querySelectorAll('.resort-card').forEach(card => {
                if (region === '全部' || card.dataset.region === region) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });

            // 重新应用当前排序
            if (currentSort !== 'default') {
                sortBy(currentSort);
            }

            // 滚动到顶部
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function sortBy(type) {
            currentSort = type;

            // 更新按钮状态
            document.querySelectorAll('.sort-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');

            const container = document.getElementById('content');
            const cards = Array.from(container.querySelectorAll('.resort-card:not(.hidden)'));

            if (type === 'default') {
                // 默认排序：按地区和原始顺序
                cards.sort((a, b) => {
                    const regionOrder = ['全部', '北海道', '长野', '新潟', '群马', '山形'];
                    const regionA = regionOrder.indexOf(a.dataset.region);
                    const regionB = regionOrder.indexOf(b.dataset.region);
                    return regionA - regionB;
                });
            } else {
                // 按数值排序
                cards.sort((a, b) => {
                    let valA, valB;
                    if (type === 'snow') {
                        valA = parseFloat(a.dataset.snow);
                        valB = parseFloat(b.dataset.snow);
                    } else if (type === 'forecast') {
                        valA = parseFloat(a.dataset.forecast);
                        valB = parseFloat(b.dataset.forecast);
                    } else if (type === 'score') {
                        valA = parseFloat(a.dataset.score);
                        valB = parseFloat(b.dataset.score);
                    }
                    return valB - valA; // 降序
                });
            }

            // 重新排列
            cards.forEach(card => container.appendChild(card));
        }
    </script>
</body>
</html>
'''

# 保存文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ 已生成 index.html")
print(f"📊 统计:")
for region, resorts in regions_map.items():
    if resorts and region != '全部':
        print(f"  {region}: {len(resorts)}个雪场")
