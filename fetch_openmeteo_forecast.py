#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 Open-Meteo API 获取未来7天降雪预报
Open-Meteo 是免费的天气 API，无需 API key
数据来源包括 ECMWF、GFS 等多个气象模型
"""

import json
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 并发数限制（Open-Meteo 免费版有速率限制）
CONCURRENCY = 3
MAX_RETRIES = 3

# WMO 天气代码映射
WMO_CODES = {
    0: ("晴天", "☀️"),
    1: ("晴间多云", "🌤️"),
    2: ("多云", "⛅"),
    3: ("阴天", "☁️"),
    45: ("雾", "🌫️"),
    48: ("雾凇", "🌫️"),
    51: ("小毛毛雨", "🌧️"),
    53: ("毛毛雨", "🌧️"),
    55: ("大毛毛雨", "🌧️"),
    56: ("冻毛毛雨", "🌧️"),
    57: ("冻毛毛雨", "🌧️"),
    61: ("小雨", "🌧️"),
    63: ("中雨", "🌧️"),
    65: ("大雨", "🌧️"),
    66: ("冻雨", "🌧️"),
    67: ("冻雨", "🌧️"),
    71: ("小雪", "🌨️"),
    73: ("中雪", "❄️"),
    75: ("大雪", "❄️❄️"),
    77: ("雪粒", "🌨️"),
    80: ("阵雨", "🌧️"),
    81: ("阵雨", "🌧️"),
    82: ("暴雨", "🌧️"),
    85: ("阵雪", "🌨️"),
    86: ("大阵雪", "❄️❄️"),
    95: ("雷暴", "⛈️"),
    96: ("雷暴冰雹", "⛈️"),
    99: ("雷暴大冰雹", "⛈️"),
}


def get_weather_text(code):
    """根据 WMO 代码获取天气描述"""
    return WMO_CODES.get(code, ("未知", "❓"))


def fetch_resort_weather(resort):
    """获取单个雪场的天气数据（带重试）"""
    name = resort['resort_name']
    coords = resort.get('coordinates', '')

    if not coords or ',' not in coords:
        return name, None, "缺少坐标"

    try:
        lon, lat = coords.split(',')
        lat, lon = float(lat), float(lon)
    except:
        return name, None, "坐标格式错误"

    # Open-Meteo API 请求
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'snowfall,snow_depth,temperature_2m,weathercode',
        'daily': 'snowfall_sum,temperature_2m_min,temperature_2m_max,weathercode',
        'timezone': 'Asia/Tokyo',
        'forecast_days': 7
    }

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            time.sleep(0.5)  # 请求间隔
            response = requests.get(url, params=params, timeout=20)
            if response.status_code == 200:
                data = response.json()
                result = parse_open_meteo_data(data)
                return name, result, None
            else:
                last_error = f"HTTP {response.status_code}"
        except requests.Timeout:
            last_error = "请求超时"
        except Exception as e:
            last_error = str(e)[:50]

        if attempt < MAX_RETRIES - 1:
            time.sleep(1)  # 重试前等待

    return name, None, last_error


def parse_open_meteo_data(data):
    """解析 Open-Meteo 返回的数据"""
    daily = data.get('daily', {})
    hourly = data.get('hourly', {})

    # 每日数据
    daily_snowfall = daily.get('snowfall_sum', [])
    daily_temp_min = daily.get('temperature_2m_min', [])
    daily_temp_max = daily.get('temperature_2m_max', [])
    daily_weather_codes = daily.get('weathercode', [])
    daily_dates = daily.get('time', [])

    # 计算总降雪量
    total_snow = sum(s for s in daily_snowfall if s is not None)

    # 获取当前天气（使用第一个小时的数据）
    current_temp = hourly.get('temperature_2m', [None])[0]
    current_weather_code = hourly.get('weathercode', [0])[0] or 0
    current_snow_depth = hourly.get('snow_depth', [0])[0] or 0

    # 计算24小时降雪（前24个小时的累计）
    hourly_snow = hourly.get('snowfall', [])
    snow_24h = sum(s for s in hourly_snow[:24] if s is not None)

    # 天气描述
    weather_text, snow_emoji = get_weather_text(current_weather_code)

    # 根据降雪量调整 emoji
    if snow_24h >= 20:
        snow_emoji = "❄️❄️❄️"
    elif snow_24h >= 10:
        snow_emoji = "❄️❄️"
    elif snow_24h >= 5:
        snow_emoji = "❄️"
    elif snow_24h > 0:
        snow_emoji = "🌨️"

    return {
        'current': {
            'temperature': round(current_temp, 1) if current_temp else None,
            'snow_24h': round(snow_24h, 1),
            'snow_depth': round(current_snow_depth * 100, 0),  # 转换为 cm
            'weather_code': current_weather_code,
            'weather_text': weather_text,
            'snow_emoji': snow_emoji
        },
        'forecast': {
            'total_7day_snowfall': round(total_snow, 1),
            'daily_snowfall': [round(s, 1) if s else 0 for s in daily_snowfall],
            'daily_temp_min': [round(t, 0) if t else None for t in daily_temp_min],
            'daily_temp_max': [round(t, 0) if t else None for t in daily_temp_max],
            'daily_weather_code': daily_weather_codes,
            'daily_dates': daily_dates,
            'max_day_snowfall': round(max(s for s in daily_snowfall if s) if any(daily_snowfall) else 0, 1)
        },
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M')
    }


def main():
    print("=" * 60)
    print("🌨️  Open-Meteo 天气数据获取工具")
    print("=" * 60)
    print()

    # 读取雪场数据
    with open('resort_details_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    resorts = data['resorts']
    total = len(resorts)

    print(f"📊 开始获取 {total} 个雪场的天气预报...\n")

    results = {}
    success_count = 0
    fail_count = 0

    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        future_to_resort = {executor.submit(fetch_resort_weather, resort): resort for resort in resorts}

        for i, future in enumerate(as_completed(future_to_resort), 1):
            name, result, error = future.result()
            if result:
                results[name] = result
                success_count += 1
                forecast = result['forecast']
                current = result['current']
                print(f"[{i}/{total}] ✅ {name}: "
                      f"7天{forecast['total_7day_snowfall']:.1f}cm, "
                      f"24h{current['snow_24h']:.1f}cm, "
                      f"{current['temperature']}°C {current['snow_emoji']}")
            else:
                fail_count += 1
                print(f"[{i}/{total}] ❌ {name}: {error}")

            # 避免请求过快
            time.sleep(0.2)

    print(f"\n{'='*60}")
    print(f"✅ 成功: {success_count} 个")
    print(f"❌ 失败: {fail_count} 个")

    if success_count > 0:
        # 保存完整数据
        output = {
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'forecast_days': 7,
            'source': 'Open-Meteo (ECMWF)',
            'resorts': results
        }

        with open('weather_data.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"\n📁 完整数据已保存到 weather_data.json")

        # 同时更新 forecast_7day.json（兼容旧格式）
        forecast_output = {
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'forecast_days': 7,
            'source': 'Open-Meteo',
            'resorts': {}
        }

        for name, data in results.items():
            forecast_output['resorts'][name] = {
                'total_7day_snowfall': data['forecast']['total_7day_snowfall'],
                'daily_snowfall': data['forecast']['daily_snowfall'],
                'daily_temperature': data['forecast']['daily_temp_min'],
                'max_day_snowfall': data['forecast']['max_day_snowfall']
            }

        with open('forecast_7day.json', 'w', encoding='utf-8') as f:
            json.dump(forecast_output, f, ensure_ascii=False, indent=2)

        print(f"📁 预报数据已保存到 forecast_7day.json")

        # 显示降雪最多的雪场
        print(f"\n🏔️  未来7天降雪最多的雪场:")
        sorted_resorts = sorted(results.items(),
                               key=lambda x: x[1]['forecast']['total_7day_snowfall'],
                               reverse=True)
        for i, (name, data) in enumerate(sorted_resorts[:10], 1):
            snow = data['forecast']['total_7day_snowfall']
            print(f"   {i}. {name}: {snow:.1f}cm")

    else:
        print(f"\n⚠️  没有成功获取任何数据")


if __name__ == '__main__':
    main()
