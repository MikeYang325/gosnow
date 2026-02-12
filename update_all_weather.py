#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同时更新index.html和详情页的天气数据
"""
import json
import subprocess
import re
from pathlib import Path

# 读取ID映射
with open('resort_id_mapping_complete.json', 'r') as f:
    id_mapping = json.load(f)

# 雪场英文名到中文名的映射
resort_names = {
    'niseko-united': '二世谷联合雪场',
    'furano-ski-resort': '富良野滑雪场',
    'rusutsu-resort': '留寿都度假村',
    'hoshino-resorts-tomamu': '星野 TOMAMU 度假村',
    'kiroro-ski-resort': '喜乐乐雪世界',
    'shiga-kogen-ski-resort': '志贺高原',
    'nozawa-onsen-ski-resort': '野泽温泉',
    'naeba-ski-resort': '苗场',
    'gala-yuzawa-ski-resort': 'GALA 汤泽',
    'kagura-ski-resort': '神乐',
    'myoko-kogen-ski-resort': '妙高高原',
    'zao-onsen-ski-resort': '藏王温泉',
    'hakuba-happo-one-ski-resort': '白马八方尾根',
    'hakuba-goryu-ski-resort': '白马五竜',
    'hakuba-47-ski-resort': '白马 47 滑雪场',
    'hakuba-tsugaike-ski-resort': '白马栂池高原',
    'sapporo-teine-ski-resort': '札幌手稻滑雪场',
    'kamui-ski-links': '神居滑雪场',
    'asahidake-ski-resort': '旭岳滑雪场',
    'madarao-kogen-ski-resort': '斑尾高原滑雪场',
    'karuizawa-prince-ski-resort': '轻井泽王子滑雪场',
    'sugadaira-kogen-ski-resort': '菅平高原滑雪场',
    'ishiuchi-maruyama-ski-resort': '石打丸山滑雪场',
    'iwappara-ski-resort': '岩原滑雪场',
    'lotte-arai-resort': 'LOTTE乐天新井度假村',
    'hakkaisan-ski-resort': '八海山滑雪场',
    'hakkoda-ski-resort': '八甲田滑雪场',
    'appi-kogen-ski-resort': '安比高原滑雪场',
}

print(f"开始更新首页和详情页的天气数据...\n")

# 存储所有雪场的天气数据
weather_data = {}

# 1. 获取所有雪场的天气数据
for resort_key, spot_id in id_mapping.items():
    try:
        # 获取积雪数据
        result = subprocess.run(
            ['curl', '-s', f'https://site.weathernews.jp/site/ski/json/spotobs/{spot_id}.json'],
            capture_output=True, text=True, timeout=10
        )
        obs_data = json.loads(result.stdout)
        snow_depth = obs_data.get('snow_depth', '0')

        # 获取天气预报数据
        result = subprocess.run(
            ['curl', '-s', f'https://site.weathernews.jp/site/ski/json/fcst_v1/fcst{spot_id}.json'],
            capture_output=True, text=True, timeout=10
        )
        fcst_data = json.loads(result.stdout)

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

            print(f"✅ {resort_names.get(resort_key, resort_key)}: {snow_depth}cm, {forecasts[0]['temp']}°C")

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
    resort_name = resort_names.get(resort_key, '')
    if not resort_name:
        continue

    # 更新snow-badge（当前天气）
    pattern = rf'(<span class="resort-name">{re.escape(resort_name)}</span>.*?<a[^>]*class="snow-badge"[^>]*>)🌤️ [^<]+(</a>)'
    replacement = rf'\g<1>🌤️ {data["current_snow"]}cm · {data["current_temp"]}°C\g<2>'
    index_content = re.sub(pattern, replacement, index_content, flags=re.DOTALL)

    # 更新7天预报标签
    pattern = rf'(<span class="resort-name">{re.escape(resort_name)}</span>.*?<span class="info-tag forecast-tag">)🔮 7天[^<]+(</span>)'
    replacement = rf'\g<1>🔮 7天{data["total_7day_snow"]}cm\g<2>'
    index_content = re.sub(pattern, replacement, index_content, flags=re.DOTALL)

    # 更新data-snow和data-forecast属性
    pattern = rf'(<div class="resort-card"[^>]*onclick="[^"]*{re.escape(resort_key)}-new\.html"[^>]*data-snow=")[^"]*(" data-forecast=")[^"]*(")'
    replacement = rf'\g<1>{data["current_snow"]}\g<2>{data["total_7day_snow"]}\g<3>'
    index_content = re.sub(pattern, replacement, index_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f"\n{'='*60}")
print(f"✅ 成功更新: {len(weather_data)}/28 个雪场")
print(f"✅ 首页和详情页数据已同步")
