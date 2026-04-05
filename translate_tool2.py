import os
import re

i18n_keys = {}

def add_i18n(key, ko, en):
    i18n_keys[key] = {"ko": ko, "en": en}

# Top Tabs / Sections
add_i18n("admin_new_prog_title", "✨ 새로운 프로그램 기획", "✨ Plan New Program")
add_i18n("admin_new_step1", "1. 미디어 첨부", "1. Attach Media")
add_i18n("admin_new_step2", "2. 프로그램 기본 정보", "2. Basic Info")
add_i18n("admin_new_step3", "3. 워크플로우 기획", "3. Workflow Planning")
add_i18n("admin_new_yt", "유튜브 영상 링크 (옵션)", "YouTube Link (Optional)")
add_i18n("admin_new_poster", "포스터 이미지 (1MB 이하 필수)", "Poster Image (Max 1MB)")
add_i18n("admin_new_upload", "클릭하여 이미지 업로드<br>(Drag & Drop 불가)", "Click to upload image<br>(No Drag & Drop)")
add_i18n("admin_new_pname", "프로그램 명", "Program Name")
add_i18n("admin_new_color", "캘린더 색상", "Color")
add_i18n("admin_new_start", "모집 시작일", "Start Date")
add_i18n("admin_new_end", "모집 종료일", "End Date")
add_i18n("admin_new_max", "모집 정원 (명)", "Capacity (ppl)")
add_i18n("admin_new_desc", "프로그램 한줄 소개", "Short Description")
add_i18n("admin_new_guide", "세부 일정 표기 가이드", "Schedule Format Guide")
add_i18n("admin_new_guide_desc", "시간은 빈틈없이 소괄호( ) 안에 적어주세요! (예: 2026-03-23 (14:00) : OT)", "Put time in parentheses! (e.g., 2026-03-23 (14:00) : OT)")
add_i18n("admin_new_fill_ex", "✏️ 예시 양식 채우기", "✏️ Fill Example")
add_i18n("admin_parent_title", "👨‍👩‍👧‍👦 신규 학부모 계정 연동", "👨‍👩‍👧‍👦 Link New Parent Account")
add_i18n("admin_parent_desc", "학생이 먼저 시스템에 등록되어 있어야 합니다. (수강신청 완료 필수)", "Student must be registered first.")
add_i18n("admin_parent_pname", "학부모 성함", "Parent Name")
add_i18n("admin_parent_child", "연동할 자녀 실명", "Child Full Name")
add_i18n("admin_parent_pin", "학부모 로그인 PIN (4자리)", "Parent PIN (4 digits)")
add_i18n("admin_parent_create", "🔗 학부모 계정 생성", "🔗 Create Parent Account")
add_i18n("admin_att_sel_prog", "📌 대상 프로그램 선택", "📌 Select Target Program")
add_i18n("admin_att_tab_daily", "📝 일일 출석부", "📝 Daily Attendance")
add_i18n("admin_att_tab_stat", "📊 출결 통계", "📊 Attendance Stats")
add_i18n("admin_att_tab_edit", "⚙️ 출결 수정/삭제", "⚙️ Edit Attendance")
add_i18n("admin_att_date", "체크할 날짜", "Date to Check")
add_i18n("admin_att_save", "💾 일괄 저장 (서버 전송)", "💾 Save to Server")
add_i18n("admin_eval_sel", "학생 검색 및 선택", "Search & Select Student")
add_i18n("admin_eval_stat", "선택된 학생", "Selected Student")
add_i18n("admin_eval_empty", "검색 후 선택해주세요", "Search and select")
add_i18n("admin_eval_scores", "항목별 역량 평가 (1~100점)", "Competency Eval (1~100)")
add_i18n("admin_eval_task", "실행력 (Task)", "Execution (Task)")
add_i18n("admin_eval_prof", "전문성 (Prof)", "Professionalism (Prof)")
add_i18n("admin_eval_att", "성실도 (Att)", "Diligence (Att)")
add_i18n("admin_eval_comm", "소통력 (Comm)", "Communication (Comm)")
add_i18n("admin_eval_comment", "정성 평가 코멘트", "Qualitative Comment")
add_i18n("admin_eval_ph", "학생의 이번 주 활동에 대한 칭찬이나 보완점을 적어주세요. (학부모/학생 대시보드에 노출됨)", "Write praises or feedback for the student.")
add_i18n("admin_eval_btn", "🚀 평가 및 피드백 전송", "🚀 Submit Feedback")
add_i18n("admin_chat_sel", "대화 채널 및 대상 선택", "Select Channel & Target")
add_i18n("admin_chat_target", "대화 대상", "Chat Target")
add_i18n("admin_chat_ch", "채널 선택", "Channel Selection")
add_i18n("admin_chat_load", "💬 대화 불러오기", "💬 Load Chat")
add_i18n("admin_chat_send", "전송", "Send")

replacements = {
    # Text > span tag
    '✨ 새로운 프로그램 기획': '<span data-i18n="admin_new_prog_title">✨ 새로운 프로그램 기획</span>',
    '1. 미디어 첨부': '<span data-i18n="admin_new_step1">1. 미디어 첨부</span>',
    '2. 프로그램 기본 정보': '<span data-i18n="admin_new_step2">2. 프로그램 기본 정보</span>',
    '3. 워크플로우 기획': '<span data-i18n="admin_new_step3">3. 워크플로우 기획</span>',
    '유튜브 영상 링크 (옵션)': '<span data-i18n="admin_new_yt">유튜브 영상 링크 (옵션)</span>',
    '포스터 이미지 (1MB 이하 필수)': '<span data-i18n="admin_new_poster">포스터 이미지 (1MB 이하 필수)</span>',
    '클릭하여 이미지 업로드<br>(Drag & Drop 불가)': '<span data-i18n="admin_new_upload">클릭하여 이미지 업로드<br>(Drag & Drop 불가)</span>',
    '프로그램 명': '<span data-i18n="admin_new_pname">프로그램 명</span>',
    '>캘린더 색상<': ' data-i18n="admin_new_color">캘린더 색상<',
    '모집 시작일': '<span data-i18n="admin_new_start">모집 시작일</span>',
    '모집 종료일': '<span data-i18n="admin_new_end">모집 종료일</span>',
    '모집 정원 (명)': '<span data-i18n="admin_new_max">모집 정원 (명)</span>',
    '프로그램 한줄 소개': '<span data-i18n="admin_new_desc">프로그램 한줄 소개</span>',
    '세부 일정 표기 가이드': '<span data-i18n="admin_new_guide">세부 일정 표기 가이드</span>',
    '시간은 빈틈없이 소괄호( ) 안에 적어주세요! (예: 2026-03-23 (14:00) : OT)': '<span data-i18n="admin_new_guide_desc">시간은 빈틈없이 소괄호( ) 안에 적어주세요! (예: 2026-03-23 (14:00) : OT)</span>',
    '✏️ 예시 양식 채우기': '<span data-i18n="admin_new_fill_ex">✏️ 예시 양식 채우기</span>',
    '👨‍👩‍👧‍👦 신규 학부모 계정 연동': '<span data-i18n="admin_parent_title">👨‍👩‍👧‍👦 신규 학부모 계정 연동</span>',
    '학생이 먼저 시스템에 등록되어 있어야 합니다. (수강신청 완료 필수)': '<span data-i18n="admin_parent_desc">학생이 먼저 시스템에 등록되어 있어야 합니다. (수강신청 완료 필수)</span>',
    '학부모 성함': '<span data-i18n="admin_parent_pname">학부모 성함</span>',
    '연동할 자녀 실명': '<span data-i18n="admin_parent_child">연동할 자녀 실명</span>',
    '학부모 로그인 PIN (4자리)': '<span data-i18n="admin_parent_pin">학부모 로그인 PIN (4자리)</span>',
    '🔗 학부모 계정 생성': '<span data-i18n="admin_parent_create">🔗 학부모 계정 생성</span>',
    '📌 대상 프로그램 선택': '<span data-i18n="admin_att_sel_prog">📌 대상 프로그램 선택</span>',
    '📝 일일 출석부': '<span data-i18n="admin_att_tab_daily">📝 일일 출석부</span>',
    '📊 출결 통계': '<span data-i18n="admin_att_tab_stat">📊 출결 통계</span>',
    '⚙️ 출결 수정/삭제': '<span data-i18n="admin_att_tab_edit">⚙️ 출결 수정/삭제</span>',
    '체크할 날짜': '<span data-i18n="admin_att_date">체크할 날짜</span>',
    '💾 일괄 저장 (서버 전송)': '<span data-i18n="admin_att_save">💾 일괄 저장 (서버 전송)</span>',
    '학생 검색 및 선택': '<span data-i18n="admin_eval_sel">학생 검색 및 선택</span>',
    '선택된 학생': '<span data-i18n="admin_eval_stat">선택된 학생</span>',
    '>검색 후 선택해주세요<': ' data-i18n="admin_eval_empty">검색 후 선택해주세요<',
    '항목별 역량 평가 (1~100점)': '<span data-i18n="admin_eval_scores">항목별 역량 평가 (1~100점)</span>',
    '실행력 (Task)': '<span data-i18n="admin_eval_task">실행력 (Task)</span>',
    '전문성 (Prof)': '<span data-i18n="admin_eval_prof">전문성 (Prof)</span>',
    '성실도 (Att)': '<span data-i18n="admin_eval_att">성실도 (Att)</span>',
    '소통력 (Comm)': '<span data-i18n="admin_eval_comm">소통력 (Comm)</span>',
    '정성 평가 코멘트': '<span data-i18n="admin_eval_comment">정성 평가 코멘트</span>',
    '🚀 평가 및 피드백 전송': '<span data-i18n="admin_eval_btn">🚀 평가 및 피드백 전송</span>',
    '대화 채널 및 대상 선택': '<span data-i18n="admin_chat_sel">대화 채널 및 대상 선택</span>',
    '대화 대상': '<span data-i18n="admin_chat_target">대화 대상</span>',
    '채널 선택': '<span data-i18n="admin_chat_ch">채널 선택</span>',
    '💬 대화 불러오기': '<span data-i18n="admin_chat_load">💬 대화 불러오기</span>',
    '전송</button>': '<span data-i18n="admin_chat_send">전송</span></button>',
    
    # Placeholders
    'placeholder="예: 고독한 독서가"': 'placeholder="예: 고독한 독서가" data-i18n-ph="admin_new_pname"',
    'placeholder="실명 입력 (예: 홍길동)"': 'placeholder="실명 입력 (예: 홍길동)" data-i18n-ph="admin_parent_pname"',
    'placeholder="자녀 이름 (예: 홍길준)"': 'placeholder="자녀 이름 (예: 홍길준)" data-i18n-ph="admin_parent_child"',
    'placeholder="비밀번호 설정"': 'placeholder="비밀번호 설정" data-i18n-ph="admin_parent_pin"',
    'placeholder="학생의 이번 주 활동에 대한 칭찬이나 보완점을 적어주세요. (학부모/학생 대시보드에 노출됨)"': 'placeholder="..." data-i18n-ph="admin_eval_ph"'
}

base_dir = "c:/anti/real_project"
filepath = os.path.join(base_dir, "admin.html")

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

for k, v in replacements.items():
    content = content.replace(k, v)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

# Update i18n
i18n_path = os.path.join(base_dir, "i18n.js")
with open(i18n_path, 'r', encoding='utf-8') as f:
    i18n_content = f.read()

ko_keys_str = ""
en_keys_str = ""
for k, v in i18n_keys.items():
    ko_keys_str += f'        "{k}": "{v["ko"]}",\n'
    en_keys_str += f'        "{k}": "{v["en"]}",\n'

ko_anchor = '"download_fail": "저장 실패"'
i18n_content = i18n_content.replace(ko_anchor, ko_anchor + ',\n' + ko_keys_str.rstrip(',\n'))

en_anchor = '"download_fail": "Save Failed"'
i18n_content = i18n_content.replace(en_anchor, en_anchor + ',\n' + en_keys_str.rstrip(',\n'))

with open(i18n_path, 'w', encoding='utf-8') as f:
    f.write(i18n_content)

print("Second translation injection completed!")
