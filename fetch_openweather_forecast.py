#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 OpenWeatherMap API 获取未来7天降雪预报（并发版本）
"""

import json
import requests
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')

if not API_KEY:
    print("❌ 错误: 请设置环境变量 OPENWEATHER_API_KEY")
    print("   export OPENWEATHER_API_KEY='your_api_key_here'")
    exit(1)

# 并发数限制
CONCURRENCY = 10


def parse_weather_data(weather_data):
    """解析天气数据"""
    forecast_list = weather_data.get('list', [])

    daily_snow = {}
    daily_temp = {}
    daily_weather = {}

    for item in forecast_list:
        dt = item.get('dt')
        date = datetime.fromtimestamp(dt).strftime('%Y-%m-%d')
        snow_3h = item.get('snow', {}).get('3h', 0)
        temp = item.get('main', {}).get('temp', 0)
        weather_main = item.get('weather', [{}])[0].get('main', '')

        if date not in daily_snow:
            daily_snow[date] = 0
            daily_temp[date] = []
            daily_weather[date] = []

        daily_snow[date] += snow_3h / 10
        daily_temp[date].append(temp)
        daily_weather[date].append(weather_main)

    sorted_days = sorted(daily_snow.items())
    daily_snowfall = [round(snow, 1) for date, snow in sorted_days[:7]]

    daily_temp_min = []
    daily_temp_max = []
    daily_weather_main = []
    for date, snow in sorted_days[:7]:
        temps = daily_temp.get(date, [0])
        weathers = daily_weather.get(date, ['Clear'])
        daily_temp_min.append(round(min(temps), 0) if temps else 0)
        daily_temp_max.append(round(max(temps), 0) if temps else 0)
        main_weather = max(set(weathers), key=weathers.count) if weathers else 'Clear'
        daily_weather_main.append(main_weather)

    total_snow = sum(daily_snowfall)

    return {
        'total_7day_snowfall': round(total_snow, 1),
        'daily_snowfall': daily_snowfall,
        'daily_temp_min': daily_temp_min,
        'daily_temp_max': daily_temp_max,
        'daily_weather': daily_weather_main,
        'max_day_snowfall': round(max(daily_snowfall) if daily_snowfall else 0, 1),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M')
    }


def fetch_resort(resort):
    """获取单个雪场的天气数据"""
    name = resort['resort_name']
    coords = resort.get('coordinates', '')

    if not coords or ',' not in coords:
        return name, None, "缺少坐标"

    try:
        lon, lat = coords.split(',')
        lat, lon = float(lat), float(lon)
    except:
        return name, None, "坐标格式错误"

    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'zh_cn'
    }

    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            weather_data = response.json()
            result = parse_weather_data(weather_data)
            return name, result, None
        elif response.status_code == 401:
            text = response.json()
            return name, None, f"API Key错误: {text.get('message', '')}"
        else:
            return name, None, f"HTTP {response.status_code}"
    except requests.Timeout:
        return name, None, "请求超时"
    except Exception as e:
        return name, None, str(e)


def main():
    # 读取雪场数据
    with open('resort_details_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    resorts = data['resorts']
    total = len(resorts)

    print(f"🌤️  并发获取 {total} 个雪场的天气预报（并发数: {CONCURRENCY}）...\n")

    results = {}
    success_count = 0
    fail_count = 0

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        future_to_resort = {executor.submit(fetch_resort, resort): resort for resort in resorts}

        for i, future in enumerate(as_completed(future_to_resort), 1):
            name, result, error = future.result()
            if result:
                results[name] = result
                success_count += 1
                print(f"[{i}/{total}] ✅ {name}: {result['total_7day_snowfall']:.1f}cm")
            else:
                fail_count += 1
                print(f"[{i}/{total}] ❌ {name}: {error}")

    print(f"\n{'='*60}")
    print(f"✅ 成功: {success_count} 个")
    print(f"❌ 失败: {fail_count} 个")

    if success_count > 0:
        output = {
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'forecast_days': 5,
            'source': 'OpenWeatherMap',
            'resorts': results
        }

        with open('forecast_7day.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"\n📁 已保存到 forecast_7day.json")
    else:
        print(f"\n⚠️  没有成功获取任何数据")
        print(f"💡 如果 API Key 未激活，请等待1-2小时后再运行此脚本")


if __name__ == '__main__':
    main()
