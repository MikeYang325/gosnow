#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新28个雪场的天气和积雪数据
从weathernews.jp API获取实时数据并更新HTML文件
"""
import json
import subprocess
import re
from pathlib import Path

# 读取ID映射
with open('resort_id_mapping_complete.json', 'r') as f:
    id_mapping = json.load(f)

print(f"开始更新28个雪场的天气数据...\n")

updated_count = 0
failed_resorts = []

for resort_key, spot_id in id_mapping.items():
    print(f"正在更新: {resort_key} (ID: {spot_id})")

    # 获取积雪数据
    try:
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

        # 提取今天的天气
        if 'srf' in fcst_data and len(fcst_data['srf']) > 0:
            today = fcst_data['srf'][0]
            temp = today.get('AIRTMP', 0)
            snow = today.get('SNOW', 0)

            print(f"  ✅ 积雪: {snow_depth}cm, 温度: {temp}°C, 降雪: {snow}cm")

            # 更新HTML文件
            html_file = Path(f'resorts/{resort_key}-new.html')
            if html_file.exists():
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()

                # 更新当前天气文本
                html_content = re.sub(
                    r'<div class="weather-sub">数据更新中</div>',
                    f'<div class="weather-sub">积雪 {snow_depth}cm · {temp}°C</div>',
                    html_content
                )

                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                updated_count += 1
            else:
                print(f"  ⚠️  HTML文件不存在")
                failed_resorts.append(resort_key)
        else:
            print(f"  ⚠️  无天气预报数据")
            failed_resorts.append(resort_key)

    except Exception as e:
        print(f"  ❌ 更新失败: {e}")
        failed_resorts.append(resort_key)

print(f"\n{'='*60}")
print(f"✅ 成功更新: {updated_count}/28 个雪场")
if failed_resorts:
    print(f"❌ 失败的雪场: {', '.join(failed_resorts)}")
