#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一数据管理系统
从详情页提取所有信息，更新到 resort_details_full.json
确保所有信息都有唯一的数据源
"""
import json
import re
from pathlib import Path
from datetime import datetime

# 读取现有的 resort_details_full.json
with open('resort_details_full.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 读取 weathernews ID 映射
with open('resort_id_mapping_complete.json', 'r', encoding='utf-8') as f:
    id_mapping = json.load(f)

# 雪场英文名到中文名的映射
resort_key_to_name = {
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

# 区域映射
region_map = {
    'niseko-united': '北海道',
    'furano-ski-resort': '北海道',
    'rusutsu-resort': '北海道',
    'hoshino-resorts-tomamu': '北海道',
    'kiroro-ski-resort': '北海道',
    'sapporo-teine-ski-resort': '北海道',
    'kamui-ski-links': '北海道',
    'asahidake-ski-resort': '北海道',
    'shiga-kogen-ski-resort': '中部',
    'nozawa-onsen-ski-resort': '中部',
    'naeba-ski-resort': '中部',
    'gala-yuzawa-ski-resort': '中部',
    'kagura-ski-resort': '中部',
    'myoko-kogen-ski-resort': '中部',
    'hakuba-happo-one-ski-resort': '中部',
    'hakuba-goryu-ski-resort': '中部',
    'hakuba-47-ski-resort': '中部',
    'hakuba-tsugaike-ski-resort': '中部',
    'madarao-kogen-ski-resort': '中部',
    'karuizawa-prince-ski-resort': '中部',
    'sugadaira-kogen-ski-resort': '中部',
    'ishiuchi-maruyama-ski-resort': '中部',
    'iwappara-ski-resort': '中部',
    'lotte-arai-resort': '中部',
    'hakkaisan-ski-resort': '中部',
    'zao-onsen-ski-resort': '东北',
    'hakkoda-ski-resort': '东北',
    'appi-kogen-ski-resort': '东北',
}

print("从详情页提取信息并更新 resort_details_full.json...\n")

# 创建新的雪场列表
updated_resorts = []
updated_count = 0

for resort_key, resort_name in resort_key_to_name.items():
    detail_file = Path(f'resorts/{resort_key}-new.html')
    if not detail_file.exists():
        print(f"⚠️  {resort_name}: 详情页不存在")
        continue

    # 读取详情页
    with open(detail_file, 'r', encoding='utf-8') as f:
        detail_content = f.read()

    # 提取所有信息
    resort_info = {
        'resort_key': resort_key,
        'resort_name': resort_name,
        'region': region_map.get(resort_key, ''),
        'weathernews_id': id_mapping.get(resort_key, ''),
    }

    # 提取官网
    website_match = re.search(r'<span class="info-label">官网</span>\s*<span class="info-value">.*?href="([^"]+)"', detail_content)
    if website_match:
        resort_info['website'] = website_match.group(1)

    # 提取一日券价格
    price_match = re.search(r'<span class="info-label">一日券</span>\s*<span class="info-value">(?:<span>)?([¥￥][0-9,]+)', detail_content)
    if price_match:
        resort_info['ticket_price'] = price_match.group(1)

    # 提取海拔落差
    elevation_match = re.search(r'<span class="info-label">海拔落差</span>\s*<span class="info-value">([^<]+)</span>', detail_content)
    if elevation_match:
        resort_info['elevation'] = elevation_match.group(1).strip()

    # 提取雪道数量
    trails_match = re.search(r'<span class="info-label">雪道数量</span>\s*<span class="info-value">(?:<span>)?(\d+)条', detail_content)
    if trails_match:
        resort_info['trails'] = int(trails_match.group(1))

    # 提取年均降雪
    snow_match = re.search(r'<span class="info-label">年均降雪</span>\s*<span class="info-value">([^<]+)</span>', detail_content)
    if snow_match:
        resort_info['annual_snowfall'] = snow_match.group(1).strip()

    # 提取雪场特色
    feature_match = re.search(r'<span class="info-label">雪场特色</span>\s*<span class="info-value">([^<]+)</span>', detail_content)
    if feature_match:
        resort_info['features'] = feature_match.group(1).strip()

    # 提取地址
    address_match = re.search(r'<span class="info-label">地址</span>\s*<span class="info-value">([^<]+)</span>', detail_content)
    if address_match:
        resort_info['address'] = address_match.group(1).strip()

    # 提取小红书评价
    review_match = re.search(r'<div class="review-box">\s*([^<]+)\s*</div>', detail_content)
    if review_match:
        resort_info['xiaohongshu_review'] = review_match.group(1).strip()

    # 提取图片路径
    hero_match = re.search(r'<img class="hero-image" src="([^"]+)"', detail_content)
    if hero_match:
        resort_info['hero_image'] = hero_match.group(1)

    trail_map_match = re.search(r'<img class="trail-map-img" src="([^"]+)"', detail_content)
    if trail_map_match:
        resort_info['trail_map_image'] = trail_map_match.group(1)

    updated_resorts.append(resort_info)
    print(f"✅ {resort_name}: {resort_info.get('trails', '?')}条雪道, {resort_info.get('ticket_price', '?')}")
    updated_count += 1

# 保存为新的 JSON 文件
output_data = {
    'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_resorts': len(updated_resorts),
    'resorts': updated_resorts
}

with open('resorts_unified.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"✅ 成功提取: {updated_count} 个雪场")
print(f"✅ 保存到: resorts_unified.json")
print(f"\n下一步：使用这个统一的数据源重新生成首页和详情页")
