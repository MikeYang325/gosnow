#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
隐藏未完成的雪场：在没有-new.html的resort-card上添加 style="display:none;"
"""

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
for i, line in enumerate(lines):
    if 'class="resort-card"' in line:
        # 检查这一行是否已经包含-new.html
        if '-new.html' in line:
            # 已完成的雪场，保留
            output_lines.append(line)
        else:
            # 未完成的雪场，添加 style="display:none;"
            if 'style=' not in line:
                line = line.replace('class="resort-card"', 'class="resort-card" style="display:none;"')
            output_lines.append(line)
    else:
        output_lines.append(line)

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(output_lines)

print("✅ 已隐藏未完成的雪场")
