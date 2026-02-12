#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新index.html：
1. 将28个已完成雪场的链接改为-new.html
2. 隐藏其他未完成的雪场
"""

# 28个已完成的雪场（英文文件名，不含后缀）
completed_resorts = [
    'appi-kogen-ski-resort',
    'asahidake-ski-resort',
    'furano-ski-resort',
    'gala-yuzawa-ski-resort',
    'hakkaisan-ski-resort',
    'hakkoda-ski-resort',
    'hakuba-47-ski-resort',
    'hakuba-goryu-ski-resort',
    'hakuba-happo-one-ski-resort',
    'hakuba-tsugaike-ski-resort',
    'hoshino-resorts-tomamu',
    'ishiuchi-maruyama-ski-resort',
    'iwappara-ski-resort',
    'kagura-ski-resort',
    'kamui-ski-links',
    'karuizawa-prince-ski-resort',
    'kiroro-ski-resort',
    'lotte-arai-resort',
    'madarao-kogen-ski-resort',
    'myoko-kogen-ski-resort',
    'naeba-ski-resort',
    'niseko-united',
    'nozawa-onsen-ski-resort',
    'rusutsu-resort',
    'sapporo-teine-ski-resort',
    'shiga-kogen-ski-resort',
    'sugadaira-kogen-ski-resort',
    'zao-onsen-ski-resort',
]

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 将已完成雪场的链接改为-new.html
for resort in completed_resorts:
    # 替换 onclick 中的链接
    content = content.replace(
        f"onclick=\"window.location.href='resorts/{resort}.html'\"",
        f"onclick=\"window.location.href='resorts/{resort}-new.html'\""
    )
    # 替换详情按钮中的链接
    content = content.replace(
        f"href=\"resorts/{resort}.html\"",
        f"href=\"resorts/{resort}-new.html\""
    )

# 2. 隐藏未完成的雪场卡片（添加 style="display:none;"）
import re

# 找到所有 resort-card，检查是否在已完成列表中
def hide_incomplete_cards(match):
    card_html = match.group(0)
    # 检查这个卡片是否指向已完成的雪场
    is_completed = any(resort in card_html for resort in completed_resorts)

    if is_completed:
        return card_html  # 保留已完成的
    else:
        # 隐藏未完成的：在 class="resort-card" 后添加 style="display:none;"
        return card_html.replace(
            'class="resort-card"',
            'class="resort-card" style="display:none;"',
            1
        )

# 使用正则匹配所有 resort-card（包括多行）
pattern = r'<div class="resort-card"[^>]*>.*?</div>\s*</div>\s*</div>'
content = re.sub(pattern, hide_incomplete_cards, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ index.html 已更新：")
print(f"  - 28个已完成雪场链接已改为 -new.html")
print(f"  - 43个未完成雪场已隐藏")
