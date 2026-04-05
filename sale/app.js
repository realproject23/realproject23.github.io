// ─────────────────────────────────────────────
// app.js — 메인 앱 로직
// ─────────────────────────────────────────────

// 상태 관리
const state = {
  currentPage: 'browse',
  calYear: new Date().getFullYear(),
  calMonth: new Date().getMonth() + 1,
  studentLoggedIn: null,
  parentLoggedIn: null,
  adminLoggedIn: null,
  adminTab: 'dashboard',
  theme: localStorage.getItem('yc-theme') || 'warm'
};

// ────────────────────────────
// 초기화
// ────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initThemeSwitcher();
  initTabbar();
  initPages();
  initLoginSelects();
  initLoginButtons();
  initCalendarNav();
  renderBrowse();
  renderCalendar();

  // 데모 배너
  const banner = document.getElementById('demo-banner');
  if (banner && CONFIG.demoMode) banner.textContent = CONFIG.demoNotice;
});

// ────────────────────────────
// 테마 스위처
// ────────────────────────────
function initThemeSwitcher() {
  applyTheme(state.theme);
  const dots = document.querySelectorAll('.theme-dot');
  dots.forEach(dot => {
    dot.addEventListener('click', () => {
      const theme = dot.dataset.theme;
      state.theme = theme;
      localStorage.setItem('yc-theme', theme);
      applyTheme(theme);
      dots.forEach(d => d.classList.remove('active'));
      dot.classList.add('active');
    });
  });
}

function applyTheme(theme) {
  const body = document.body;
  body.classList.remove('theme-warm', 'theme-mono', 'theme-mint');
  body.classList.add('theme-' + theme);
  // 활성 dot 업데이트
  document.querySelectorAll('.theme-dot').forEach(d => {
    d.classList.toggle('active', d.dataset.theme === theme);
  });
}

// ────────────────────────────
// 탭바 생성
// ────────────────────────────
function initTabbar() {
  const tabbar = document.getElementById('tabbar');
  CONFIG.menus.forEach(menu => {
    const btn = createEl('button', 'tab-item' + (menu.id === 'browse' ? ' active' : ''));
    btn.dataset.page = menu.id;
    const icon = createEl('span', 'tab-icon', menu.icon);
    const label = createEl('span', 'tab-label', menu.label);
    btn.appendChild(icon);
    btn.appendChild(label);
    btn.addEventListener('click', () => switchPage(menu.id));
    tabbar.appendChild(btn);
  });
}

function switchPage(pageId) {
  state.currentPage = pageId;
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-item').forEach(t => t.classList.remove('active'));
  const page = document.getElementById('page-' + pageId);
  if (page) page.classList.add('active');
  const tab = document.querySelector(`.tab-item[data-page="${pageId}"]`);
  if (tab) tab.classList.add('active');

  // 페이지 제목 변경
  const titles = { browse: '찾아보기', calendar: '전체 일정', student: '나의 이야기', parent: '학부모 라운지', admin: '관리자' };
  document.getElementById('header-title').textContent = titles[pageId] || CONFIG.brand;
}

// ────────────────────────────
// 로그인 셀렉트 초기화
// ────────────────────────────
function initPages() {}

function initLoginSelects() {
  // 학생 셀렉트
  const studentSel = document.getElementById('student-select');
  APP_DATA.users.forEach(u => {
    const opt = createEl('option', '', u.name + ' (' + u.program + ')');
    opt.value = u.name;
    studentSel.appendChild(opt);
  });

  // 학부모 셀렉트
  const parentSel = document.getElementById('parent-select');
  APP_DATA.parents.forEach(p => {
    const opt = createEl('option', '', p.name);
    opt.value = p.name;
    parentSel.appendChild(opt);
  });

  // 관리자 셀렉트
  const adminSel = document.getElementById('admin-select');
  APP_DATA.admins.forEach(a => {
    const roleLabel = a.role === 'super' ? '👑 시설장' : a.role === 'staff' ? '📋 행정' : '📝 선생님';
    const opt = createEl('option', '', a.name + ' [' + roleLabel + ']');
    opt.value = a.name;
    adminSel.appendChild(opt);
  });
}

function initLoginButtons() {
  document.getElementById('student-login-btn').addEventListener('click', () => {
    const name = document.getElementById('student-select').value;
    const user = APP_DATA.users.find(u => u.name === name);
    if (user) {
      state.studentLoggedIn = user;
      document.getElementById('student-login').style.display = 'none';
      document.getElementById('student-dashboard').style.display = 'block';
      renderStudentDashboard(user);
    }
  });

  document.getElementById('parent-login-btn').addEventListener('click', () => {
    const name = document.getElementById('parent-select').value;
    const parent = APP_DATA.parents.find(p => p.name === name);
    if (parent) {
      state.parentLoggedIn = parent;
      document.getElementById('parent-login').style.display = 'none';
      document.getElementById('parent-dashboard').style.display = 'block';
      renderParentDashboard(parent);
    }
  });

  document.getElementById('admin-login-btn').addEventListener('click', () => {
    const name = document.getElementById('admin-select').value;
    const admin = APP_DATA.admins.find(a => a.name === name);
    if (admin) {
      state.adminLoggedIn = admin;
      document.getElementById('admin-login').style.display = 'none';
      document.getElementById('admin-dashboard').style.display = 'block';
      renderAdminDashboard(admin);
    }
  });
}

// ────────────────────────────
// 찾아보기 페이지
// ────────────────────────────
function renderBrowse() {
  const list = document.getElementById('program-list');
  list.innerHTML = '';

  APP_DATA.programs.forEach(prog => {
    const card = createEl('div', 'neu-card program-card');
    const colorBar = createEl('div', 'program-color-bar');
    colorBar.style.background = prog.color;
    card.appendChild(colorBar);

    const title = createEl('div', 'program-title', prog.title);
    card.appendChild(title);

    const desc = createEl('div', 'program-desc', prog.desc);
    card.appendChild(desc);

    const meta = createEl('div', 'program-meta');
    const status = getRecruitStatus(prog.recruit_start, prog.recruit_end);
    const badge = createEl('span', 'badge ' + status.cls, status.text);
    meta.appendChild(badge);

    // 수용 인원
    Object.keys(prog.roles_capacity).forEach(role => {
      const enrolled = APP_DATA.users.filter(u => u.program === prog.title).length;
      const cap = createEl('span', 'meta-item', '👥 ' + enrolled + '/' + prog.roles_capacity[role] + '명');
      meta.appendChild(cap);
    });

    // 기간
    const period = createEl('span', 'meta-item', '📆 ' + prog.recruit_start + ' ~ ' + prog.recruit_end);
    meta.appendChild(period);
    card.appendChild(meta);

    // 진행률 바
    const roleKeys = Object.keys(prog.roles_workflow);
    if (roleKeys.length > 0) {
      const wf = prog.roles_workflow[roleKeys[0]];
      const progress = getProgress(wf);
      const progContainer = createEl('div', 'progress-bar-container mt-12');
      const progFill = createEl('div', 'progress-bar-fill');
      progFill.style.width = progress + '%';
      progContainer.appendChild(progFill);
      card.appendChild(progContainer);

      const progLabel = createEl('div', 'meta-item', '진행률 ' + progress + '%');
      card.appendChild(progLabel);
    }

    // 커리큘럼 아코디언
    if (roleKeys.length > 0) {
      const accHeader = createEl('div', 'accordion-header mt-12');
      accHeader.innerHTML = '<span style="font-size:0.8rem; font-weight:500;">📝 커리큘럼 보기</span><span class="chevron">▶</span>';
      card.appendChild(accHeader);

      const accBody = createEl('div', 'accordion-body');
      roleKeys.forEach(role => {
        prog.roles_workflow[role].forEach(item => {
          const wfItem = createEl('div', 'workflow-item');
          const check = createEl('div', 'workflow-check' + (item.done ? ' done' : ''), item.done ? '✓' : '');
          const info = createEl('div', 'workflow-info');
          const task = createEl('div', 'workflow-task', item.task);
          const date = createEl('div', 'workflow-date', item.start_date + (item.time ? ' (' + item.time + ')' : ''));
          info.appendChild(task);
          info.appendChild(date);
          if (item.score > 0) {
            const score = createEl('div', 'workflow-score', '⭐ ' + item.score + '점');
            info.appendChild(score);
          }
          wfItem.appendChild(check);
          wfItem.appendChild(info);
          accBody.appendChild(wfItem);
        });
      });
      card.appendChild(accBody);

      accHeader.addEventListener('click', () => {
        accHeader.classList.toggle('open');
        accBody.classList.toggle('open');
      });
    }

    // 신청 버튼
    const applyBtn = createEl('button', 'neu-btn neu-btn-primary neu-btn-block mt-12', '✨ 수강 신청하기');
    applyBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      showToast('데모 모드에서는 신청이 제한됩니다.', 'warning');
    });
    card.appendChild(applyBtn);

    list.appendChild(card);
  });
}

// ────────────────────────────
// 캘린더 페이지
// ────────────────────────────
function initCalendarNav() {
  document.getElementById('cal-prev').addEventListener('click', () => {
    state.calMonth--;
    if (state.calMonth < 1) { state.calMonth = 12; state.calYear--; }
    renderCalendar();
  });
  document.getElementById('cal-next').addEventListener('click', () => {
    state.calMonth++;
    if (state.calMonth > 12) { state.calMonth = 1; state.calYear++; }
    renderCalendar();
  });
}

function renderCalendar() {
  const title = document.getElementById('cal-title');
  title.textContent = state.calYear + '년 ' + state.calMonth + '월';

  const grid = document.getElementById('calendar-grid');
  grid.innerHTML = '';

  // 요일 헤더
  const dayNames = ['일', '월', '화', '수', '목', '금', '토'];
  dayNames.forEach(d => {
    grid.appendChild(createEl('div', 'calendar-day-header', d));
  });

  const daysInMonth = getDaysInMonth(state.calYear, state.calMonth);
  const firstDay = getFirstDayOfMonth(state.calYear, state.calMonth);
  const today = getToday();

  // 이벤트 날짜 수집
  const eventDates = new Set();
  APP_DATA.programs.forEach(prog => {
    Object.values(prog.roles_workflow).forEach(wfList => {
      wfList.forEach(item => {
        if (item.start_date) {
          const d = parseDate(item.start_date);
          if (d.year === state.calYear && d.month === state.calMonth) {
            eventDates.add(d.day);
          }
        }
      });
    });
  });

  // 빈 셀
  for (let i = 0; i < firstDay; i++) {
    grid.appendChild(createEl('div', 'calendar-cell empty'));
  }

  // 날짜 셀
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = state.calYear + '-' + String(state.calMonth).padStart(2, '0') + '-' + String(d).padStart(2, '0');
    let cls = 'calendar-cell';
    if (dateStr === today) cls += ' today';
    if (eventDates.has(d)) cls += ' has-event';

    const cell = createEl('div', cls, String(d));
    cell.addEventListener('click', () => showDayEvents(dateStr));
    grid.appendChild(cell);
  }

  // 이벤트 목록
  renderCalendarEvents();
}

function renderCalendarEvents() {
  const container = document.getElementById('calendar-events');
  container.innerHTML = '';
  const monthStr = state.calYear + '-' + String(state.calMonth).padStart(2, '0');
  let hasEvents = false;

  APP_DATA.programs.forEach(prog => {
    Object.values(prog.roles_workflow).forEach(wfList => {
      wfList.forEach(item => {
        if (item.start_date && item.start_date.startsWith(monthStr)) {
          hasEvents = true;
          const card = createEl('div', 'neu-card-flat');
          const row = createEl('div', 'flex-between');
          const left = createEl('div', '');
          const title = createEl('div', 'workflow-task', prog.title + ' — ' + item.task);
          const date = createEl('div', 'workflow-date', item.start_date + (item.time ? ' ' + item.time : ''));
          left.appendChild(title);
          left.appendChild(date);
          row.appendChild(left);

          const colorDot = createEl('div', '');
          colorDot.style.cssText = 'width:10px;height:10px;border-radius:50%;background:' + prog.color;
          row.appendChild(colorDot);

          card.appendChild(row);
          container.appendChild(card);
        }
      });
    });
  });

  if (!hasEvents) {
    container.appendChild(createEl('div', 'text-center section-subtitle mt-16', '이번 달에는 예정된 일정이 없습니다.'));
  }
}

function showDayEvents(dateStr) {
  const events = [];
  APP_DATA.programs.forEach(prog => {
    Object.values(prog.roles_workflow).forEach(wfList => {
      wfList.forEach(item => {
        if (item.start_date === dateStr) {
          events.push({ program: prog.title, task: item.task, time: item.time, color: prog.color });
        }
      });
    });
  });

  if (events.length === 0) return;

  const overlay = document.getElementById('popup-overlay');
  const content = document.getElementById('popup-content');
  content.innerHTML = '';

  const title = createEl('div', 'popup-title', '📅 ' + dateStr + ' 일정');
  content.appendChild(title);

  events.forEach(ev => {
    const item = createEl('div', 'neu-card-flat');
    const row = createEl('div', 'flex gap-8');
    const dot = createEl('span', '');
    dot.style.cssText = 'display:inline-block;width:8px;height:8px;border-radius:50%;background:' + ev.color + ';margin-top:5px;flex-shrink:0;';
    const info = createEl('div', '');
    info.appendChild(createEl('div', 'workflow-task', ev.program));
    info.appendChild(createEl('div', 'workflow-date', ev.task + (ev.time ? ' (' + ev.time + ')' : '')));
    row.appendChild(dot);
    row.appendChild(info);
    item.appendChild(row);
    content.appendChild(item);
  });

  const closeBtn = createEl('button', 'neu-btn neu-btn-block mt-12', '닫기');
  closeBtn.addEventListener('click', () => overlay.classList.remove('show'));
  content.appendChild(closeBtn);

  overlay.classList.add('show');
  overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.classList.remove('show'); });
}

// ────────────────────────────
// 학생 대시보드
// ────────────────────────────
function renderStudentDashboard(user) {
  const container = document.getElementById('student-dashboard');
  container.innerHTML = '';

  // 헤더
  const header = createEl('div', 'flex-between mb-16');
  header.appendChild(createEl('div', 'section-title', '📖 ' + user.name + '님의 이야기'));
  const logoutBtn = createEl('button', 'neu-btn neu-btn-sm', '🔓 로그아웃');
  logoutBtn.addEventListener('click', () => {
    state.studentLoggedIn = null;
    container.style.display = 'none';
    document.getElementById('student-login').style.display = 'block';
  });
  header.appendChild(logoutBtn);
  container.appendChild(header);

  // 프로그램 정보
  const prog = APP_DATA.programs.find(p => p.title === user.program);
  if (!prog) {
    container.appendChild(createEl('div', 'alert alert-warning', '등록된 프로그램이 없습니다.'));
    return;
  }

  const progCard = createEl('div', 'neu-card');
  progCard.appendChild(createEl('div', 'program-title', user.program));

  // 출결 통계
  const attCounts = { 출석: 0, 지각: 0, 결석: 0, 병결: 0 };
  Object.values(user.attendance).forEach(status => {
    if (attCounts.hasOwnProperty(status)) attCounts[status]++;
  });

  const statGrid = createEl('div', 'stat-grid');
  Object.entries(attCounts).forEach(([label, count]) => {
    const stat = createEl('div', 'neu-card-flat stat-card');
    stat.appendChild(createEl('div', 'stat-value', String(count)));
    stat.appendChild(createEl('div', 'stat-label', label));
    statGrid.appendChild(stat);
  });
  progCard.appendChild(statGrid);

  // 출결 뱃지
  const attList = createEl('div', 'att-list');
  Object.entries(user.attendance).forEach(([date, status]) => {
    const color = CONFIG.attendanceColors[status] || '#888';
    const badge = createEl('span', 'att-badge');
    badge.textContent = date.slice(5) + ' ' + status;
    badge.style.background = color;
    badge.style.color = '#fff';
    attList.appendChild(badge);
  });
  if (Object.keys(user.attendance).length > 0) {
    progCard.appendChild(createEl('div', 'mb-8', ''));
    progCard.appendChild(createEl('div', 'form-label', '출결 기록'));
    progCard.appendChild(attList);
  }
  container.appendChild(progCard);

  // 워크플로우 체크리스트
  const wfCard = createEl('div', 'neu-card');
  wfCard.appendChild(createEl('div', 'section-title', '📝 나의 체크리스트'));

  const roleKeys = Object.keys(prog.roles_workflow);
  if (roleKeys.length > 0) {
    const progress = getProgress(prog.roles_workflow[roleKeys[0]]);
    const progBar = createEl('div', 'progress-bar-container');
    const progFill = createEl('div', 'progress-bar-fill');
    progFill.style.width = progress + '%';
    progBar.appendChild(progFill);
    wfCard.appendChild(progBar);
    wfCard.appendChild(createEl('div', 'meta-item mb-12', '진행률 ' + progress + '%'));

    prog.roles_workflow[roleKeys[0]].forEach(item => {
      const wfItem = createEl('div', 'workflow-item');
      const check = createEl('div', 'workflow-check' + (item.done ? ' done' : ''), item.done ? '✓' : '');
      check.addEventListener('click', () => {
        showToast('데모 모드에서는 변경할 수 없습니다.');
      });
      const info = createEl('div', 'workflow-info');
      info.appendChild(createEl('div', 'workflow-task', item.task));
      info.appendChild(createEl('div', 'workflow-date', item.start_date + (item.time ? ' (' + item.time + ')' : '')));
      if (item.score > 0) info.appendChild(createEl('div', 'workflow-score', '⭐ ' + item.score + '점'));
      if (item.comment) info.appendChild(createEl('div', 'workflow-date', '💬 ' + item.comment));
      // 서브태스크
      if (item.subtasks && item.subtasks.length > 0) {
        item.subtasks.forEach(st => {
          const sub = createEl('div', 'workflow-date', (st.done ? '✅' : '⬜') + ' ' + st.desc);
          info.appendChild(sub);
        });
      }
      wfItem.appendChild(check);
      wfItem.appendChild(info);
      wfCard.appendChild(wfItem);
    });
  }
  container.appendChild(wfCard);
}

// ────────────────────────────
// 학부모 대시보드
// ────────────────────────────
function renderParentDashboard(parent) {
  const container = document.getElementById('parent-dashboard');
  container.innerHTML = '';

  const header = createEl('div', 'flex-between mb-16');
  header.appendChild(createEl('div', 'section-title', '👨‍👩‍👧 ' + parent.name + '님'));
  const logoutBtn = createEl('button', 'neu-btn neu-btn-sm', '🔓 로그아웃');
  logoutBtn.addEventListener('click', () => {
    state.parentLoggedIn = null;
    container.style.display = 'none';
    document.getElementById('parent-login').style.display = 'block';
  });
  header.appendChild(logoutBtn);
  container.appendChild(header);

  // 자녀 정보
  parent.children.forEach(childName => {
    const user = APP_DATA.users.find(u => u.name === childName);
    if (!user) return;

    const card = createEl('div', 'neu-card');
    card.appendChild(createEl('div', 'program-title', '👧 ' + user.name));
    card.appendChild(createEl('div', 'program-desc', '프로그램: ' + user.program));

    // 출결
    const attCounts = { 출석: 0, 지각: 0, 결석: 0, 병결: 0 };
    Object.values(user.attendance).forEach(status => {
      if (attCounts.hasOwnProperty(status)) attCounts[status]++;
    });

    const statGrid = createEl('div', 'stat-grid');
    Object.entries(attCounts).forEach(([label, count]) => {
      const stat = createEl('div', 'neu-card-flat stat-card');
      stat.appendChild(createEl('div', 'stat-value', String(count)));
      stat.appendChild(createEl('div', 'stat-label', label));
      statGrid.appendChild(stat);
    });
    card.appendChild(statGrid);

    // 프로그램 진척도
    const prog = APP_DATA.programs.find(p => p.title === user.program);
    if (prog) {
      const roleKeys = Object.keys(prog.roles_workflow);
      if (roleKeys.length > 0) {
        const progress = getProgress(prog.roles_workflow[roleKeys[0]]);
        const progBar = createEl('div', 'progress-bar-container');
        const progFill = createEl('div', 'progress-bar-fill');
        progFill.style.width = progress + '%';
        progBar.appendChild(progFill);
        card.appendChild(createEl('div', 'form-label', '진행률'));
        card.appendChild(progBar);
        card.appendChild(createEl('div', 'meta-item', progress + '% 완료'));
      }
    }

    container.appendChild(card);
  });
}

// ────────────────────────────
// 관리자 대시보드
// ────────────────────────────
function renderAdminDashboard(admin) {
  const container = document.getElementById('admin-dashboard');
  container.innerHTML = '';

  // 헤더
  const header = createEl('div', 'flex-between mb-12');
  const isSuper = admin.role === 'super';
  const roleLabel = isSuper ? '시설장' : admin.role === 'staff' ? '행정담당자' : '선생님';
  header.appendChild(createEl('div', 'section-title', '🛠️ 통합 관리 시스템'));
  const headerRight = createEl('div', 'flex gap-8');
  headerRight.appendChild(createEl('span', 'badge badge-info', roleLabel + ' ' + admin.name));
  const logoutBtn = createEl('button', 'neu-btn neu-btn-sm', '🔓');
  logoutBtn.addEventListener('click', () => {
    state.adminLoggedIn = null;
    container.style.display = 'none';
    document.getElementById('admin-login').style.display = 'block';
  });
  headerRight.appendChild(logoutBtn);
  header.appendChild(headerRight);
  container.appendChild(header);

  // 탭
  const tabs = [
    { id: 'dashboard', label: '📈 대시보드' },
    { id: 'finance', label: '💳 재무' },
    { id: 'roster', label: '📊 명단' },
    { id: 'attendance', label: '✅ 출석' },
    { id: 'eval', label: '📝 평가' }
  ];

  const tabBar = createEl('div', 'admin-tabs');
  tabs.forEach(tab => {
    const btn = createEl('button', 'admin-tab' + (tab.id === 'dashboard' ? ' active' : ''), tab.label);
    btn.dataset.tab = tab.id;
    btn.addEventListener('click', () => {
      tabBar.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('active'));
      btn.classList.add('active');
      container.querySelectorAll('.admin-panel').forEach(p => p.classList.remove('active'));
      const panel = document.getElementById('admin-panel-' + tab.id);
      if (panel) panel.classList.add('active');
    });
    tabBar.appendChild(btn);
  });
  container.appendChild(tabBar);

  // 패널: 대시보드
  const dashPanel = createEl('div', 'admin-panel active');
  dashPanel.id = 'admin-panel-dashboard';
  const myProgs = isSuper || admin.role === 'staff'
    ? APP_DATA.programs.map(p => p.title)
    : (admin.programs || []);
  const myUsers = APP_DATA.users.filter(u => myProgs.includes(u.program));

  const statGrid = createEl('div', 'stat-grid');
  const sc1 = createEl('div', 'neu-card-flat stat-card');
  sc1.appendChild(createEl('div', 'stat-value', String(myProgs.length)));
  sc1.appendChild(createEl('div', 'stat-label', '프로그램'));
  statGrid.appendChild(sc1);
  const sc2 = createEl('div', 'neu-card-flat stat-card');
  sc2.appendChild(createEl('div', 'stat-value', String(myUsers.length)));
  sc2.appendChild(createEl('div', 'stat-label', CONFIG.terms.user));
  statGrid.appendChild(sc2);

  // 출결 통계
  let totalAtt = 0, attCount = 0;
  myUsers.forEach(u => {
    Object.values(u.attendance).forEach(s => {
      totalAtt++;
      if (s === '출석') attCount++;
    });
  });
  const sc3 = createEl('div', 'neu-card-flat stat-card');
  sc3.appendChild(createEl('div', 'stat-value', totalAtt > 0 ? Math.round((attCount / totalAtt) * 100) + '%' : '-'));
  sc3.appendChild(createEl('div', 'stat-label', '출석률'));
  statGrid.appendChild(sc3);

  // 매출
  const totalRev = APP_DATA.payments.reduce((s, p) => s + p.amount, 0);
  const sc4 = createEl('div', 'neu-card-flat stat-card');
  sc4.appendChild(createEl('div', 'stat-value', formatCurrency(totalRev).replace(' 원', '')));
  sc4.appendChild(createEl('div', 'stat-label', '총 매출 (원)'));
  statGrid.appendChild(sc4);

  dashPanel.appendChild(statGrid);

  // 프로그램별 간단 분석
  myProgs.forEach(pTitle => {
    const prog = APP_DATA.programs.find(p => p.title === pTitle);
    if (!prog) return;
    const progUsers = myUsers.filter(u => u.program === pTitle);
    const card = createEl('div', 'neu-card-flat');
    const row = createEl('div', 'flex-between');
    row.appendChild(createEl('div', 'workflow-task', prog.title));
    row.appendChild(createEl('span', 'meta-item', '👥 ' + progUsers.length + '명'));
    card.appendChild(row);

    const roleKeys = Object.keys(prog.roles_workflow);
    if (roleKeys.length > 0) {
      const progress = getProgress(prog.roles_workflow[roleKeys[0]]);
      const bar = createEl('div', 'progress-bar-container');
      const fill = createEl('div', 'progress-bar-fill');
      fill.style.width = progress + '%';
      bar.appendChild(fill);
      card.appendChild(bar);
    }
    dashPanel.appendChild(card);
  });
  container.appendChild(dashPanel);

  // 패널: 재무
  const finPanel = createEl('div', 'admin-panel');
  finPanel.id = 'admin-panel-finance';
  finPanel.appendChild(createEl('div', 'section-title', '💳 결제 내역'));

  if (isSuper || admin.role === 'staff') {
    const table = createEl('table', 'data-table');
    const thead = createEl('thead');
    const tr = createEl('tr');
    ['결제일', '학생', '항목', '금액', '수단'].forEach(h => tr.appendChild(createEl('th', '', h)));
    thead.appendChild(tr);
    table.appendChild(thead);

    const tbody = createEl('tbody');
    APP_DATA.payments.forEach(pay => {
      const row = createEl('tr');
      [pay.date, pay.student, pay.category, formatCurrency(pay.amount), pay.method].forEach(val => {
        row.appendChild(createEl('td', '', val));
      });
      tbody.appendChild(row);
    });
    table.appendChild(tbody);

    const tableCard = createEl('div', 'neu-card');
    tableCard.style.overflowX = 'auto';
    tableCard.appendChild(table);
    finPanel.appendChild(tableCard);

    // 총액
    finPanel.appendChild(createEl('div', 'alert alert-success', '💰 누적 매출: ' + formatCurrency(totalRev)));
  } else {
    finPanel.appendChild(createEl('div', 'alert alert-danger', '🔒 접근 권한이 없습니다.'));
  }
  container.appendChild(finPanel);

  // 패널: 명단
  const rosterPanel = createEl('div', 'admin-panel');
  rosterPanel.id = 'admin-panel-roster';
  rosterPanel.appendChild(createEl('div', 'section-title', '📊 종합 명단'));

  myProgs.forEach(pTitle => {
    const progUsers = myUsers.filter(u => u.program === pTitle);
    if (progUsers.length === 0) return;
    const card = createEl('div', 'neu-card');
    card.appendChild(createEl('div', 'program-title', pTitle + ' (' + progUsers.length + '명)'));
    progUsers.forEach(u => {
      const item = createEl('div', 'workflow-item');
      item.appendChild(createEl('div', 'workflow-task', '👤 ' + u.name));
      card.appendChild(item);
    });
    rosterPanel.appendChild(card);
  });
  container.appendChild(rosterPanel);

  // 패널: 출석
  const attPanel = createEl('div', 'admin-panel');
  attPanel.id = 'admin-panel-attendance';
  attPanel.appendChild(createEl('div', 'section-title', '✅ 출석 관리'));
  attPanel.appendChild(createEl('div', 'alert alert-info', '💡 데모 모드: 출석 변경은 제한됩니다.'));

  myUsers.forEach(user => {
    const card = createEl('div', 'neu-card-flat');
    card.appendChild(createEl('div', 'workflow-task', user.name + ' (' + user.program + ')'));
    const attList = createEl('div', 'att-list');
    Object.entries(user.attendance).forEach(([date, status]) => {
      const color = CONFIG.attendanceColors[status] || '#888';
      const badge = createEl('span', 'att-badge');
      badge.textContent = date.slice(5) + ' ' + status;
      badge.style.background = color;
      badge.style.color = '#fff';
      attList.appendChild(badge);
    });
    card.appendChild(attList);
    attPanel.appendChild(card);
  });
  container.appendChild(attPanel);

  // 패널: 평가
  const evalPanel = createEl('div', 'admin-panel');
  evalPanel.id = 'admin-panel-eval';
  evalPanel.appendChild(createEl('div', 'section-title', '📝 평가/코멘트'));
  evalPanel.appendChild(createEl('div', 'alert alert-info', '💡 데모 모드: 평가 입력은 제한됩니다.'));

  myProgs.forEach(pTitle => {
    const prog = APP_DATA.programs.find(p => p.title === pTitle);
    if (!prog) return;
    const card = createEl('div', 'neu-card');
    card.appendChild(createEl('div', 'program-title', pTitle));
    Object.values(prog.roles_workflow).forEach(wfList => {
      wfList.forEach(item => {
        if (item.score > 0 || item.comment) {
          const wfItem = createEl('div', 'workflow-item');
          const info = createEl('div', 'workflow-info');
          info.appendChild(createEl('div', 'workflow-task', item.task));
          if (item.score > 0) info.appendChild(createEl('div', 'workflow-score', '⭐ ' + item.score + '점'));
          if (item.comment) info.appendChild(createEl('div', 'workflow-date', '💬 ' + item.comment));
          wfItem.appendChild(info);
          card.appendChild(wfItem);
        }
      });
    });
    evalPanel.appendChild(card);
  });
  container.appendChild(evalPanel);
}
