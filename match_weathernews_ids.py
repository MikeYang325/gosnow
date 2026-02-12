#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从weathernews.jp的JSON数据中匹配28个已完成雪场的spot_id
"""

# 我们28个雪场的日文名称（需要匹配）
our_resorts = {
    'niseko-united': ['ニセコ', 'ニセコユナイテッド', 'ニセコアンヌプリ'],
    'furano-ski-resort': ['富良野'],
    'rusutsu-resort': ['ルスツ'],
    'hoshino-resorts-tomamu': ['トマム', '星野リゾート　トマム'],
    'kiroro-ski-resort': ['キロロ'],
    'shiga-kogen-ski-resort': ['志賀高原'],
    'nozawa-onsen-ski-resort': ['野沢温泉'],
    'naeba-ski-resort': ['苗場'],
    'gala-yuzawa-ski-resort': ['ガーラ湯沢', 'GALA湯沢'],
    'kagura-ski-resort': ['かぐら', 'みつまた'],
    'myoko-kogen-ski-resort': ['妙高'],
    'zao-onsen-ski-resort': ['蔵王'],
    'hakuba-happo-one-ski-resort': ['八方尾根', '白馬八方尾根'],
    'hakuba-goryu-ski-resort': ['五竜', '白馬五竜'],
    'hakuba-47-ski-resort': ['Hakuba47', '白馬47'],
    'hakuba-tsugaike-ski-resort': ['栂池', '白馬栂池'],
    'sapporo-teine-ski-resort': ['手稲', 'サッポロテイネ'],
    'kamui-ski-links': ['カムイ'],
    'asahidake-ski-resort': ['旭岳'],
    'madarao-kogen-ski-resort': ['斑尾'],
    'karuizawa-prince-ski-resort': ['軽井沢'],
    'sugadaira-kogen-ski-resort': ['菅平'],
    'ishiuchi-maruyama-ski-resort': ['石打丸山'],
    'iwappara-ski-resort': ['岩原'],
    'lotte-arai-resort': ['ロッテアライ', 'アライ'],
    'hakkaisan-ski-resort': ['八海山'],
    'hakkoda-ski-resort': ['八甲田'],
    'appi-kogen-ski-resort': ['安比高原'],
}

# 从用户提供的JSON中提取（这里只是示例，实际需要完整JSON）
# 已知的匹配：
known_matches = {
    'hoshino-resorts-tomamu': '31201',  # 星野リゾート　トマム
    'kamui-ski-links': '31203',  # カムイスキーリンクス
}

print("已知匹配的雪场ID：")
for resort, spotid in known_matches.items():
    print(f"  {resort}: {spotid}")
