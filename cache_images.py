#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载所有详情页的hero图片和雪道图，保存到本地images文件夹
并更新HTML中的图片链接
"""
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

# 创建images目录
images_dir = Path('images')
images_dir.mkdir(exist_ok=True)

# 获取所有详情页
detail_pages = list(Path('resorts').glob('*-new.html'))

print(f"找到 {len(detail_pages)} 个详情页\n")

total_images = 0
downloaded_images = 0
failed_images = []

for html_file in detail_pages:
    resort_name = html_file.stem.replace('-new', '')
    print(f"处理: {resort_name}")

    # 读取HTML内容
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 查找所有图片URL
    # 匹配 hero-image 和 trail-map-img
    hero_pattern = r'<img class="hero-image" src="([^"]+)"'
    trail_pattern = r'<img class="trail-map-img" src="([^"]+)"'

    hero_match = re.search(hero_pattern, html_content)
    trail_match = re.search(trail_pattern, html_content)

    images_to_download = []
    if hero_match:
        images_to_download.append(('hero', hero_match.group(1)))
    if trail_match:
        images_to_download.append(('trail', trail_match.group(1)))

    if not images_to_download:
        print(f"  ⚠️  未找到图片")
        continue

    # 下载图片
    for img_type, img_url in images_to_download:
        total_images += 1

        # 获取文件扩展名
        parsed_url = urlparse(img_url)
        ext = Path(parsed_url.path).suffix or '.jpg'

        # 生成本地文件名
        local_filename = f"{resort_name}-{img_type}{ext}"
        local_path = images_dir / local_filename

        # 如果文件已存在，跳过下载
        if local_path.exists():
            print(f"  ✓ {img_type}: 已存在 {local_filename}")
            downloaded_images += 1

            # 更新HTML中的链接
            if img_type == 'hero':
                html_content = re.sub(
                    hero_pattern,
                    f'<img class="hero-image" src="../images/{local_filename}"',
                    html_content
                )
            else:
                html_content = re.sub(
                    trail_pattern,
                    f'<img class="trail-map-img" src="../images/{local_filename}"',
                    html_content
                )
            continue

        # 下载图片
        try:
            print(f"  ⬇️  下载 {img_type}: {img_url}")
            result = subprocess.run(
                ['curl', '-L', '-s', '-o', str(local_path), img_url],
                capture_output=True,
                timeout=30
            )

            if result.returncode == 0 and local_path.exists() and local_path.stat().st_size > 0:
                print(f"  ✅ 保存为: {local_filename}")
                downloaded_images += 1

                # 更新HTML中的链接
                if img_type == 'hero':
                    html_content = re.sub(
                        hero_pattern,
                        f'<img class="hero-image" src="../images/{local_filename}"',
                        html_content
                    )
                else:
                    html_content = re.sub(
                        trail_pattern,
                        f'<img class="trail-map-img" src="../images/{local_filename}"',
                        html_content
                    )
            else:
                print(f"  ❌ 下载失败")
                failed_images.append((resort_name, img_type, img_url))
                if local_path.exists():
                    local_path.unlink()
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            failed_images.append((resort_name, img_type, img_url))
            if local_path.exists():
                local_path.unlink()

    # 保存更新后的HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print()

print("=" * 60)
print(f"总计: {total_images} 张图片")
print(f"成功: {downloaded_images} 张")
print(f"失败: {len(failed_images)} 张")

if failed_images:
    print("\n失败的图片:")
    for resort, img_type, url in failed_images:
        print(f"  - {resort} ({img_type}): {url}")
