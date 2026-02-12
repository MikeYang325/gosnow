#!/usr/bin/env python3
"""更新首页为紧凑卡片样式"""
import json
import re

# 读取数据
with open('resort_details_full.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    resorts = data.get('resorts', data) if isinstance(data, dict) else data

with open('weather_data.json', 'r', encoding='utf-8') as f:
    weather_data = json.load(f)

with open('xiaohongshu_reviews.json', 'r', encoding='utf-8') as f:
    reviews = json.load(f)

# 地区分类
def get_region(address):
    if not address:
        return '其他'
    if '北海道' in address:
        return '北海道'
    elif any(x in address for x in ['青森', '岩手', '宮城', '秋田', '山形', '福島', '福岛']):
        return '东北'
    elif any(x in address for x in ['東京', '神奈川', '埼玉', '千葉', '茨城', '栃木', '群馬', '群马']):
        return '关东'
    elif any(x in address for x in ['新潟', '長野', '长野', '山梨', '静岡', '静冈', '岐阜', '愛知', '富山', '石川', '福井']):
        return '中部'
    elif any(x in address for x in ['大阪', '京都', '兵庫', '兵库', '滋賀', '滋贺', '奈良', '和歌山']):
        return '关西'
    return '其他'

# 生成卡片HTML
def generate_card(resort):
    name = resort.get('resort_name', '')
    english = resort.get('english_name', '')
    address = resort.get('address', '')
    website = resort.get('website', '')
    highlights = resort.get('highlights', '')
    ticket = resort.get('ticket_prices', {})
    ticket_price = ticket.get('one_day_adult', 'N/A')
    coords = resort.get('coordinates', '')

    region = get_region(address)

    # 天气数据
    w = weather_data.get(name, {})
    current = w.get('current', {})
    forecast = w.get('forecast', {})
    snow_24h = current.get('snow_24h', 0)
    temp = current.get('temperature', 0)
    snow_emoji = current.get('snow_emoji', '🌤️')
    forecast_7day = forecast.get('total_7day_snowfall', 0)

    # Windy URL
    windy_url = 'https://www.windy.com/?snow'
    if coords:
        parts = coords.split(',')
        if len(parts) == 2:
            windy_url = f'https://www.windy.com/{parts[1]}/{parts[0]}?{parts[1]},{parts[0]},10,snow'

    # 解析highlights
    trail_match = re.search(r'(\d+)\s*雪道', highlights)
    trails = trail_match.group(1) if trail_match else ''
    drop_match = re.search(r'落差(\d+)m', highlights)
    elevation = f'落差{drop_match.group(1)}m' if drop_match else ''
    snow_match = re.search(r'年降雪(\d+)m', highlights)
    annual_snow = f'年雪{snow_match.group(1)}m' if snow_match else ''

    # 评价
    review = reviews.get(name, resort.get('xiaohongshu_review', ''))

    # 详情页链接
    detail_url = f"resorts/{english.lower().replace(' ', '-').replace('/', '-')}.html"

    # 生成info标签
    info_tags = []
    if elevation:
        info_tags.append(f'<span class="info-tag">{elevation}</span>')
    if trails:
        info_tags.append(f'<span class="info-tag">{trails}条雪道</span>')
    if annual_snow:
        info_tags.append(f'<span class="info-tag">{annual_snow}</span>')
    info_tags.append(f'<span class="info-tag">{ticket_price}</span>')
    info_tags.append(f'<span class="info-tag forecast-tag">🔮 7天{forecast_7day:.1f}cm</span>')

    html = f'''        <div class="resort-card" data-region="{region}" data-snow="{snow_24h}" data-forecast="{forecast_7day}" onclick="window.location.href='{detail_url}'">
            <div class="resort-header">
                <span class="resort-name">{name}</span>
                <span class="region-tag">{region}</span>
                <a href="{windy_url}" target="_blank" class="snow-badge" onclick="event.stopPropagation()">{snow_emoji} {snow_24h:.1f}cm · {temp:.0f}°C</a>
            </div>
            <div class="resort-info">
                {' '.join(info_tags)}
            </div>
'''

    if review:
        html += f'''            <div class="xiaohongshu-review">💬 {review}</div>
'''

    html += '''        </div>

'''
    return html, snow_24h, forecast_7day

# 读取现有index.html获取头部和尾部
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到cards-grid的位置
cards_start = content.find('<div class="cards-grid" id="content">')
cards_end = content.find('</div>\n        </div>\n\n        <div class="footer">')

if cards_start == -1 or cards_end == -1:
    # 备用方案：找footer
    cards_end = content.find('<div class="footer">')
    if cards_end == -1:
        print("找不到卡片区域")
        exit(1)

header = content[:cards_start + len('<div class="cards-grid" id="content">\n')]
footer = content[cards_end:]

# 生成所有卡片
cards_html = ''
for resort in resorts:
    card, _, _ = generate_card(resort)
    cards_html += card

# 组合
new_content = header + cards_html + '        ' + footer

# 写入
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ 已更新首页，共 {len(resorts)} 个雪场卡片")
