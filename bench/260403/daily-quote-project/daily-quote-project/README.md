# ✨ 오늘의 명언 — 매일 바뀌는 자동화 명언 페이지

매일 아침 자동으로 명언이 바뀌는 웹페이지입니다.  
GitHub Actions가 매일 `main.py`를 실행하여 오늘에 해당하는 명언을 골라 `index.html`을 생성합니다.

## 🛠 구성
- `quotes.json` — 명언 40개 데이터 (퍼블릭 도메인)
- `main.py` — 오늘 날짜 기반으로 명언 1개 선택 + HTML 생성
- `.github/workflows/daily_quote.yml` — 매일 아침 자동 실행 설정

## 💡 특징
- 외부 패키지(pip install) **불필요** — 파이썬 표준 라이브러리만 사용
- 배경 그라데이션 색상이 매일 바뀜
- "어제의 명언" 섹션 포함
- 모바일 반응형 디자인

## 🚀 배포 방법
1. 이 폴더의 **내용물**을 GitHub 리포지토리에 업로드
2. Settings → Pages → Branch: `main` 선택
3. Actions 탭 → `Daily Quote Generator` → Run workflow
4. `https://[이름].github.io/` 에서 확인!
