#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成所有雪场的详情页
使用统一数据源: weather_data.json (Open-Meteo)
"""

import json
import re
from datetime import datetime, timedelta

# WMO天气代码映射
WMO_CODES = {
    0: ('晴天', '☀️'),
    1: ('晴间多云', '🌤️'),
    2: ('多云', '⛅'),
    3: ('阴天', '☁️'),
    45: ('雾', '🌫️'),
    48: ('雾凇', '🌫️'),
    51: ('小毛毛雨', '🌧️'),
    53: ('毛毛雨', '🌧️'),
    55: ('大毛毛雨', '🌧️'),
    61: ('小雨', '🌧️'),
    63: ('中雨', '🌧️'),
    65: ('大雨', '🌧️'),
    66: ('冻雨', '🌧️'),
    67: ('大冻雨', '🌧️'),
    71: ('小雪', '❄️'),
    73: ('中雪', '❄️❄️'),
    75: ('大雪', '❄️❄️❄️'),
    77: ('雪粒', '❄️'),
    80: ('小阵雨', '🌧️'),
    81: ('阵雨', '🌧️'),
    82: ('大阵雨', '🌧️'),
    85: ('小阵雪', '❄️'),
    86: ('大阵雪', '❄️❄️'),
    95: ('雷暴', '⛈️'),
    96: ('雷暴+冰雹', '⛈️'),
    99: ('雷暴+大冰雹', '⛈️'),
}

def get_weather_info(code):
    return WMO_CODES.get(code, ('未知', '🌤️'))

def format_transport_info(transport, transport_detailed):
    """交通信息直接显示官网链接"""
    return ''  # 不再生成交通信息内容，由外部直接显示链接按钮

def parse_highlights(highlights):
    """从highlights字段解析海拔、雪道数量等信息"""
    result = {
        'elevation_min': None,
        'elevation_max': None,
        'elevation_drop': None,
        'trail_count': None,
        'annual_snowfall': None
    }

    if not highlights:
        return result

    # 解析海拔: 格式如 "308-1308m" 或 "落差700m"
    elevation_match = re.search(r'(\d+)-(\d+)m', highlights)
    if elevation_match:
        result['elevation_min'] = int(elevation_match.group(1))
        result['elevation_max'] = int(elevation_match.group(2))
        result['elevation_drop'] = result['elevation_max'] - result['elevation_min']

    # 解析落差: 格式如 "落差700m"
    drop_match = re.search(r'落差(\d+)m', highlights)
    if drop_match:
        result['elevation_drop'] = int(drop_match.group(1))

    # 解析雪道数量: 格式如 "76 雪道" 或 "76雪道"
    trail_match = re.search(r'(\d+)\s*雪道', highlights)
    if trail_match:
        result['trail_count'] = int(trail_match.group(1))

    # 解析年降雪量: 格式如 "粉雪量 15m+" 或 "年降雪 20m+"
    snow_match = re.search(r'(?:粉雪量|年降雪|降雪量?)\s*(\d+)m', highlights)
    if snow_match:
        result['annual_snowfall'] = f"{snow_match.group(1)}m+"

    return result

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

# 读取多维度评价数据
try:
    with open('reviews_detailed.json', 'r', encoding='utf-8') as f:
        reviews_detailed = json.load(f).get('reviews', {})
except:
    reviews_detailed = {}

# 维度名称映射
DIMENSION_NAMES = {
    'snow_quality': '❄️ 雪质',
    'crowd': '👥 人流',
    'terrain': '⛷️ 地形',
    'dining': '🍜 餐饮',
    'value': '💰 性价比',
    'transport': '🚌 交通'
}

# 只生成指定的5个雪场（测试用，正式发布时注释掉）
# TEST_RESORTS = ['富良野滑雪场', '留寿都度假村', '喜乐乐雪世界', '神立高原滑雪场', '二世谷联合雪场']
TEST_RESORTS = None  # 设为None则生成全部

resorts_to_generate = resort_data['resorts']
if TEST_RESORTS:
    resorts_to_generate = [r for r in resort_data['resorts'] if r['resort_name'] in TEST_RESORTS]
    print(f"⚠️ 测试模式：只生成 {len(resorts_to_generate)} 个雪场")
else:
    print(f"开始生成 {len(resort_data['resorts'])} 个雪场的详情页...")

for resort in resorts_to_generate:
    name = resort['resort_name']
    english = resort.get('english_name', '')
    japanese = resort.get('japanese_name', '')
    address = resort.get('address', '')
    website = resort.get('website', '')
    highlights = resort.get('highlights', '')

    # 新增字段：hero图、天气链接、摄像头、雪道图、雪票链接、官网交通页
    hero_image = resort.get('hero_image', '')
    weather_url = resort.get('weather_url', '')
    live_camera = resort.get('live_camera', '')
    trail_map = resort.get('trail_map', '')
    ticket_url = resort.get('ticket_url', '')
    transport_page = resort.get('transport_page', '')

    # 雪场简介
    intro = resort.get('intro', '')

    # 解析highlights获取基础信息
    parsed_info = parse_highlights(highlights)

    # 优先使用专门字段，否则使用解析结果
    elevation_min = resort.get('elevation_min') or parsed_info['elevation_min']
    elevation_max = resort.get('elevation_max') or parsed_info['elevation_max']
    elevation_drop = resort.get('elevation_drop') or parsed_info['elevation_drop']
    trail_count = resort.get('trail_count') or parsed_info['trail_count']
    lift_count = resort.get('lift_count')
    annual_snowfall = resort.get('annual_snowfall') or parsed_info['annual_snowfall']
    skiable_area = resort.get('skiable_area')

    # 雪道图URL（优先使用新字段trail_map，兼容旧字段trail_map_url）
    trail_map_url = resort.get('trail_map', '') or resort.get('trail_map_url', '')

    # 雪票联盟（如IKON Pass）
    pass_alliance = resort.get('pass_alliance', '')

    # 夜场是否包含在日票中
    night_included_in_day_pass = resort.get('night_included_in_day_pass', False)

    # 获取坐标用于天气链接
    coords = resort.get('coordinates', '')
    if coords:
        lon, lat = coords.split(',')
        windy_url = f"https://www.windy.com/{lat}/{lon}?{lat},{lon},10,snow"
    else:
        windy_url = "https://www.windy.com/?snow"

    # 从统一数据源获取天气
    resort_weather = weather_data.get(name, {})
    current = resort_weather.get('current', {})
    forecast = resort_weather.get('forecast', {})

    # 当前天气
    temp = current.get('temperature', 0)
    snow_24h = current.get('snow_24h', 0)
    snow_emoji = current.get('snow_emoji', '🌤️')
    weather_text = current.get('weather_text', '未知')

    # 7天预报
    forecast_7day = forecast.get('total_7day_snowfall', 0)
    daily_snowfall = forecast.get('daily_snowfall', [])
    daily_temp_min = forecast.get('daily_temp_min', [])
    daily_temp_max = forecast.get('daily_temp_max', [])
    daily_weather_code = forecast.get('daily_weather_code', [])
    daily_dates = forecast.get('daily_dates', [])

    # 生成日期和预报数据
    daily_forecast = []
    for i in range(min(len(daily_snowfall), 7)):
        # 使用API返回的日期
        if i < len(daily_dates):
            date_str = daily_dates[i]
            date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%m-%d')
        else:
            date = (datetime.now() + timedelta(days=i)).strftime('%m-%d')

        weather_code = daily_weather_code[i] if i < len(daily_weather_code) else 0
        weather_text_day, weather_icon = get_weather_info(weather_code)

        daily_forecast.append({
            'date': date,
            'snowfall': daily_snowfall[i] if i < len(daily_snowfall) else 0,
            'temp_min': daily_temp_min[i] if i < len(daily_temp_min) else 0,
            'temp_max': daily_temp_max[i] if i < len(daily_temp_max) else 0,
            'weather_code': weather_code,
            'weather_text': weather_text_day,
            'weather_icon': weather_icon
        })

    # 票价
    ticket = resort.get('ticket_prices', {})
    ticket_price = ticket.get('one_day_adult', 'N/A')

    # 交通
    transport = resort.get('transport', '')
    transport_detailed = resort.get('transport_detailed', '')

    # 小红书评价
    review = resort.get('xiaohongshu_review', '')

    # 夜滑信息
    night_skiing = resort.get('night_skiing_info', '')

    # 生成详情页HTML
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" name="viewport"/>
    <title>{name} - 追雪</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}

        .back-btn {{
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            display: inline-flex;
            align-items: center;
            gap: 5px;
            color: white;
            text-decoration: none;
            font-size: 0.9em;
            padding: 5px 10px;
            border-radius: 6px;
            transition: all 0.2s;
        }}

        .back-btn:hover {{
            background: rgba(255,255,255,0.2);
        }}

        .hero-section {{
            background: white;
            border-radius: 12px;
            padding: 0;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            overflow: hidden;
        }}

        .hero-image {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            display: block;
            border-radius: 12px;
        }}

        .header-title {{
            font-size: 1.4em;
            font-weight: 700;
            margin-bottom: 5px;
        }}

        .header-subtitle {{
            font-size: 0.85em;
            opacity: 0.9;
        }}

        .content {{
            padding: 15px;
            max-width: 600px;
            margin: 0 auto;
        }}

        .section {{
            background: white;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}

        .section-title {{
            font-size: 1em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 2px solid #667eea;
        }}

        .info-table {{
            display: flex;
            flex-direction: column;
        }}

        .info-row {{
            display: flex;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
        }}

        .info-row:last-child {{
            border-bottom: none;
        }}

        .info-label {{
            font-size: 0.8em;
            color: #999;
            width: 80px;
            flex-shrink: 0;
        }}

        .info-value {{
            font-size: 0.85em;
            font-weight: 600;
            color: #333;
            flex: 1;
        }}

        .weather-box {{
            background: linear-gradient(135deg, #42a5f5 0%, #1976d2 100%);
            color: white;
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 12px;
        }}

        .weather-current {{
            font-size: 1em;
            font-weight: 700;
            margin-bottom: 8px;
        }}

        .forecast-grid {{
            display: flex;
            gap: 4px;
            margin-top: 12px;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            padding-bottom: 4px;
        }}

        .forecast-grid::-webkit-scrollbar {{
            display: none;
        }}

        .forecast-day {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 8px 4px;
            text-align: center;
            flex: 1;
            min-width: 54px;
        }}

        .forecast-date {{
            font-size: 0.7em;
            color: #999;
            margin-bottom: 4px;
        }}

        .forecast-temp {{
            font-size: 0.75em;
            font-weight: 700;
            color: #ff6b6b;
        }}

        .forecast-snow-val {{
            font-size: 0.7em;
            font-weight: 600;
            color: #1976d2;
            margin-top: 2px;
            white-space: nowrap;
        }}

        .text-content {{
            font-size: 0.85em;
            color: #555;
            line-height: 1.6;
            white-space: pre-wrap;
        }}

        /* 交通信息样式 */
        .transport-grid {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .transport-item {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 10px 12px;
            border-left: 3px solid #667eea;
        }}

        .transport-label {{
            font-size: 0.8em;
            font-weight: 600;
            color: #667eea;
            margin-bottom: 4px;
        }}

        .transport-value {{
            font-size: 0.85em;
            color: #333;
            line-height: 1.6;
        }}

        .transport-link {{
            color: #667eea;
            text-decoration: none;
            border-bottom: 1px dashed #667eea;
        }}

        .transport-link:hover {{
            color: #764ba2;
            border-bottom-color: #764ba2;
        }}

        .transport-simple {{
            font-size: 0.85em;
            color: #555;
            line-height: 1.6;
        }}

        .transport-summary {{
            font-size: 0.9em;
            color: #333;
            line-height: 2;
        }}

        .review-box {{
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 12px;
            border-radius: 8px;
            font-size: 0.85em;
            color: #555;
            line-height: 1.6;
        }}

        .dimension-grid {{
            display: flex;
            flex-direction: column;
        }}

        .dimension-item {{
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
        }}

        .dimension-item:last-child {{
            border-bottom: none;
        }}

        .dimension-row1 {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .dimension-name {{
            font-size: 0.8em;
            font-weight: 600;
            color: #333;
            width: 65px;
            flex-shrink: 0;
            white-space: nowrap;
        }}

        .dimension-bar {{
            flex: 1;
            height: 6px;
            background: #e0e0e0;
            border-radius: 3px;
            overflow: hidden;
        }}

        .dimension-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 3px;
        }}

        .dimension-score {{
            font-size: 0.75em;
            color: #667eea;
            font-weight: 600;
            width: 30px;
            text-align: right;
            flex-shrink: 0;
        }}

        .dimension-comment {{
            font-size: 0.75em;
            color: #666;
            line-height: 1.4;
            margin-top: 4px;
            padding-left: 75px;
        }}

        .tips-list {{
            list-style: none;
            padding: 0;
        }}

        .tips-list li {{
            font-size: 0.85em;
            color: #555;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }}

        .tips-list li:last-child {{
            border-bottom: none;
        }}

        .tips-list li::before {{
            content: '💡';
            flex-shrink: 0;
        }}

        .review-summary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 12px;
            font-size: 0.9em;
            font-weight: 600;
        }}

        .btn-group {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 15px;
        }}

        .btn {{
            padding: 10px;
            background: #667eea;
            color: white;
            text-decoration: none;
            text-align: center;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9em;
            transition: all 0.2s;
        }}

        .btn:active {{
            transform: scale(0.95);
            background: #5568d3;
        }}

        .btn-secondary {{
            background: #f8f9fa;
            color: #2c3e50;
        }}

        .btn-secondary:active {{
            background: #e9ecef;
        }}

        .quick-links {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 12px;
        }}

        .quick-link {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 6px 12px;
            background: #f0f4ff;
            color: #667eea;
            text-decoration: none;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 500;
            transition: all 0.2s;
        }}

        .quick-link:hover {{
            background: #667eea;
            color: white;
        }}

        @media (min-width: 768px) {{
            .header {{
                padding: 20px 25px;
            }}

            .header-title {{
                font-size: 1.6em;
            }}

            .content {{
                padding: 25px 20px;
            }}

            .section {{
                padding: 20px;
                margin-bottom: 20px;
            }}

            .info-table {{
                max-width: 600px;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <a href="../index.html" class="back-btn">← 返回列表</a>
        <div class="header-title">{name}</div>
        <div class="header-subtitle">{english}</div>
    </div>
'''

    html += '''
    <div class="content">
'''

    # Hero图片区块 - 放在content内部作为第一个section
    if hero_image:
        html += f'''        <!-- Hero图片 -->
        <div class="hero-section">
            <img src="{hero_image}" alt="{name}" class="hero-image" onerror="this.parentElement.style.display='none'"/>
        </div>

'''

    # 雪场简介区块
    if intro:
        html += f'''        <!-- 雪场简介 -->
        <div class="section">
            <div class="section-title">📝 雪场简介</div>
            <div class="text-content">{intro}</div>
        </div>

'''

    # 基本信息区块
    html += f'''        <!-- 基本信息 -->
        <div class="section">
            <div class="section-title">📍 基本信息</div>
            <div class="info-table">
                <div class="info-row">
                    <span class="info-label">日文名称</span>
                    <span class="info-value">{japanese}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">一日券</span>
                    <span class="info-value">{ticket_price}</span>
                </div>
'''

    # 添加海拔信息
    if elevation_max and elevation_min:
        html += f'''                <div class="info-row">
                    <span class="info-label">海拔范围</span>
                    <span class="info-value">{elevation_min}m - {elevation_max}m</span>
                </div>
'''
    if elevation_drop:
        html += f'''                <div class="info-row">
                    <span class="info-label">落差</span>
                    <span class="info-value">{elevation_drop}m</span>
                </div>
'''

    # 添加雪道数量
    if trail_count:
        html += f'''                <div class="info-row">
                    <span class="info-label">雪道数量</span>
                    <span class="info-value">{trail_count}条</span>
                </div>
'''

    # 添加缆车数量
    if lift_count:
        html += f'''                <div class="info-row">
                    <span class="info-label">缆车数量</span>
                    <span class="info-value">{lift_count}条</span>
                </div>
'''

    # 添加年均降雪量
    if annual_snowfall:
        html += f'''                <div class="info-row">
                    <span class="info-label">年均降雪</span>
                    <span class="info-value">{annual_snowfall}</span>
                </div>
'''

    # 添加可滑面积
    if skiable_area:
        html += f'''                <div class="info-row">
                    <span class="info-label">可滑面积</span>
                    <span class="info-value">{skiable_area}</span>
                </div>
'''

    # 添加雪票联盟
    if pass_alliance:
        html += f'''                <div class="info-row">
                    <span class="info-label">雪票联盟</span>
                    <span class="info-value" style="color: #667eea;">{pass_alliance}</span>
                </div>
'''

    html += f'''                <div class="info-row">
                    <span class="info-label">特色</span>
                    <span class="info-value">{highlights}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">地址</span>
                    <span class="info-value">{address}</span>
                </div>
            </div>
        </div>

        <!-- 天气与降雪 -->
        <div class="section">
            <div class="section-title">🌤️ 天气与降雪</div>
            <div class="weather-box">
                <a href="{weather_url if weather_url else windy_url}" target="_blank" class="weather-current" style="text-decoration: none; color: inherit; display: block;">
                    {snow_emoji} 当前: {snow_24h:.1f}cm · {temp if temp is not None else '-'}°C · {weather_text}
                </a>
                <a href="{weather_url if weather_url else windy_url}" target="_blank" style="font-size: 0.9em; opacity: 0.9; text-decoration: none; color: inherit; display: block;">
                    🔮 未来7天预计: {forecast_7day:.1f}cm
                </a>
            </div>
'''

    # 添加未来7天预报
    if daily_forecast:
        html += '''            <div class="forecast-grid">
'''
        for i, day in enumerate(daily_forecast[:7]):
            date = day.get('date', '')
            snow_sum = day.get('snowfall', 0)
            temp_min = day.get('temp_min', 0)
            temp_max = day.get('temp_max', 0)
            weather_icon = day.get('weather_icon', '🌤️')

            if snow_sum > 0:
                snow_display = f"{snow_sum:.1f}cm"
                icon = "❄️"
            else:
                snow_display = "-"
                icon = weather_icon

            html += f'''                <div class="forecast-day">
                    <div class="forecast-date">{date}</div>
                    <div class="forecast-temp">{temp_min if temp_min is not None else '-'}°~{temp_max if temp_max is not None else '-'}°</div>
                    <div class="forecast-snow-val">{icon} {snow_display}</div>
                </div>
'''
        html += '''            </div>
'''

    # 添加快捷链接（天气官网、摄像头、雪道图、雪票购买）
    quick_links = []
    if weather_url:
        quick_links.append(f'<a href="{weather_url}" target="_blank" class="quick-link">🌤️ 官网天气</a>')
    if live_camera:
        quick_links.append(f'<a href="{live_camera}" target="_blank" class="quick-link">📹 实时摄像头</a>')
    if trail_map_url:
        quick_links.append(f'<a href="{trail_map_url}" target="_blank" class="quick-link">🗺️ 雪道图</a>')
    if ticket_url:
        quick_links.append(f'<a href="{ticket_url}" target="_blank" class="quick-link">🎫 购买雪票</a>')
    if windy_url:
        quick_links.append(f'<a href="{windy_url}" target="_blank" class="quick-link">🌬️ Windy预报</a>')

    if quick_links:
        html += f'''            <div class="quick-links">
                {''.join(quick_links)}
            </div>
'''

    html += '''        </div>
'''

    # 交通信息 - 只显示官网链接
    if transport_page:
        html += f'''        <!-- 交通信息 -->
        <div class="section">
            <div class="section-title">🚌 交通信息</div>
            <a href="{transport_page}" target="_blank" class="btn" style="display: block; text-align: center;">🔗 查看官网交通详情</a>
        </div>
'''

    # 夜场信息
    if night_skiing and night_skiing != '无':
        night_info_html = f'<div class="text-content">{night_skiing}</div>'

        # 添加是否包含在日票中的信息
        if night_included_in_day_pass:
            night_info_html += '''
            <div style="margin-top: 10px; padding: 8px 12px; background: #e8f5e9; border-radius: 6px; font-size: 0.85em; color: #2e7d32;">
                ✓ 夜场包含在日票中
            </div>'''

        html += f'''        <!-- 夜场信息 -->
        <div class="section">
            <div class="section-title">🌙 夜场信息</div>
            {night_info_html}
        </div>
'''

    # 多维度评价
    detailed_review = reviews_detailed.get(name, {})
    if detailed_review:
        summary = detailed_review.get('summary', '')
        dimensions = detailed_review.get('dimensions', {})
        tips = detailed_review.get('tips', [])

        html += '''        <!-- 多维度评价 -->
        <div class="section">
            <div class="section-title">⭐ 多维度评价</div>
'''
        if summary:
            html += f'''            <div class="review-summary">{summary}</div>
'''

        if dimensions:
            html += '''            <div class="dimension-grid">
'''
            for dim_key, dim_data in dimensions.items():
                dim_name = DIMENSION_NAMES.get(dim_key, dim_key)
                score = dim_data.get('score', 0)
                comment = dim_data.get('comment', '')
                fill_width = score * 20

                html += f'''                <div class="dimension-item">
                    <div class="dimension-row1">
                        <span class="dimension-name">{dim_name}</span>
                        <div class="dimension-bar">
                            <div class="dimension-fill" style="width: {fill_width}%;"></div>
                        </div>
                        <span class="dimension-score">{score}/5</span>
                    </div>
                    <div class="dimension-comment">{comment}</div>
                </div>
'''
            html += '''            </div>
'''

        if tips:
            html += '''            <ul class="tips-list" style="margin-top: 15px;">
'''
            for tip in tips:
                html += f'''                <li>{tip}</li>
'''
            html += '''            </ul>
'''

        html += '''        </div>
'''

    # 小红书评价（如果没有多维度评价，显示原评价）
    elif review:
        html += f'''        <!-- 游客评价 -->
        <div class="section">
            <div class="section-title">💬 游客评价</div>
            <div class="review-box">{review}</div>
        </div>
'''

    # 雪道图
    # 优先使用静态图片，没有则只显示链接按钮
    trail_map_image = resort.get('trail_map_image', '')

    if trail_map_image or trail_map_url:
        html += '''        <!-- 雪道图 -->
        <div class="section">
            <div class="section-title">🗺️ 雪道图</div>
            <div style="text-align: center;">
'''
        # 判断是否有静态图片或URL是图片格式
        is_image_url = trail_map_image or (trail_map_url and any(trail_map_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']))

        if is_image_url:
            img_src = trail_map_image if trail_map_image else trail_map_url
            link_url = trail_map_url if trail_map_url else img_src
            html += f'''                <a href="{link_url}" target="_blank">
                    <img src="{img_src}" alt="{name}雪道图" style="max-width: 100%; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"/>
                </a>
                <p style="margin-top: 8px; font-size: 0.75em; color: #999;">点击图片查看大图</p>
'''
        else:
            # 只有链接，显示按钮
            html += f'''                <a href="{trail_map_url}" target="_blank" class="btn" style="display: inline-block; margin: 10px 0;">🗺️ 查看雪道图</a>
'''
        html += '''            </div>
        </div>
'''

    # 操作按钮
    html += f'''        <!-- 操作按钮 -->
        <div class="btn-group">
            <a href="{website}" target="_blank" class="btn">🌐 访问官网</a>
            <a href="https://www.google.com/maps/search/?api=1&query={name}" target="_blank" class="btn btn-secondary">🗺️ 地图导航</a>
        </div>
    </div>
</body>
</html>
'''

    # 保存文件
    filename = f"resorts/{english.lower().replace(' ', '-').replace('/', '-')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

print(f"✅ 已生成 {len(resorts_to_generate)} 个详情页！")
