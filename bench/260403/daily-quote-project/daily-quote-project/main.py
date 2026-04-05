import json
import hashlib
from datetime import datetime


def load_quotes(filepath="quotes.json"):
    """quotes.json에서 명언 목록을 불러옵니다."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def pick_today_quote(quotes):
    """
    오늘 날짜를 기반으로 명언 1개를 선택합니다.
    같은 날이면 항상 같은 명언이 나오고, 날짜가 바뀌면 다른 명언이 나옵니다.
    """
    today_str = datetime.now().strftime("%Y-%m-%d")
    # 날짜 문자열의 해시값으로 인덱스 결정 (단순 나머지 연산보다 고르게 분포)
    hash_val = int(hashlib.md5(today_str.encode()).hexdigest(), 16)
    index = hash_val % len(quotes)
    return quotes[index], today_str


def pick_yesterday_quote(quotes):
    """어제의 명언을 선택합니다."""
    from datetime import timedelta
    yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    hash_val = int(hashlib.md5(yesterday_str.encode()).hexdigest(), 16)
    index = hash_val % len(quotes)
    return quotes[index], yesterday_str


def generate_html(today_quote, today_date, yesterday_quote, yesterday_date):
    """오늘의 명언을 보여주는 HTML 페이지를 생성합니다."""

    # 배경 그라데이션 색상도 날짜 기반으로 변경
    gradients = [
        ("linear-gradient(135deg, #0f0c29, #302b63, #24243e)", "#a78bfa"),
        ("linear-gradient(135deg, #0d1b2a, #1b2838, #1a1a2e)", "#38bdf8"),
        ("linear-gradient(135deg, #1a1a2e, #16213e, #0f3460)", "#818cf8"),
        ("linear-gradient(135deg, #0b0b0f, #1a1a2e, #162447)", "#34d399"),
        ("linear-gradient(135deg, #1b1b2f, #162447, #1a1a2e)", "#f472b6"),
        ("linear-gradient(135deg, #0d1117, #161b22, #21262d)", "#fbbf24"),
        ("linear-gradient(135deg, #1a1a2e, #0f3460, #162447)", "#fb923c"),
    ]
    day_of_year = datetime.now().timetuple().tm_yday
    bg_gradient, accent_color = gradients[day_of_year % len(gradients)]

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>오늘의 명언</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700;900&family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Inter', sans-serif;
            background: {bg_gradient};
            color: #e2e8f0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            overflow-x: hidden;
        }}

        /* 배경 장식 원 */
        body::before {{
            content: '';
            position: fixed;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, {accent_color}10, transparent 70%);
            top: -200px;
            right: -200px;
            border-radius: 50%;
            pointer-events: none;
        }}
        body::after {{
            content: '';
            position: fixed;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, {accent_color}08, transparent 70%);
            bottom: -100px;
            left: -100px;
            border-radius: 50%;
            pointer-events: none;
        }}

        .container {{
            max-width: 700px;
            width: 100%;
            text-align: center;
            position: relative;
            z-index: 1;
        }}

        /* 날짜 뱃지 */
        .date-badge {{
            display: inline-block;
            padding: 8px 24px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 30px;
            font-size: 0.85em;
            color: #94a3b8;
            margin-bottom: 50px;
            backdrop-filter: blur(10px);
        }}

        /* 메인 명언 카드 */
        .quote-card {{
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 24px;
            padding: 60px 50px;
            backdrop-filter: blur(20px);
            position: relative;
            margin-bottom: 40px;
            animation: fadeInUp 1s ease-out;
        }}

        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .quote-mark {{
            font-size: 5em;
            color: {accent_color};
            opacity: 0.3;
            font-family: Georgia, serif;
            line-height: 0.5;
            margin-bottom: 20px;
            display: block;
        }}

        .quote-text {{
            font-family: 'Noto Serif KR', serif;
            font-size: 1.7em;
            font-weight: 700;
            line-height: 1.8;
            color: #f1f5f9;
            margin-bottom: 30px;
            word-break: keep-all;
        }}

        .divider {{
            width: 60px;
            height: 2px;
            background: {accent_color};
            margin: 0 auto 25px;
            opacity: 0.5;
        }}

        .author {{
            font-size: 1.1em;
            color: {accent_color};
            font-weight: 600;
            margin-bottom: 5px;
        }}

        .era {{
            font-size: 0.8em;
            color: #64748b;
        }}

        /* 어제의 명언 */
        .yesterday {{
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 16px;
            padding: 25px 30px;
            margin-bottom: 40px;
            animation: fadeInUp 1.3s ease-out;
        }}

        .yesterday-label {{
            font-size: 0.75em;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }}

        .yesterday-quote {{
            font-family: 'Noto Serif KR', serif;
            font-size: 0.95em;
            color: #94a3b8;
            line-height: 1.7;
            font-style: italic;
        }}

        .yesterday-author {{
            font-size: 0.8em;
            color: #64748b;
            margin-top: 8px;
        }}

        /* 푸터 */
        footer {{
            font-size: 0.7em;
            color: #475569;
            margin-top: 20px;
            animation: fadeInUp 1.6s ease-out;
        }}
        footer a {{
            color: #64748b;
            text-decoration: none;
        }}

        /* 반응형 */
        @media (max-width: 600px) {{
            .quote-card {{ padding: 40px 25px; }}
            .quote-text {{ font-size: 1.3em; }}
            .quote-mark {{ font-size: 3em; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="date-badge">📅 {today_date}</div>

        <div class="quote-card">
            <span class="quote-mark">"</span>
            <div class="quote-text">{today_quote['quote']}</div>
            <div class="divider"></div>
            <div class="author">— {today_quote['author']}</div>
            <div class="era">{today_quote.get('era', '')}</div>
        </div>

        <div class="yesterday">
            <div class="yesterday-label">어제의 명언 · {yesterday_date}</div>
            <div class="yesterday-quote">"{yesterday_quote['quote']}"</div>
            <div class="yesterday-author">— {yesterday_quote['author']}</div>
        </div>

        <footer>
            Powered by Python + GitHub Actions · 매일 아침 자동 업데이트<br>
            <a href="https://github.com">GitHub Pages</a>에서 호스팅
        </footer>
    </div>
</body>
</html>"""
    return html


def main():
    print("=== 오늘의 명언 생성기 ===")

    # 1. 명언 데이터 로드
    quotes = load_quotes()
    print(f"총 {len(quotes)}개의 명언 로드 완료")

    # 2. 오늘의 명언 선택
    today_quote, today_date = pick_today_quote(quotes)
    print(f"오늘의 명언 ({today_date}): \"{today_quote['quote']}\" - {today_quote['author']}")

    # 3. 어제의 명언 선택
    yesterday_quote, yesterday_date = pick_yesterday_quote(quotes)

    # 4. HTML 생성
    html = generate_html(today_quote, today_date, yesterday_quote, yesterday_date)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html 생성 완료!")
    print("=== 완료 ===")


if __name__ == "__main__":
    main()
