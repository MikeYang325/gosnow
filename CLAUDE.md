# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**追雪 (GoSnow)** - A Japanese ski resort information aggregation website featuring 51 ski resorts with real-time weather forecasts, snowfall predictions, and user reviews.

- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks)
- **Data Generation**: Python scripts
- **Deployment**: GitHub Pages
- **Domain**: gosnow.site

## Architecture

### Data Flow

```
resort_details_full.json (static resort data)
         ↓
    Python scripts
         ↓
forecast_7day.json (weather API data) + xiaohongshu_reviews.json
         ↓
generate_mobile_version.py → index.html (homepage)
generate_detail_pages.py → detail_*.html (51 detail pages)
         ↓
    Deploy to server
```

### Key Components

1. **Data Layer**
   - `resort_details_full.json`: Master resort data (51 resorts) with coordinates, ticket prices, transport info, highlights, night skiing info
   - `forecast_7day.json`: 7-day weather forecasts per resort (temperature, snowfall) from OpenWeatherMap API
   - `xiaohongshu_reviews.json`: User reviews from Xiaohongshu (Chinese social platform)

2. **Generation Scripts** (Python)
   - `generate_mobile_version.py`: Generates `index.html` with region filtering and sorting
   - `generate_detail_pages.py`: Generates 51 individual resort detail pages
   - `fetch_openweather_forecast.py`: Fetches weather data from OpenWeatherMap API (requires `OPENWEATHER_API_KEY` env var)

3. **Frontend**
   - `index.html`: Homepage with region tabs (全部/北海道/长野/新潟/群马/山形), sorting options (current snowfall/7-day snowfall/score), and resort cards
   - `detail_*.html`: Individual resort pages with weather charts, transport info, reviews, and navigation links
   - Mobile-first responsive design with max-width 900px centered layout

### Data Structure

**Resort Object** (in resort_details_full.json):
```json
{
  "resort_name": "二世谷联合雪场",
  "english_name": "Niseko United",
  "japanese_name": "ニセコユナイテッド",
  "address": "北海道虻田郡倶知安町...",
  "website": "https://...",
  "coordinates": "142.8694,42.8247",
  "ticket_prices": {"one_day_adult": "¥8,200"},
  "highlights": "308-1308m，76 雪道，粉雪量 15m+",
  "night_skiing_info": "有；Grand Hirafu 区 ¥3,500...",
  "transport": "...",
  "transport_detailed": "...",
  "xiaohongshu_review": "粉雪天花板，进阶玩家天堂...",
  "weather_data": {
    "temperature": -8,
    "snow_24h": 10,
    "snow_emoji": "❄️❄️",
    "weather_text": "中雪"
  }
}
```

**Forecast Object** (in forecast_7day.json):
```json
{
  "resort_name": {
    "total_7day_snowfall": 0.6,
    "daily_snowfall": [0.0, 0.0, 0.1, ...],
    "daily_temperature": [-12.6, -11.3, -10.8, ...],
    "max_day_snowfall": 0.3
  }
}
```

## Common Development Tasks

### Update Weather Data
```bash
cd /Users/mac/Documents/cc/gosnow/
python3 fetch_openweather_forecast.py
```
This fetches 7-day forecasts from OpenWeatherMap API for all 51 resorts and updates `forecast_7day.json`.

### Regenerate HTML Pages
```bash
python3 generate_mobile_version.py  # Generates index.html
python3 generate_detail_pages.py    # Generates detail_*.html (51 files)
```
Run these after modifying data files or generation scripts. Always regenerate before deploying.

### Deploy via GitHub Pages
```bash
git add .
git commit -m "Update content"
git push origin main
```

### Local Testing
```bash
open index.html  # View homepage in browser
open detail_二世谷联合雪场.html  # View a detail page
```

## Important Rules

**CRITICAL**: Read `PROJECT_RULES.md` and `WORKLOG.md` before making changes. These files contain:
- Deployment procedures
- File naming conventions (detail pages must be `detail_{resort_name}.html`)
- Workflow requirements (always regenerate HTML after code changes)
- Work logging requirements (update WORKLOG.md after each session)

### Key Constraints

1. **File Naming**: Do not rename `index.html` or change detail page naming scheme
2. **Data Integrity**: Do not manually edit generated HTML files; regenerate from scripts instead
3. **Deployment**: Always test locally before deploying; push to GitHub for deployment
4. **Documentation**: Update WORKLOG.md with all changes and deployment results

## File Organization

```
/Users/mac/Documents/cc/gosnow/
├── index.html                      # Generated homepage
├── detail_*.html                   # Generated detail pages (51 files)
├── wx.jpg                          # WeChat QR code image
├── resort_details_full.json        # Master resort data (DO NOT EDIT MANUALLY)
├── forecast_7day.json              # Weather data (auto-updated)
├── xiaohongshu_reviews.json        # User reviews
├── generate_mobile_version.py      # Homepage generator
├── generate_detail_pages.py        # Detail page generator
├── fetch_openweather_forecast.py   # Weather fetcher
├── PROJECT_RULES.md                # Project rules (MUST READ)
├── WORKLOG.md                      # Work log (MUST UPDATE)
└── README.md                       # Quick start guide
```

## Styling & Design

- **Color Scheme**: Purple gradient (667eea → 764ba2)
- **Layout**: Centered, max-width 900px, mobile-first responsive
- **Typography**: System fonts (-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC')
- **Cards**: Compact design with hover effects, shadow on interaction
- **Charts**: Temperature (red dots) + snowfall (blue bars) combined visualization

## Deployment Environment

- **Platform**: GitHub Pages
- **Domain**: gosnow.site

## Before Making Changes

1. Read the latest entry in `WORKLOG.md` to understand current state
2. Check `PROJECT_RULES.md` for any constraints
3. For data changes: modify JSON files, then regenerate HTML
4. For code changes: test locally with `python3 generate_*.py`, then verify HTML output
5. Always update `WORKLOG.md` with your changes before finishing
