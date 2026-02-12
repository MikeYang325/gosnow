#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从详情页提取信息并同步到首页
确保首页和详情页的雪票价格、雪道数量、描述等信息一致
"""
import re
from pathlib import Path

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

print("开始同步首页和详情页信息...\n")

# 读取首页
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

updated_count = 0

for resort_key, resort_name in resort_names.items():
    detail_file = Path(f'resorts/{resort_key}-new.html')
    if not detail_file.exists():
        print(f"⚠️  {resort_name}: 详情页不存在")
        continue

    # 读取详情页
    with open(detail_file, 'r', encoding='utf-8') as f:
        detail_content = f.read()

    # 提取详情页信息
    # 1. 雪道数量（支持两种格式）
    trails_match = re.search(r'<span class="info-label">雪道数量</span>\s*<span class="info-value">(?:<span>)?(\d+)条', detail_content)
    trails = trails_match.group(1) if trails_match else None

    # 2. 一日券价格（提取第一个价格，支持两种格式）
    price_match = re.search(r'<span class="info-label">一日券</span>\s*<span class="info-value">(?:<span>)?([¥￥][0-9,]+)', detail_content)
    price = price_match.group(1) if price_match else None

    # 3. 雪场特色（作为描述）
    feature_match = re.search(r'<span class="info-label">雪场特色</span>\s*<span class="info-value">([^<]+)</span>', detail_content)
    feature = feature_match.group(1).strip() if feature_match else None

    if not trails or not price:
        print(f"⚠️  {resort_name}: 无法提取完整信息 (雪道:{trails}, 价格:{price})")
        continue

    # 在首页中查找对应的雪场卡片
    # 查找模式：<span class="resort-name">雪场名</span>...到下一个</div>之前的内容
    card_pattern = rf'(<span class="resort-name">{re.escape(resort_name)}</span>.*?<div class="resort-info">)(.*?)(</div>)'
    card_match = re.search(card_pattern, index_content, flags=re.DOTALL)

    if not card_match:
        print(f"⚠️  {resort_name}: 在首页中未找到")
        continue

    # 提取当前的info区域
    current_info = card_match.group(2)

    # 更新雪道数量和价格
    # 保留天气预报和积雪深度标签，只更新雪道和价格
    new_info = re.sub(r'<span class="info-tag">\d+条雪道</span>', f'<span class="info-tag">{trails}条雪道</span>', current_info)
    new_info = re.sub(r'<span class="info-tag">[¥￥][0-9,]+</span>', f'<span class="info-tag">{price}</span>', new_info)

    # 替换首页内容
    new_card = card_match.group(1) + new_info + card_match.group(3)
    index_content = index_content.replace(card_match.group(0), new_card)

    print(f"✅ {resort_name}: {trails}条雪道, {price}")
    updated_count += 1

# 保存更新后的首页
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f"\n{'='*60}")
print(f"✅ 成功同步: {updated_count}/{len(resort_names)} 个雪场")
print(f"✅ 首页信息已更新")
