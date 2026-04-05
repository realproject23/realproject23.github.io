import os
import re

html_files = ["dashboard.html", "parents.html", "admin.html"]
i18n_keys = {} # key -> {ko, en}

def add_i18n(key, ko, en):
    i18n_keys[key] = {"ko": ko, "en": en}

# Add all translations
add_i18n("admin_no_pending", "대기 중인 승인 요청이 없습니다.", "No pending approvals.")
add_i18n("admin_chart_dist", "📊 프로그램별 수강생 분포 현황", "📊 Student Distribution by Program")
add_i18n("adv_donut", "🍩 전체출결", "🍩 Total Attendance")
add_i18n("adv_line", "📈 성취도추이", "📈 Achievement Trend")
add_i18n("adv_heat", "🗺️ 출결히트맵", "🗺️ Attendance Heatmap")
add_i18n("adv_scatter", "⚡ 피드백효과", "⚡ Feedback Effect")
add_i18n("adv_stacked", "📊 출결상세", "📊 Attendance Details")
add_i18n("admin_ai_analyzing", "데이터를 분석하는 중입니다...", "Analyzing data...")
add_i18n("admin_bill_student", "대상 학생 이름", "Target Student Name")
add_i18n("admin_bill_fee", "결제 금액 (원)", "Payment Amount (KRW)")
add_i18n("admin_bill_note", "비고 (예: 3월 수강료)", "Note (e.g. March Fee)")
add_i18n("admin_bill_card", "💳 카드결제", "💳 Credit Card")
add_i18n("admin_bill_bank", "🏦 계좌이체", "🏦 Bank Transfer")
add_i18n("admin_bill_cash", "💵 현금", "💵 Cash")
add_i18n("admin_table_loading", "데이터 로딩 중...", "Loading data...")
add_i18n("admin_table_no_data", "일치하는 데이터 없음", "No matching data")
add_i18n("admin_chart_pie", "항목별 매출 구성", "Revenue by Category")
add_i18n("admin_chart_line", "일자별 매출 추이", "Revenue Trend by Date")
add_i18n("admin_filter_name", "🔍 학생명 검색...", "🔍 Search student...")
add_i18n("admin_filter_prog", "📁 전체 프로그램", "📁 All Programs")
add_i18n("admin_filter_role", "🎯 전체 역할", "🎯 All Roles")
add_i18n("admin_role_student", "🎓 수강생", "🎓 Student")
add_i18n("admin_role_parent", "👨‍👩‍👧‍👦 학부모", "👨‍👩‍👧‍👦 Parent")
add_i18n("admin_table_date", "결제일", "Date")
add_i18n("admin_table_name", "학생명", "Student Name")
add_i18n("admin_table_item", "항목", "Item")
add_i18n("admin_table_amount", "금액", "Amount")
add_i18n("admin_table_method", "결제수단", "Method")
add_i18n("admin_table_remark", "비고", "Remark")
add_i18n("admin_table_manage", "관리", "Manage")
add_i18n("admin_table_pname", "참여 프로그램", "Program")
add_i18n("admin_table_prole", "역할(Role)", "Role")
add_i18n("admin_table_name_only", "이름", "Name")
add_i18n("hello_msg", "안녕하세요! 활동하면서 체크리스트와 관련된 질문이 있다면 언제든 편하게 남겨주세요. 😊", "Hello! Feel free to ask any questions regarding the activity checklist anytime. 😊")
add_i18n("dash_loading_prog", "일정을 불러오는 중입니다...", "Loading schedule...")
add_i18n("parent_sel", "자녀를 선택하세요.", "Select a child.")
add_i18n("parent_analyzing2", "데이터를 분석 중입니다...", "Analyzing data...")
add_i18n("chat_no_history", "대화 이력이 없습니다.", "No chat history.")
add_i18n("chat_select", "대상을 선택하고 대화를 불러오세요.", "Select target and load chat.")
add_i18n("admin_pw_cur", "현재 비밀번호", "Current Password")
add_i18n("admin_pw_new", "새 비밀번호", "New Password")
add_i18n("admin_pw_btn", "비밀번호 변경", "Change Password")
add_i18n("admin_edit_student", "👤 학생 정보 수정 / 퇴소", "👤 Edit Student / Expel")
add_i18n("admin_edit_sname", "새 이름 (변경 시)", "New Name (optional)")
add_i18n("admin_edit_spin", "새 PIN (변경 시)", "New PIN (optional)")
add_i18n("admin_edit_btnsave", "💾 정보 수정", "💾 Save Info")
add_i18n("admin_edit_kick", "🗑️ 강제 퇴소", "🗑️ Expel")
add_i18n("admin_dl_title", "📥 다운로드 경로 설정", "📥 Download Path Setting")
add_i18n("admin_dl_desc", "파일(CSV/JSON) 다운로드 시 정보를 저장할 기본 경로를 설정합니다.", "Set the default local path to save downloaded files (CSV/JSON).")
add_i18n("admin_dl_ph", "예: C:\\Users\\Downloads\\YouthCanvas_Data", "e.g., C:\\Downloads")
add_i18n("admin_dl_save", "💾 경로 저장", "💾 Save Path")
add_i18n("admin_dl_success", "✅ 경로가 저장되었습니다. 다음 변경 전까지 유지됩니다.", "✅ Path saved. It will be maintained.")
add_i18n("admin_bk_title", "📦 전체 데이터 백업", "📦 Full Data Backup")
add_i18n("admin_bk_desc", "모든 데이터를 JSON 형식으로 다운로드합니다.", "Download all data in JSON format.")
add_i18n("admin_bk_btn", "📥 JSON 백업 다운로드", "📥 Download JSON Backup")
add_i18n("download_success", "저장 완료", "Save Successful")
add_i18n("download_fail", "저장 실패", "Save Failed")

replacements = {
    # Element replacements (adding data-i18n attribute)
    '>대기 중인 승인 요청이 없습니다.<': '>대기 중인 승인 요청이 없습니다.<', # Handled differently to avoid HTML breakage
    'placeholder="대상 학생 이름"': 'placeholder="대상 학생 이름" data-i18n-ph="admin_bill_student"',
    'placeholder="결제 금액 (원)"': 'placeholder="결제 금액 (원)" data-i18n-ph="admin_bill_fee"',
    'placeholder="비고 (예: 3월 수강료)"': 'placeholder="비고 (예: 3월 수강료)" data-i18n-ph="admin_bill_note"',
    'placeholder="🔍 학생명 검색..."': 'placeholder="🔍 학생명 검색..." data-i18n-ph="admin_filter_name"',
    'placeholder="현재 비밀번호"': 'placeholder="현재 비밀번호" data-i18n-ph="admin_pw_cur"',
    'placeholder="새 비밀번호"': 'placeholder="새 비밀번호" data-i18n-ph="admin_pw_new"',
    'placeholder="새 이름 (변경 시)"': 'placeholder="새 이름 (변경 시)" data-i18n-ph="admin_edit_sname"',
    'placeholder="새 PIN (변경 시)"': 'placeholder="새 PIN (변경 시)" data-i18n-ph="admin_edit_spin"',
    '예: C:\\Users\\Downloads\\YouthCanvas_Data': '예: C:\\\\Users\\\\Downloads',
    
    # Text replacements in HTML
    '프로그램별 수강생 분포 현황': '<span data-i18n="admin_chart_dist">📊 프로그램별 수강생 분포 현황</span>',
    '🍩 전체출결': '<span data-i18n="adv_donut">🍩 전체출결</span>',
    '📈 성취도추이': '<span data-i18n="adv_line">📈 성취도추이</span>',
    '🗺️ 출결히트맵': '<span data-i18n="adv_heat">🗺️ 출결히트맵</span>',
    '⚡ 피드백효과': '<span data-i18n="adv_scatter">⚡ 피드백효과</span>',
    '📊 출결상세': '<span data-i18n="adv_stacked">📊 출결상세</span>',
    '데이터를 분석하는 중입니다...': '<span data-i18n="admin_ai_analyzing">데이터를 분석하는 중입니다...</span>',
    '💳 카드결제': '<span data-i18n="admin_bill_card">💳 카드결제</span>',
    '🏦 계좌이체': '<span data-i18n="admin_bill_bank">🏦 계좌이체</span>',
    '💵 현금': '<span data-i18n="admin_bill_cash">💵 현금</span>',
    '데이터 로딩 중...': '<span data-i18n="admin_table_loading">데이터 로딩 중...</span>',
    '일치하는 데이터 없음': '<span data-i18n="admin_table_no_data">일치하는 데이터 없음</span>',
    '항목별 매출 구성': '<span data-i18n="admin_chart_pie">항목별 매출 구성</span>',
    '일자별 매출 추이': '<span data-i18n="admin_chart_line">일자별 매출 추이</span>',
    '📁 전체 프로그램': '<span data-i18n="admin_filter_prog">📁 전체 프로그램</span>',
    '🎯 전체 역할': '<span data-i18n="admin_filter_role">🎯 전체 역할</span>',
    '🎓 수강생': '<span data-i18n="admin_role_student">🎓 수강생</span>',
    '👨‍👩‍👧‍👦 학부모': '<span data-i18n="admin_role_parent">👨‍👩‍👧‍👦 학부모</span>',
    '<th>결제일</th>': '<th data-i18n="admin_table_date">결제일</th>',
    '<th>학생명</th>': '<th data-i18n="admin_table_name">학생명</th>',
    '<th>항목</th>': '<th data-i18n="admin_table_item">항목</th>',
    '<th>금액</th>': '<th data-i18n="admin_table_amount">금액</th>',
    '<th>결제수단</th>': '<th data-i18n="admin_table_method">결제수단</th>',
    '<th>비고</th>': '<th data-i18n="admin_table_remark">비고</th>',
    '<th>관리</th>': '<th data-i18n="admin_table_manage">관리</th>',
    '<th>이름</th>': '<th data-i18n="admin_table_name_only">이름</th>',
    '<th>참여 프로그램</th>': '<th data-i18n="admin_table_pname">참여 프로그램</th>',
    '<th>역할(Role)</th>': '<th data-i18n="admin_table_prole">역할(Role)</th>',
    '>대화 이력이 없습니다.<': ' data-i18n="chat_no_history">대화 이력이 없습니다.<',
    '>대상을 선택하고 대화를 불러오세요.<': ' data-i18n="chat_select">대상을 선택하고 대화를 불러오세요.<',
    '비밀번호 변경</button>': '<span data-i18n="admin_pw_btn">비밀번호 변경</span></button>',
    '👤 학생 정보 수정 / 퇴소': '<span data-i18n="admin_edit_student">👤 학생 정보 수정 / 퇴소</span>',
    '💾 정보 수정</button>': '<span data-i18n="admin_edit_btnsave">💾 정보 수정</span></button>',
    '🗑️ 강제 퇴소</button>': '<span data-i18n="admin_edit_kick">🗑️ 강제 퇴소</span></button>',
    '📥 다운로드 경로 설정': '<span data-i18n="admin_dl_title">📥 다운로드 경로 설정</span>',
    '파일(CSV/JSON) 다운로드 시 정보를 저장할 기본 경로를 설정합니다.': '<span data-i18n="admin_dl_desc">파일(CSV/JSON) 다운로드 시 정보를 저장할 기본 경로를 설정합니다.</span>',
    '✅ 경로가 저장되었습니다. 다음 변경 전까지 유지됩니다.': '<span data-i18n="admin_dl_success">✅ 경로가 저장되었습니다. 다음 변경 전까지 유지됩니다.</span>',
    '📦 전체 데이터 백업': '<span data-i18n="admin_bk_title">📦 전체 데이터 백업</span>',
    '모든 데이터를 JSON 형식으로 다운로드합니다.': '<span data-i18n="admin_bk_desc">모든 데이터를 JSON 형식으로 다운로드합니다.</span>',
    '📥 JSON 백업 다운로드</button>': '<span data-i18n="admin_bk_btn">📥 JSON 백업 다운로드</span></button>',
    '대기 중인 승인 요청이 없습니다.': '<span data-i18n="admin_no_pending">대기 중인 승인 요청이 없습니다.</span>',
}

base_dir = "c:/anti/real_project"

# Apply replacements to HTML
for file in html_files:
    filepath = os.path.join(base_dir, file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for k, v in replacements.items():
        if k in content:
            if k == 'placeholder="예: C:\\Users\\Downloads\\YouthCanvas_Data"':
                 content = content.replace(k, 'placeholder="예: C:\\Users\\Downloads" data-i18n-ph="admin_dl_ph"')
            else:
                 content = content.replace(k, v)

    # JS string injections
    content = content.replace("'대기 중인 승인 요청이 없습니다.'", "(window.getI18nText ? getI18nText('admin_no_pending') : '대기 중인 승인 요청이 없습니다.')")
    content = content.replace('"안녕하세요! 활동하면서 체크리스트와 관련된 질문이 있다면 언제든 편하게 남겨주세요. 😊"', "(window.getI18nText ? getI18nText('hello_msg') : '안녕하세요! 활동하면서 체크리스트와 관련된 질문이 있다면 언제든 편하게 남겨주세요. 😊')")
    content = content.replace("'일치하는 데이터 없음'", "(window.getI18nText ? getI18nText('admin_table_no_data') : '일치하는 데이터 없음')")
    content = content.replace("'데이터 로딩 중...'", "(window.getI18nText ? getI18nText('admin_table_loading') : '데이터 로딩 중...')")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Update i18n.js
i18n_path = os.path.join(base_dir, "i18n.js")
with open(i18n_path, 'r', encoding='utf-8') as f:
    i18n_content = f.read()

# Add keys to i18n logic
ko_keys_str = ""
en_keys_str = ""
for k, v in i18n_keys.items():
    ko_keys_str += f'        "{k}": "{v["ko"]}",\n'
    en_keys_str += f'        "{k}": "{v["en"]}",\n'

# Inject into ko dictionary
ko_anchor = '"admin_logout": "🔓 로그아웃"'
i18n_content = i18n_content.replace(ko_anchor, ko_anchor + ',\n' + ko_keys_str.rstrip(',\n'))

# Inject into en dictionary
en_anchor = '"admin_logout": "🔓 Logout"'
i18n_content = i18n_content.replace(en_anchor, en_anchor + ',\n' + en_keys_str.rstrip(',\n'))

with open(i18n_path, 'w', encoding='utf-8') as f:
    f.write(i18n_content)

print("Translation update completed!")
