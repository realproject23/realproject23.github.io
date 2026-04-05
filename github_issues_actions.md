# GitHub Issues & Actions Workflow Plan
# (GitHub 이슈 및 액션 워크플로우 계획)

## 📋 Goal: Automate Project Management and Deployment
# (목표: 프로젝트 관리 및 배포 자동화)
**Project:** Youth Canvas (Integrated Youth Facility Management Platform)
# (프로젝트: Youth Canvas - 청소년 시설 통합 관리 플랫폼)
**Reference:** `c:\anti\real_project\bench\260403` (GitHub Actions-based automation)
# (참조: c:\anti\real_project\bench\260403 - GitHub 액션 기반 자동화)

---

## 🗓 Interaction Log
# (📅 상호작용 기록)

| Date & Time | Participant | Description |
| :--- | :--- | :--- |
| 2026-04-05 18:17 | USER | Requested to proceed with the server deployment stage using GitHub Issues and Actions, referencing the provided bench project. |
| (사용자: 제공된 벤치 프로젝트를 참조하여 GitHub 이슈 및 액션을 활용한 서버 배포 단계를 진행하도록 요청함) | | |
| 2026-04-05 18:18 | Antigravity | Analyzed the sample project. Identified a "self-updating" static site pattern using GitHub Actions and Python. Started drafting the integration plan. |
| (Antigravity: 샘플 프로젝트 분석 완료. GitHub 액션과 파이썬을 활용한 "자체 업데이트" 정적 사이트 패턴 확인 후 통합 계획 초안 작성 시작) | | |
| 2026-04-05 18:22 | Antigravity | Started creating Issue Templates and Deployment Workflows. Added Korean translations to documentation. |
| (Antigravity: 이슈 템플릿 및 배포 워크플로우 생성 시작. 문서에 한글 번역 주석 추가) | | |

---

## 👥 Roles and Responsibilities
# (👥 역할 및 책임)

### 🤖 AI (Antigravity) Role
# (🤖 AI (Antigravity) 의 역할)
- **Action Scripting**: Create and maintain YAML files in `.github/workflows/`.
# (액션 스크립트 작성: .github/workflows/ 폴더 내 YAML 파일 생성 및 유지보수)
- **Python-Action Integration**: Develop Python scripts that the Actions will trigger (e.g., data report generators, automated status checkers).
# (파이썬-액션 통합: 액션이 실행할 파이썬 스크립트 개발 - 예: 데이터 보고서 생성기, 자동 상태 점검기 등)
- **Issue Automation**: Suggest and implement Issue Templates to standardize user requests.
# (이슈 자동화: 사용자 요청을 표준화하기 위한 이슈 템플릿 제안 및 구현)
- **Documentation**: Continuously log progress in `.md` files.
# (문서화: .md 파일에 진행 상황을 지속적으로 기록)

### 👤 USER Role
# (👤 사용자(USER) 의 역할)
- **Organization Settings**: Manage secrets (API keys) in GitHub repository settings.
# (조직 설정: GitHub 저장소 설정에서 보안 비밀번호(API 키 등) 관리)
- **Feedback & Direction**: Decide which features should be automated.
# (피드백 및 방향 설정: 어떤 기능을 자동화할지 결정)
- **Approval**: Monitor and approve Issue requests or Actions results on the GitHub interface.
# (승인: GitHub 인터페이스에서 이슈 요청 또는 액션 결과 모니터링 및 승인)
- **Security Management**: Ensure `serviceAccountKey.json` is safely provided as a GitHub Secret if needed for Actions.
# (보안 관리: 액션에 필요한 경우 serviceAccountKey.json 파일을 GitHub Secret으로 안전하게 제공)

---

## 🚀 Priority Automation Tasks
# (🚀 우선순위 자동화 작업)

### 1. GitHub Issues: Request Management
# (1. GitHub 이슈: 요청 관리)
Standardize how students, parents, or admins report issues or request approvals.
# (학생, 학부모 또는 관리자가 문제를 보고하거나 승인을 요청하는 방식을 표준화함)
- **Template 1**: Student Enrollment Request.
# (템플릿 1: 학생 수강 신청 요청)
- **Template 2**: Task Approval Request.
# (템플릿 2: 미션/과제 승인 요청)
- **Action**: I will create `.github/ISSUE_TEMPLATE` files to manage these.
# (수행: 이를 관리하기 위해 .github/ISSUE_TEMPLATE 파일을 생성함)

### 2. GitHub Actions: Automated Dashboard Updates
# (2. GitHub 액션: 자동 대시보드 업데이트)
Similar to the "Daily Quote" reference, we can have an Action that runs a script to update a summary page.
# ("오늘의 명언" 참조 사례와 유사하게, 요약 페이지를 업데이트하는 스크립트를 실행하는 액션을 구성할 수 있음)
- **Workflow**: `dashboard_sync.yml`.
# (워크플로우 파일명: dashboard_sync.yml)
- **Function**: Weekly or daily update of student statistics (e.g., total enrollment) and saving it as a static JSON or HTML file for the public site.
# (기능: 학생 통계(예: 전체 등록 수)를 주간 또는 일간으로 업데이트하고 이를 공개 사이트용 정적 JSON 또는 HTML 파일로 저장)

### 3. GitHub Actions: Continuous Deployment (CD)
# (3. GitHub 액션: 지속적 배포 (CD))
- **Workflow**: `deploy.yml`.
# (워크플로우 파일명: deploy.yml)
- **Function**: Automatically push latest code to the static hosting and verify backend consistency.
# (기능: 최신 코드를 정적 호스팅에 자동으로 푸시하고 백엔드 일관성 검증)

---

## 🔒 Security Configuration (For USER)
# (🔒 보안 설정 - 사용자용 지침)
To make Actions work with Firebase, the following **GitHub Secrets** must be added by the USER:
# (액션이 Firebase와 연동되게 하려면 사용자가 다음 GitHub Secrets를 추가해야 함:)
1. `FIREBASE_SERVICE_ACCOUNT`: The contents of `serviceAccountKey.json`.
# (FIREBASE_SERVICE_ACCOUNT: serviceAccountKey.json 파일의 내용)
2. `ENV_FILE`: The contents of `.env`.
# (ENV_FILE: .env 파일의 내용)

**Action Needed**: I will prepare the Issue Templates and the first Workflow file as a draft.
# (필요한 도구: 이슈 템플릿과 첫 번째 워크플로우 파일 초안을 준비하겠음)
