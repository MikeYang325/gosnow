#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从weathernews.jp API获取真实的天气和降雪数据，更新到HTML页面
包括：7天预报（温度、降雪量）、当前积雪深度
"""
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime, timedelta

# 读取ID映射
with open('resort_id_mapping_complete.json', 'r') as f:
    id_mapping = json.load(f)

print(f"开始获取28个雪场的真实天气数据...\n")

updated_count = 0
failed_resorts = []

for resort_key, spot_id in id_mapping.items():
    print(f"正在更新: {resort_key} (ID: {spot_id})")

    try:
        # 1. 获取积雪数据
        result = subprocess.run(
            ['curl', '-s', f'https://site.weathernews.jp/site/ski/json/spotobs/{spot_id}.json'],
            capture_output=True, text=True, timeout=10
        )
        obs_data = json.loads(result.stdout)
        snow_depth = obs_data.get('snow_depth', '0')

        # 2. 获取天气预报数据
        result = subprocess.run(
            ['curl', '-s', f'https://site.weathernews.jp/site/ski/json/fcst_v1/fcst{spot_id}.json'],
            capture_output=True, text=True, timeout=10
        )
        fcst_data = json.loads(result.stdout)

        if 'srf' not in fcst_data or len(fcst_data['srf']) < 7:
            print(f"  ⚠️  天气预报数据不足")
            failed_resorts.append(resort_key)
            continue

        # 3. 提取7天预报数据
        forecasts = []
        for i in range(7):
            if i < len(fcst_data['srf']):
                day_data = fcst_data['srf'][i]
                forecasts.append({
                    'temp': day_data.get('AIRTMP', 0),
                    'snow': day_data.get('SNOW', 0),
                })
            else:
                forecasts.append({'temp': 0, 'snow': 0})

        # 4. 更新HTML文件
        html_file = Path(f'resorts/{resort_key}-new.html')
        if not html_file.exists():
            print(f"  ⚠️  HTML文件不存在")
            failed_resorts.append(resort_key)
            continue

        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 更新当前天气
        html_content = re.sub(
            r'<div class="weather-sub">.*?</div>',
            f'<div class="weather-sub">积雪 {snow_depth}cm · {forecasts[0]["temp"]}°C</div>',
            html_content,
            count=1
        )

        # 更新7天预报
        day_labels = ['今天', '明天', '后天', '第4天', '第5天', '第6天', '第7天']
        for i, (label, forecast) in enumerate(zip(day_labels, forecasts)):
            # 更新温度
            pattern = rf'(<div class="forecast-date">{label}</div>\s*<div class="forecast-temp">)([^<]+)(</div>)'
            html_content = re.sub(
                pattern,
                rf'\g<1>{forecast["temp"]}°C\g<3>',
                html_content
            )

            # 更新降雪
            pattern = rf'(<div class="forecast-date">{label}</div>.*?<div class="forecast-snow">)([^<]+)(</div>)'
            html_content = re.sub(
                pattern,
                rf'\g<1>{forecast["snow"]}cm\g<3>',
                html_content,
                flags=re.DOTALL
            )

        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"  ✅ 积雪: {snow_depth}cm, 今日: {forecasts[0]['temp']}°C / {forecasts[0]['snow']}cm")
        updated_count += 1

    except Exception as e:
        print(f"  ❌ 更新失败: {e}")
        failed_resorts.append(resort_key)

print(f"\n{'='*60}")
print(f"✅ 成功更新: {updated_count}/28 个雪场")
if failed_resorts:
    print(f"❌ 失败的雪场: {', '.join(failed_resorts)}")

print(f"\n数据来源: weathernews.jp")
print(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
