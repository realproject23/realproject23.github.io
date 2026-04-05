import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# --- 페이지 설정 ---
st.set_page_config(
    page_title="Youth Canvas | 시설 통합 관리 시스템",
    page_icon="🛠️",
    layout="wide",
)

# --- 커스텀 CSS (모든 디자인 톤앤매너 통합) ---
st.markdown("""
    <style>
    .main-title { font-family: 'Nanum Square', sans-serif; color: #1A202C; font-weight: 800; font-size: 2.2rem; }
    .admin-badge { background-color: #f1f5f9; color: #475569; padding: 4px 10px; border-radius: 8px; font-size: 0.9rem; font-weight: 600; margin-left: 10px; vertical-align: middle;}
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 15px; background-color: #ffffff; border-radius: 8px 8px 0 0; border: 1px solid #e2e8f0; border-bottom: none; color: #718096;
    }
    .stTabs [aria-selected="true"] { background-color: #f8fafc; border-bottom: 2px solid #ef4444 !important; color: #ef4444 !important; font-weight: bold;}
    
    .finance-card { background-color: white; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; margin-bottom: 20px; }
    .finance-val { font-size: 2.5rem; font-weight: 800; color: #1A202C; }
    .hint-box { background-color: #ebf8ff; color: #2b6cb0; padding: 15px; border-radius: 8px; font-size: 0.9rem; margin-bottom: 15px; border: 1px solid #bee3f8; }
    
    .positive-box { background-color: #f0fff4; border-left: 5px solid #48bb78; padding: 10px 15px; border-radius: 4px; margin-top: 10px; font-size: 0.9rem; color: #276749; }
    .negative-box { background-color: #fff5f5; border-left: 5px solid #f56565; padding: 10px 15px; border-radius: 4px; margin-top: 10px; font-size: 0.9rem; color: #9b2c2c; }
    
    div.stButton > button:first-child { background-color: #ef4444; color: white; border: none; font-weight: bold; border-radius: 8px; }
    div.stDownloadButton > button { background-color: #ffffff; color: #4A5568 !important; border: 1px solid #e2e8f0; font-weight: bold; border-radius: 8px; }
    div.stDownloadButton > button:hover { border-color: #ef4444; color: #ef4444 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 통합 데이터 로드 ---
@st.cache_data
def load_integrated_data():
    # 1. 학생 데이터
    student_data = [
        {"student_id": "YC2601", "name": "김수아", "program": "고독한 독서가", "role": "독서가", "avg_score": 0, "attendance_days": 2, "과제 완료": 5, "출석": 18, "지각": 1, "결석": 0, "소통": 7, "피드백": 12},
        {"student_id": "YC2602", "name": "이해리", "program": "고독한 독서가", "role": "독서가", "avg_score": 0, "attendance_days": 2, "과제 완료": 4, "출석": 15, "지각": 2, "결석": 1, "소통": 3, "피드백": 5},
        {"student_id": "YC2603", "name": "김효정", "program": "내일은 내가 K-POP 스타", "role": "수강생", "avg_score": 6, "attendance_days": 1, "과제 완료": 3, "출석": 12, "지각": 0, "결석": 3, "소통": 2, "피드백": 4},
        {"student_id": "YC2604", "name": "김해리", "program": "내일은 내가 K-POP 스타", "role": "수강생", "avg_score": 0, "attendance_days": 1, "과제 완료": 5, "출석": 20, "지각": 0, "결석": 0, "소통": 8, "피드백": 15},
        {"student_id": "YC2605", "name": "조해리", "program": "봉사활동을 하자", "role": "활동가", "avg_score": 0, "attendance_days": 1, "과제 완료": 2, "출석": 10, "지각": 3, "결석": 2, "소통": 5, "피드백": 8},
        {"student_id": "YC2606", "name": "권해리", "program": "유튜브 크리에이터반", "role": "기획_대본", "avg_score": 0, "attendance_days": 1, "과제 완료": 1, "출석": 5, "지각": 0, "결석": 0, "소통": 1, "피드백": 2},
        {"student_id": "YC2610", "name": "홍승혁", "program": "유튜브 크리에이터반", "role": "기획_대본", "avg_score": 0, "attendance_days": 1, "과제 완료": 2, "출석": 8, "지각": 1, "결석": 0, "소통": 4, "피드백": 6},
    ]
    df_s = pd.DataFrame(student_data)
    df_s['종합 포인트'] = (df_s['과제 완료'] * 15) + (df_s['출석'] * 3)

    # 2. 재무 데이터
    finance_data = [
        {"결제일": "2026-03-17", "학생": "박지민", "프로그램": "내일은 내가 K-POP 스타", "항목": "수강료", "금액": 150000, "결제수단": "카드결제", "비고": "주말특강", "입력담당자": "이지현"},
        {"결제일": "2026-03-18", "학생": "이해리", "프로그램": "고독한 독서가", "항목": "교재비", "금액": 50000, "결제수단": "카드결제", "비고": "청춘의 독서 1권", "입력담당자": "마스터"},
        {"결제일": "2026-03-19", "학생": "김해리", "프로그램": "내일은 내가 K-POP 스타", "항목": "수강료", "금액": 300000, "결제수단": "계좌이체", "비고": "선납금", "입력담당자": "마스터"},
        {"결제일": "2026-03-19", "학생": "김수아", "프로그램": "고독한 독서가", "항목": "수강료", "금액": 200000, "결제수단": "현금", "비고": "현금영수증 발행", "입력담당자": "마스터"},
        {"결제일": "2026-03-20", "학생": "홍승혁", "프로그램": "유튜브 크리에이터반", "항목": "수강료", "금액": 150000, "결제수단": "계좌이체", "비고": "3월분", "입력담당자": "행정팀"},
    ]
    df_f = pd.DataFrame(finance_data)
    df_f['결제일_dt'] = pd.to_datetime(df_f['결제일'])
    
    # 3. [정보 수정 탭 복원용] 프로그램 기존 세팅 데이터
    mock_programs = {
        "내일은 내가 K-POP 스타": {
            "yt_link": "https://youtu.be/blzUaV7TiWE", "has_image": False,
            "color": "#4f46e5", "start_date": datetime(2026, 3, 12), "end_date": datetime(2026, 4, 11),
            "desc": "전문 K-POP 안무가와 함께 최신의 안무를 배운다",
            "workflow": "[수강생 : 10명]\n2026-04-12~2026-04-18 : 1차 강습\n2026-04-19~2026-04-25 : 2차 강습"
        },
        "고독한 독서가": {
            "yt_link": "", "has_image": True,
            "color": "#32CD32", "start_date": datetime(2026, 3, 20), "end_date": datetime(2026, 3, 20),
            "desc": "입시 특강", 
            "workflow": "[수강생 : 10명]\n2026-03-23 (14:00) : OT"
        }
    }
    
    return df_s, df_f, mock_programs

df_students, df_finance, mock_programs = load_integrated_data()

def convert_to_csv(df):
    return df.to_csv(index=False).encode('utf-8-sig')

# --- 헤더 ---
col_head1, col_head2 = st.columns([8, 2])
with col_head1: st.markdown("<span class='main-title'>🛠️ 시설 통합 관리 시스템</span><span class='admin-badge'>[마스터 접속중]</span>", unsafe_allow_html=True)
with col_head2: st.button("🔓 로그아웃", key="logout_btn", use_container_width=True)
st.write("") 

# --- 🚀 모든 탭 생성 ---
tabs = st.tabs(["📈 경영 대시보드", "💳 행정/재무 관리", "📊 종합 명단", "📝 신규 개설", "⚙️ 정보 수정", "✍️ 평가/코멘트 작성", "✅ 출석 관리", "👥 1:1 상담", "👨‍👩‍👧‍👦 학부모 계정", "🎨 화면 설정", "🔒 계정 관리"])

# 1️⃣ [경영 대시보드]
with tabs[0]:
    st.markdown("### 📈 최고관리자 전용 맞춤형 데이터 대시보드")
    st.markdown("<div class='hint-box'>💡 차트 범례를 클릭하여 필터링하고, 카메라 아이콘으로 이미지를 다운로드하세요.</div>", unsafe_allow_html=True)
    
    selected_charts = st.multiselect("📊 표시할 차트 선택:", 
                                     ["막대 (프로그램별 성취도)", "산점도 (피드백 효과)", "도넛 (출결 비율)", "퍼널 (전환율 분석)"],
                                     default=["막대 (프로그램별 성취도)", "산점도 (피드백 효과)"])
    
    if "막대 (프로그램별 성취도)" in selected_charts:
        avg_score = df_students.groupby('program')['종합 포인트'].mean().reset_index()
        fig = px.bar(avg_score, x='program', y='종합 포인트', color='program', text_auto='.1f', title="프로그램별 평균 성취도 비교")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f"""<div class="positive-box">🟢 <b>긍정적 시그널:</b> '{avg_score.iloc[0]['program']}' 프로그램이 가장 우수합니다.</div>""", unsafe_allow_html=True)

    if "산점도 (피드백 효과)" in selected_charts:
        fig_scatter = px.scatter(df_students, x='피드백', y='종합 포인트', color='program', size='출석', hover_name='name', title="선생님 피드백 빈도와 학생 성과 상관관계")
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown("""<div class="positive-box">🟢 <b>긍정적 시그널:</b> 피드백이 많은 학생일수록 성취도가 높습니다.</div>""", unsafe_allow_html=True)

    if "퍼널 (전환율 분석)" in selected_charts:
        fig_f = go.Figure(go.Funnel(y=['모집', '가입', '출석', '수납'], x=[120, 100, 85, 60]))
        fig_f.update_layout(title="비즈니스 전환율 퍼널")
        st.plotly_chart(fig_f, use_container_width=True)
        st.markdown("""<div class="negative-box">🔴 <b>케어 필요:</b> 수납 단계에서의 이탈률이 높습니다. 결제 리마인드 강화가 필요합니다.</div>""", unsafe_allow_html=True)

# 2️⃣ [행정/재무 관리]
with tabs[1]:
    st.markdown("## 💳 행정 및 재무 결제 관리")
    sub1, sub2 = st.tabs(["🧾 결제 내역 입력 및 관리", "📈 재무 통계 및 시각화 리포트"])
    
    with sub1:
        st.markdown("#### ➕ 신규 결제 내역 추가")
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            c1.date_input("결제일자")
            c2.selectbox("대상 학생", df_students['name'].unique())
            c3.selectbox("결제 항목", ["수강료", "교재비", "특강비"])
            c4, c5, c6 = st.columns(3)
            c4.number_input("결제 금액 (원)", min_value=0, step=10000)
            c5.selectbox("결제수단", ["카드결제", "계좌이체", "현금"])
            c6.text_input("비고")
            st.button("💾 결제 내역 저장")
        
        st.markdown("#### 📋 통합 결제 내역 데이터베이스")
        with st.container(border=True):
            search_q = st.text_input("🔍 검색어 입력 (학생명, 프로그램명, 비고, 금액 등)")
            f1, f2, f3, f4 = st.columns(4)
            sel_student = f1.selectbox("학생별", ["전체"] + list(df_finance['학생'].unique()))
            sel_program = f2.selectbox("프로그램별", ["전체"] + list(df_finance['프로그램'].unique()))
            sel_category = f3.selectbox("항목별", ["전체"] + list(df_finance['항목'].unique()))
            sel_method = f4.selectbox("결제수단별", ["전체"] + list(df_finance['결제수단'].unique()))
            
        df_f_filtered = df_finance.copy()
        if sel_student != "전체": df_f_filtered = df_f_filtered[df_f_filtered['학생'] == sel_student]
        if sel_program != "전체": df_f_filtered = df_f_filtered[df_f_filtered['프로그램'] == sel_program]
        if sel_category != "전체": df_f_filtered = df_f_filtered[df_f_filtered['항목'] == sel_category]
        if sel_method != "전체": df_f_filtered = df_f_filtered[df_f_filtered['결제수단'] == sel_method]
        if search_q:
            df_f_filtered = df_f_filtered[df_f_filtered.apply(lambda r: r.astype(str).str.contains(search_q).any(), axis=1)]
        
        df_display_f = df_f_filtered.drop(columns=['결제일_dt']).copy()
        df_display_f['금액'] = df_display_f['금액'].apply(lambda x: f"{x:,} 원")
        
        col_btn1, col_btn2 = st.columns([3, 7])
        with col_btn1:
            st.download_button("📥 전체 결제 내역 엑셀(CSV) 다운로드", convert_to_csv(df_display_f), "finance_report.csv")
        st.dataframe(df_display_f, use_container_width=True, hide_index=True)
        
        with st.expander("🗑️ 잘못 입력된 결제 내역 삭제"):
            st.selectbox("삭제할 내역 선택", df_display_f['학생'] + " - " + df_display_f['금액'])
            st.button("내역 삭제 실행", type="secondary")

    with sub2:
        st.markdown("### 📈 기관 전체 재무 상태 및 매출 분석")
        total_won = df_finance['금액'].sum()
        st.markdown(f'<div class="finance-card"><p style="margin:0; font-size:0.9rem; color:#718096; font-weight:bold;">💰 누적 총 매출 금액</p><p class="finance-val">{total_won:,} 원</p></div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("##### 🍰 항목별 매출 구성 비율")
            item_sum = df_finance.groupby('항목')['금액'].sum().reset_index()
            st.plotly_chart(px.pie(item_sum, values='금액', names='항목', hole=0.5), use_container_width=True)
            st.markdown("""<div class="positive-box">🟢 <b>긍정적 시그널:</b> '수강료' 항목이 전체 매출을 견인하고 있습니다.</div>""", unsafe_allow_html=True)
        with col_b:
            st.markdown("##### 📊 일자별 매출 추이")
            date_sum = df_finance.groupby('결제일')['금액'].sum().reset_index()
            st.plotly_chart(px.bar(date_sum, x='결제일', y='금액', text_auto=','), use_container_width=True)
            st.markdown("""<div class="negative-box">ℹ️ 일자별 수입 변동성을 확인하세요. 특정 일자에 매출이 집중됩니다.</div>""", unsafe_allow_html=True)

# 3️⃣ [종합 명단]
with tabs[2]:
    st.markdown("### 📊 데이터 필터링 및 엑셀 추출")
    col_s1, col_s2, col_s3 = st.columns(3)
    search_s = col_s1.text_input("🔍 학생명 검색")
    prog_f = col_s2.selectbox("📁 프로그램 필터", ["전체"] + list(df_students['program'].unique()))
    role_f = col_s3.selectbox("🎯 역할 필터", ["전체"] + list(df_students['role'].unique()))
    
    df_s_filtered = df_students.copy()
    if search_s: df_s_filtered = df_s_filtered[df_s_filtered['name'].str.contains(search_s)]
    if prog_f != "전체": df_s_filtered = df_s_filtered[df_s_filtered['program'] == prog_f]
    if role_f != "전체": df_s_filtered = df_s_filtered[df_s_filtered['role'] == role_f]
    
    df_display_s = df_s_filtered[['name', 'program', 'role', 'avg_score', 'attendance_days']].copy()
    df_display_s.columns = ['학생명', '프로그램', '역할', '평균성취도(점)', '총 출석(일)']
    
    st.markdown(f"<p style='font-size:0.9rem; color:#475569;'>총 <b>{len(df_display_s)}</b>명의 데이터가 조회되었습니다.</p>", unsafe_allow_html=True)
    st.dataframe(df_display_s, use_container_width=True, hide_index=True)
    st.download_button("📥 전체 명단 엑셀(CSV) 다운로드", convert_to_csv(df_display_s), "student_list.csv")

# 4️⃣ [신규 개설]
with tabs[3]:
    st.markdown("### ➕ 신규 프로그램 개설")
    with st.container(border=True):
        st.markdown("#### 🎬 1. 미디어 첨부 (선택)")
        st.warning("🚨 **[필독] 동영상 직접 업로드의 한계 및 대안**\n\n유튜브에 영상을 '일부 공개'로 올리신 후 **[유튜브 링크]**란에 붙여넣는 것이 가장 안전합니다.")
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.text_input("📺 유튜브 링크 (가장 안전)", placeholder="https://youtu.be/...")
        c_m2.file_uploader("🖼️ 이미지 (1MB 이하 필수)", type=['png', 'jpg'])
        c_m3.file_uploader("🎥 동영상 (업로드 차단됨)", disabled=True)
        
        st.markdown("#### 📝 2. 프로그램 기본 정보")
        c_i1, c_i2 = st.columns([8, 1])
        c_i1.text_input("프로그램 명")
        c_i2.color_picker("색상", "#4f46e5")
        c_d1, c_d2 = st.columns(2)
        c_d1.date_input("시작일")
        c_d2.date_input("종료일")
        st.text_area("소개")
        
        st.markdown("#### 🗓️ 3. 워크플로우 (시간 및 일정)")
        st.info("💡 **시간은 반드시 소괄호 ( ) 안에 적어주세요!** (예: 2026-03-23 (14:00) : OT)")
        st.text_area("워크플로우 양식", value="[수강생 : 10명]\n2026-03-23 (14:00~16:00) : 1차 특강\n2026-03-30 (17:30~19:30) : 2차 특강\n- 세부 목표 (하이픈으로 시작)", height=150)
        st.markdown('<div style="text-align: right;"><button style="border: none; padding: 12px 24px; cursor: pointer; font-weight:bold; color:white; background-color:#ef4444; border-radius:8px;">✨ 최종 개설하기</button></div>', unsafe_allow_html=True)

# 5️⃣ [정보 수정] - 스크린샷 1, 2 완벽 복원 (미디어 다이나믹 렌더링, 워크플로우 포함)
with tabs[4]:
    st.markdown("### ⚙️ 기존 프로그램 정보 수정")
    with st.container(border=True):
        # 1. 프로그램 선택
        prog_names = list(mock_programs.keys())
        selected_prog_to_edit = st.selectbox("⚙️ 수정할 프로그램 선택", prog_names)
        prog_info = mock_programs[selected_prog_to_edit]
        
        # 2. 미디어 첨부 수정 (동적 렌더링)
        st.markdown("#### 🎬 1. 미디어 첨부 수정")
        if prog_info['yt_link']:
            st.success(f"✅ 현재 등록된 링크: {prog_info['yt_link']}")
        elif prog_info['has_image']:
            st.success("✅ 현재 이미지가 등록되어 있습니다.")
        else:
            st.info("등록된 미디어가 없습니다.")
            
        c_e1, c_e2, c_e3 = st.columns(3)
        c_e1.text_input("📺 새 유튜브 링크", value=prog_info['yt_link'], key="edit_yt")
        c_e2.file_uploader("🖼️ 새 이미지 (1MB 이하 필수)", type=['png', 'jpg', 'jpeg'], key="edit_img")
        c_e3.file_uploader("🎥 새 동영상 (업로드 차단됨)", disabled=True, key="edit_vid")
        
        st.checkbox("🗑️ 등록된 미디어 완전히 삭제하기 (서버 에러 400 발생 시 체크 필수!)")
        st.write("---")
        
        # 3. 프로그램 기본 정보 수정
        st.markdown("#### 📝 2. 프로그램 기본 정보 수정")
        c_b1, c_b2 = st.columns([8, 1])
        c_b1.text_input("프로그램 명", value=selected_prog_to_edit, key="edit_prog_name")
        c_b2.color_picker("캘린더 색상 변경", prog_info['color'], key="edit_color")
        
        c_d3, c_d4 = st.columns(2)
        c_d3.date_input("모집 시작일 수정", value=prog_info['start_date'], key="edit_start_date")
        c_d4.date_input("모집 종료일 수정", value=prog_info['end_date'], key="edit_end_date")
        
        st.text_area("상세 내용", value=prog_info['desc'], key="edit_desc")
        
        # 4. 워크플로우 수정 (스크린샷 2 하단 복원)
        st.markdown("#### 🗓️ 3. 워크플로우 수정")
        st.info("💡 **시간은 반드시 소괄호 ( ) 안에 적어주세요!** (예: 2026-03-23 (14:00) : OT)")
        st.text_area("워크플로우 수정", value=prog_info['workflow'], height=150, key="edit_wf")
        
        st.markdown('<div style="text-align: right;"><button style="border: none; padding: 12px 24px; cursor: pointer; font-weight:bold; color:white; background-color:#ef4444; border-radius:8px;">정보 수정 완료</button></div>', unsafe_allow_html=True)

# 9️⃣ [학부모 계정]
with tabs[8]:
    st.markdown("### 👨‍👩‍👧‍👦 학부모 통합 CRM")
    with st.container(border=True):
        c_p1, c_p2 = st.columns(2)
        c_p1.text_input("학부모 대표 이름")
        c_p2.text_input("비밀번호 (4자리)", type="password")
        st.selectbox("연결할 학생 선택", ["Choose options"]) 
        st.button("새로운 계정 생성")
    st.markdown("---")
    st.markdown("""
        <p style='margin:0;'><span style='font-size: 1.2rem;'>👨‍👩‍👧‍👦</span> <b>김해리 어머니</b></p>
        <p style='margin:0; margin-bottom: 15px; color: #475569; font-size: 0.95rem;'><b>연결된 자녀:</b> 김해리, 김수아</p>
        <p style='margin:0;'><span style='font-size: 1.2rem;'>👨‍👩‍👧‍👦</span> <b>김수아 어머니</b></p>
        <p style='margin:0; margin-bottom: 15px; color: #475569; font-size: 0.95rem;'><b>연결된 자녀:</b> 김수아, 김해리</p>
    """, unsafe_allow_html=True)

# --- 나머지 미구현 탭 ---
tab_names = {5: "✍️ 평가/코멘트 작성", 6: "✅ 출석 관리", 7: "👥 1:1 상담", 9: "🎨 화면 설정", 10: "🔒 계정 관리"}
for i, name in tab_names.items():
    with tabs[i]:
        st.info(f"{name} 화면입니다. 세부 내용은 향후 운영 데이터에 따라 활성화됩니다.")