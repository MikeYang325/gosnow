#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同时更新index.html和详情页的天气数据
使用 resorts_unified.json 作为唯一数据源，确保信息一致
"""
import json
import subprocess
import re
from pathlib import Path

# 读取统一的雪场数据
with open('resorts_unified.json', 'r') as f:
    unified_data = json.load(f)

# 创建映射
resorts_map = {r['resort_key']: r for r in unified_data['resorts']}
resorts_by_name = {r['resort_name']: r for r in unified_data['resorts']}

print(f"开始更新首页和详情页的天气数据...\n")

# 存储所有雪场的天气数据
weather_data = {}

# 1. 获取所有雪场的天气数据
for resort_key, resort_info in resorts_map.items():
    spot_id = resort_info.get('weathernews_id')
    if not spot_id:
        continue

    try:
        # 获取积雪数据（增加重试机制）
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = subprocess.run(
                    ['curl', '-s', f'https://site.weathernews.jp/site/ski/json/spotobs/{spot_id}.json'],
                    capture_output=True, text=True, timeout=20
                )
                if result.stdout.strip():
                    obs_data = json.loads(result.stdout)
                    break
            except (json.JSONDecodeError, subprocess.TimeoutExpired):
                if attempt == max_retries - 1:
                    raise
                import time
                time.sleep(2)

        snow_depth = obs_data.get('snow_depth', '0')

        # 获取天气预报数据（增加重试机制）
        for attempt in range(max_retries):
            try:
                result = subprocess.run(
                    ['curl', '-s', f'https://site.weathernews.jp/site/ski/json/fcst_v1/fcst{spot_id}.json'],
                    capture_output=True, text=True, timeout=20
                )
                if result.stdout.strip():
                    fcst_data = json.loads(result.stdout)
                    break
            except (json.JSONDecodeError, subprocess.TimeoutExpired):
                if attempt == max_retries - 1:
                    raise
                import time
                time.sleep(2)

        if 'srf' in fcst_data and len(fcst_data['srf']) >= 7:
            # 提取7天预报
            forecasts = []
            total_7day_snow = 0
            for i in range(7):
                day_data = fcst_data['srf'][i]
                temp = day_data.get('AIRTMP', 0)
                snow = day_data.get('SNOW', 0)
                forecasts.append({'temp': temp, 'snow': snow})
                total_7day_snow += snow

            weather_data[resort_key] = {
                'snow_depth': snow_depth,
                'current_temp': forecasts[0]['temp'],
                'current_snow': forecasts[0]['snow'],
                'total_7day_snow': round(total_7day_snow, 1),
                'forecasts': forecasts
            }

            print(f"✅ {resort_info['resort_name']}: {snow_depth}cm, {forecasts[0]['temp']}°C")

    except Exception as e:
        print(f"❌ {resort_key}: {e}")

# 2. 更新详情页
print(f"\n更新详情页...")
for resort_key, data in weather_data.items():
    html_file = Path(f'resorts/{resort_key}-new.html')
    if not html_file.exists():
        continue

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 更新当前天气
    html_content = re.sub(
        r'<div class="weather-sub">.*?</div>',
        f'<div class="weather-sub">积雪 {data["snow_depth"]}cm · {data["current_temp"]}°C</div>',
        html_content,
        count=1
    )

    # 更新7天预报
    day_labels = ['今天', '明天', '后天', '第4天', '第5天', '第6天', '第7天']
    for i, (label, forecast) in enumerate(zip(day_labels, data['forecasts'])):
        # 更新温度
        pattern = rf'(<div class="forecast-date">{label}</div>\s*<div class="forecast-temp">)([^<]+)(</div>)'
        html_content = re.sub(pattern, rf'\g<1>{forecast["temp"]}°C\g<3>', html_content)

        # 更新降雪
        pattern = rf'(<div class="forecast-date">{label}</div>.*?<div class="forecast-snow">)([^<]+)(</div>)'
        html_content = re.sub(pattern, rf'\g<1>{forecast["snow"]}cm\g<3>', html_content, flags=re.DOTALL)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

# 3. 更新首页index.html
print(f"\n更新首页...")
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

for resort_key, data in weather_data.items():
    resort_info = resorts_map[resort_key]
    resort_name = resort_info['resort_name']

    # 更新snow-badge（当前天气）
    pattern = rf'(<span class="resort-name">{re.escape(resort_name)}</span>.*?<a[^>]*class="snow-badge"[^>]*>)🌤️ [^<]+(</a>)'
    replacement = rf'\g<1>🌤️ {data["current_snow"]}cm · {data["current_temp"]}°C\g<2>'
    index_content = re.sub(pattern, replacement, index_content, flags=re.DOTALL)

    # 更新7天预报标签
    pattern = rf'(<span class="resort-name">{re.escape(resort_name)}</span>.*?<span class="info-tag forecast-tag">)🔮 7天[^<]+(</span>)'
    replacement = rf'\g<1>🔮 7天{data["total_7day_snow"]}cm\g<2>'
    index_content = re.sub(pattern, replacement, index_content, flags=re.DOTALL)

    # 更新积雪深度标签
    pattern = rf'(<span class="resort-name">{re.escape(resort_name)}</span>.*?<span class="info-tag depth-tag">)❄️ 积雪[^<]+(</span>)'
    replacement = rf'\g<1>❄️ 积雪{data["snow_depth"]}cm\g<2>'
    index_content = re.sub(pattern, replacement, index_content, flags=re.DOTALL)

    # 更新雪道数量和价格（从统一数据源）
    if 'trails' in resort_info:
        pattern = rf'(<span class="resort-name">{re.escape(resort_name)}</span>.*?<span class="info-tag">)\d+条雪道(</span>)'
        replacement = rf'\g<1>{resort_info["trails"]}条雪道\g<2>'
        index_content = re.sub(pattern, replacement, index_content, flags=re.DOTALL)

    if 'ticket_price' in resort_info:
        pattern = rf'(<span class="resort-name">{re.escape(resort_name)}</span>.*?<span class="info-tag">)[¥￥][0-9,]+(</span>)'
        replacement = rf'\g<1>{resort_info["ticket_price"]}\g<2>'
        index_content = re.sub(pattern, replacement, index_content, flags=re.DOTALL)

    # 更新data-snow、data-forecast和data-depth属性
    pattern = rf'(<div class="resort-card" data-region="[^"]*" data-snow=")[^"]*(" data-forecast=")[^"]*"( onclick="window\.location\.href=\'resorts/{re.escape(resort_key)}-new\.html\'">)'
    replacement = rf'\g<1>{data["current_snow"]}\g<2>{data["total_7day_snow"]}" data-depth="{data["snow_depth"]}"\g<3>'
    index_content = re.sub(pattern, replacement, index_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f"\n{'='*60}")
print(f"✅ 成功更新: {len(weather_data)}/28 个雪场")
print(f"✅ 首页和详情页数据已同步")
print(f"✅ 所有信息来自统一数据源 resorts_unified.json")
