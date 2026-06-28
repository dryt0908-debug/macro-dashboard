import requests
from bs4 import BeautifulSoup
import datetime

def fetch_data():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # 1. 주식봇 펀드플로우 
    fund_text = "정상 조회 (링크 이동 필요)" 

    # 2. 인베스팅닷컴 글로벌 뉴스 RSS
    news_list = []
    try:
        rss_url = "https://kr.investing.com/rss/news_285.rss"
        res_news = requests.get(rss_url, headers=headers, timeout=10)
        soup_news = BeautifulSoup(res_news.text, 'xml')
        items = soup_news.find_all('item')[:3]
        for item in items:
            title = item.title.text if item.title else "제목 없음"
            pub_date = item.pubDate.text[17:22] if item.pubDate else "--:--"
            news_list.append({"time": pub_date, "title": title})
    except:
        news_list = [{"time": "00:00", "title": "뉴스 피드를 불러오지 못했습니다."}]

    while len(news_list) < 3:
        news_list.append({"time": "--:--", "title": "최신 속보가 없습니다."})

    return fund_text, news_list

def generate_html(fund_text, news_list):
    now = datetime.datetime.now() + datetime.timedelta(hours=9)
    date_str = now.strftime("%Y년 %m월 %d일 %A")

    html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>아침 경제 브리핑</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background-color: #f4f6f9; color: #333; padding: 16px; max-width: 600px; margin: 0 auto; }}
        header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        header h1 {{ font-size: 18pt; margin-bottom: 4px; }}
        header p {{ font-size: 10pt; opacity: 0.8; }}
        .card {{ background: white; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .card h2 {{ font-size: 13pt; color: #1e3c72; margin-bottom: 12px; border-left: 4px solid #1e3c72; padding-left: 8px; }}
        .data-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #f0f0f0; font-size: 11pt; }}
        .data-row:last-child {{ border-bottom: none; }}
        .label {{ color: #666; }}
        .value {{ font-weight: bold; }}
        .news-item {{ padding: 8px 0; border-bottom: 1px solid #f0f0f0; }}
        .news-item:last-child {{ border-bottom: none; }}
        .news-time {{ font-size: 9pt; color: #999; display: block; }}
        .news-title {{ font-size: 10.5pt; font-weight: 500; color: #222; text-decoration: none; }}
    </style>
</head>
<body>
    <header>
        <h1>🌅 아침 경제 브리핑</h1>
        <p>{date_str} 08:00 기준 업데이트</p>
    </header>

    <div class="card">
        <h2>📊 글로벌 자금 흐름</h2>
        <div class="data-row">
            <span class="label">Jusikbot 상태</span>
            <span class="value">{fund_text}</span>
        </div>
        <div class="data-row">
            <span class="label">바로가기</span>
            <span class="value"><a href="https://jusikbot.com/fund-flow" target="_blank" style="color:#2a5298;">[링크 이동]</a></span>
        </div>
    </div>

    <div class="card">
        <h2>📰 실시간 핵심 속보 (Investing)</h2>
        <div class="news-item">
            <span class="news-time">{news_list[0]['time']}</span>
            <div class="news-title">{news_list[0]['title']}</div>
        </div>
        <div class="news-item">
            <span class="news-time">{news_list[1]['time']}</span>
            <div class="news-title">{news_list[1]['title']}</div>
        </div>
        <div class="news-item">
            <span class="news-time">{news_list[2]['time']}</span>
            <div class="news-title">{news_list[2]['title']}</div>
        </div>
    </div>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    fund, news = fetch_data()
    generate_html(fund, news)
