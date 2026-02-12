#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
匹配我们28个雪场的weathernews spot_id
"""
import json

# 读取weathernews的完整雪场列表
with open('weathernews_resorts.json', 'r', encoding='utf-8') as f:
    all_resorts = json.load(f)

# 我们28个雪场的关键词匹配（日文名称）
our_resorts_keywords = {
    'niseko-united': ['ニセコ', 'アンヌプリ', 'ビラフ', 'ひらふ'],
    'furano-ski-resort': ['富良野'],
    'rusutsu-resort': ['ルスツ'],
    'hoshino-resorts-tomamu': ['トマム'],
    'kiroro-ski-resort': ['キロロ'],
    'shiga-kogen-ski-resort': ['志賀高原'],
    'nozawa-onsen-ski-resort': ['野沢温泉'],
    'naeba-ski-resort': ['苗場'],
    'gala-yuzawa-ski-resort': ['ガーラ湯沢', 'GALA'],
    'kagura-ski-resort': ['かぐら', 'みつまた'],
    'myoko-kogen-ski-resort': ['妙高'],
    'zao-onsen-ski-resort': ['蔵王'],
    'hakuba-happo-one-ski-resort': ['八方尾根'],
    'hakuba-goryu-ski-resort': ['五竜', 'Hakuba47'],
    'hakuba-47-ski-resort': ['Hakuba47', 'HAKUBA47'],
    'hakuba-tsugaike-ski-resort': ['栂池'],
    'sapporo-teine-ski-resort': ['手稲', 'テイネ'],
    'kamui-ski-links': ['カムイ'],
    'asahidake-ski-resort': ['旭岳'],
    'madarao-kogen-ski-resort': ['斑尾'],
    'karuizawa-prince-ski-resort': ['軽井沢'],
    'sugadaira-kogen-ski-resort': ['菅平'],
    'ishiuchi-maruyama-ski-resort': ['石打丸山'],
    'iwappara-ski-resort': ['岩原'],
    'lotte-arai-resort': ['ロッテアライ', 'アライリゾート'],
    'hakkaisan-ski-resort': ['八海山'],
    'hakkoda-ski-resort': ['八甲田'],
    'appi-kogen-ski-resort': ['安比高原'],
}

# 匹配结果
matches = {}
unmatched = []

for our_key, keywords in our_resorts_keywords.items():
    found = False
    for resort in all_resorts:
        name = resort['pointname']
        # 检查是否包含任何关键词
        for keyword in keywords:
            if keyword in name:
                matches[our_key] = {
                    'spotid': resort['spotid'],
                    'name': name,
                    'depth': resort.get('depth', ''),
                    'lat': resort.get('lat', ''),
                    'lon': resort.get('lon', ''),
                }
                found = True
                break
        if found:
            break

    if not found:
        unmatched.append(our_key)

# 输出结果
print(f"✅ 成功匹配 {len(matches)}/28 个雪场\n")
print("匹配结果：")
for key, info in sorted(matches.items()):
    print(f"  {key}")
    print(f"    ID: {info['spotid']}, 名称: {info['name']}, 积雪: {info['depth']}cm")

if unmatched:
    print(f"\n❌ 未匹配的雪场 ({len(unmatched)}):")
    for key in unmatched:
        print(f"  - {key}")
        print(f"    关键词: {our_resorts_keywords[key]}")

# 保存匹配结果
with open('resort_id_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(matches, f, ensure_ascii=False, indent=2)

print(f"\n✅ 匹配结果已保存到 resort_id_mapping.json")
