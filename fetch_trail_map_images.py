#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬取雪道图页面，提取静态图片URL
"""

import json
import re
import urllib.request
import urllib.error
from urllib.parse import urljoin
import ssl

# 忽略SSL证书验证
ssl._create_default_https_context = ssl._create_unverified_context

def fetch_page(url, timeout=10):
    """获取页面内容"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  获取失败: {e}")
        return None

def extract_trail_map_image(html, base_url):
    """从HTML中提取雪道图图片URL"""
    if not html:
        return None

    # 常见的雪道图图片模式
    patterns = [
        # 直接匹配常见的雪道图图片命名
        r'<img[^>]+src=["\']([^"\']*(?:map|course|gelande|trail|slope|コース|ゲレンデ)[^"\']*\.(?:jpg|jpeg|png|webp|gif))["\']',
        r'<img[^>]+src=["\']([^"\']*\.(?:jpg|jpeg|png|webp|gif))["\'][^>]*(?:map|course|gelande|trail|slope)',
        # 匹配大图链接
        r'<a[^>]+href=["\']([^"\']*(?:map|course|gelande|trail|slope)[^"\']*\.(?:jpg|jpeg|png|webp|gif))["\']',
        # 匹配背景图
        r'background(?:-image)?:\s*url\(["\']?([^"\')\s]+(?:map|course|gelande)[^"\')\s]*\.(?:jpg|jpeg|png|webp|gif))["\']?\)',
        # 通用图片匹配（优先级较低）
        r'<img[^>]+src=["\']([^"\']+\.(?:jpg|jpeg|png|webp))["\']',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        for match in matches:
            # 过滤掉小图标、logo等
            if any(skip in match.lower() for skip in ['icon', 'logo', 'button', 'banner', 'thumb', 'sns', 'facebook', 'twitter', 'instagram', 'line', 'youtube']):
                continue
            # 转换为绝对URL
            img_url = urljoin(base_url, match)
            return img_url

    return None

def main():
    # 读取数据
    with open('resort_details_full.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0

    for resort in data['resorts']:
        name = resort['resort_name']
        trail_map_url = resort.get('trail_map', '')

        if not trail_map_url:
            continue

        # 跳过PDF
        if trail_map_url.lower().endswith('.pdf'):
            print(f"⏭️ {name}: PDF文件，跳过")
            continue

        # 如果URL本身就是图片
        if any(trail_map_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
            resort['trail_map_image'] = trail_map_url
            print(f"✅ {name}: URL本身是图片")
            updated_count += 1
            continue

        print(f"🔍 {name}: 爬取 {trail_map_url}")
        html = fetch_page(trail_map_url)

        if html:
            img_url = extract_trail_map_image(html, trail_map_url)
            if img_url:
                resort['trail_map_image'] = img_url
                print(f"  ✅ 找到图片: {img_url}")
                updated_count += 1
            else:
                print(f"  ❌ 未找到图片")
        else:
            print(f"  ❌ 页面获取失败")

    # 保存更新后的数据
    with open('resort_details_full.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 完成！更新了 {updated_count} 个雪场的雪道图图片")

if __name__ == '__main__':
    main()
