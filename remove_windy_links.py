#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除所有雪场页面中的windy链接
"""
import re
from pathlib import Path

resorts_dir = Path('resorts')
updated_count = 0

for html_file in resorts_dir.glob('*-new.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 删除windy链接（包括整个<a>标签）
    pattern = r'\s*<a class="windy-link"[^>]*>.*?</a>'
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)

    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_count += 1
        print(f"✅ {html_file.name}")

print(f"\n✅ 已删除 {updated_count} 个文件中的windy链接")
