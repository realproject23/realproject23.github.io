// ============================================
// Youth Canvas — 3-Theme Neumorphism SPA
// Shared logic: Navigation, Calendar, Accordion, Theme Switcher
// ============================================

document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initCalendar();
  initMobileMenu();
  initThemeSwitcher();
});

// =============================================
//  THEME SWITCHER
// =============================================
function initThemeSwitcher() {
  const dots = document.querySelectorAll('.theme-dot');
  const saved = localStorage.getItem('yc-theme') || '1';
  
  // Apply saved theme
  applyTheme(saved);
  dots.forEach(d => {
    d.classList.toggle('active', d.dataset.theme === saved);
  });

  dots.forEach(dot => {
    dot.addEventListener('click', () => {
      const theme = dot.dataset.theme;
      applyTheme(theme);
      dots.forEach(d => d.classList.remove('active'));
      dot.classList.add('active');
      localStorage.setItem('yc-theme', theme);
    });
  });
}

function applyTheme(theme) {
  document.body.classList.remove('theme-1', 'theme-2', 'theme-3');
  document.body.classList.add('theme-' + theme);
}

// =============================================
//  NAVIGATION  
// =============================================
function initNavigation() {
  const navBtns = document.querySelectorAll('.nav-btn');
  const pages = document.querySelectorAll('.page-section');

  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.page;

      // Update active button
      navBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Show target page
      pages.forEach(p => p.classList.remove('active'));
      const targetPage = document.getElementById('page-' + target);
      if (targetPage) {
        targetPage.classList.add('active');
      }

      // Close mobile sidebar
      closeMobileMenu();
    });
  });
}

// =============================================
//  ACCORDION
// =============================================
function toggleAccordion(header) {
  const body = header.nextElementSibling;
  const isOpen = header.classList.contains('open');

  // Close all accordions in the same card
  const card = header.closest('.activity-card');
  if (card) {
    card.querySelectorAll('.accordion-header').forEach(h => {
      h.classList.remove('open');
      h.nextElementSibling.classList.remove('open');
    });
  }

  if (!isOpen) {
    header.classList.add('open');
    body.classList.add('open');
  }
}

// =============================================
//  CALENDAR
// =============================================
const calendarEvents = {
  '2026-03-22': [{ title: '[특강] 1차', type: 'lecture' }],
  '2026-03-25': [{ title: '[K-POP] 1차', type: 'special' }],
  '2026-03-27': [{ title: '[크리에이터] 기획', type: '' }],
  '2026-03-28': [{ title: '[독서] 1차', type: '' }],
  '2026-03-29': [{ title: '[특강] 2차', type: 'lecture' }],
  '2026-04-01': [{ title: '[K-POP] 2차', type: 'special' }],
  '2026-04-03': [{ title: '[크리에이터] 촬영', type: '' }],
  '2026-04-04': [{ title: '[독서] 2차', type: '' }],
  '2026-04-05': [{ title: '[봉사] 지역사회', type: '' }],
  '2026-04-10': [{ title: '[크리에이터] 편집', type: '' }],
  '2026-04-12': [{ title: '[봉사] 환경정화', type: '' }],
};

let currentYear = 2026;
let currentMonth = 3; // 1-indexed

function initCalendar() {
  renderMonthSlider();
  renderCalendar();

  document.getElementById('yearSelect').addEventListener('change', (e) => {
    currentYear = parseInt(e.target.value);
    renderCalendar();
  });
}

function renderMonthSlider() {
  const container = document.getElementById('monthSlider');
  container.innerHTML = '';
  for (let m = 1; m <= 12; m++) {
    const btn = document.createElement('button');
    btn.className = 'month-btn' + (m === currentMonth ? ' active' : '');
    btn.textContent = m;
    btn.addEventListener('click', () => {
      currentMonth = m;
      document.querySelectorAll('.month-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderCalendar();
    });
    container.appendChild(btn);
  }
}

function renderCalendar() {
  const body = document.getElementById('calendarBody');
  body.innerHTML = '';

  const firstDay = new Date(currentYear, currentMonth - 1, 1);
  const lastDay = new Date(currentYear, currentMonth, 0);
  const startDow = firstDay.getDay();
  const totalDays = lastDay.getDate();

  // Previous month fill
  const prevMonthLast = new Date(currentYear, currentMonth - 1, 0).getDate();
  for (let i = startDow - 1; i >= 0; i--) {
    const cell = createCalendarCell(prevMonthLast - i, true);
    body.appendChild(cell);
  }

  // Current month
  const today = new Date();
  for (let d = 1; d <= totalDays; d++) {
    const dateStr = `${currentYear}-${String(currentMonth).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    const isToday = today.getFullYear() === currentYear &&
                    today.getMonth() + 1 === currentMonth &&
                    today.getDate() === d;
    const events = calendarEvents[dateStr] || [];
    const cell = createCalendarCell(d, false, isToday, events);
    body.appendChild(cell);
  }

  // Next month fill
  const totalCells = startDow + totalDays;
  const remaining = (7 - (totalCells % 7)) % 7;
  for (let i = 1; i <= remaining; i++) {
    const cell = createCalendarCell(i, true);
    body.appendChild(cell);
  }
}

function createCalendarCell(day, isOtherMonth, isToday = false, events = []) {
  const cell = document.createElement('div');
  cell.className = 'calendar-cell';
  if (isOtherMonth) cell.classList.add('other-month');
  if (isToday) cell.classList.add('today');

  const dayNum = document.createElement('div');
  dayNum.className = 'day-number';
  dayNum.textContent = day;
  cell.appendChild(dayNum);

  events.forEach(ev => {
    const badge = document.createElement('span');
    badge.className = 'calendar-event' + (ev.type ? ' ' + ev.type : '');
    badge.textContent = ev.title;
    cell.appendChild(badge);
  });

  return cell;
}

// =============================================
//  MOBILE MENU
// =============================================
function initMobileMenu() {
  const menuBtn = document.getElementById('mobileMenuBtn');
  const overlay = document.getElementById('overlay');

  if (menuBtn) {
    menuBtn.addEventListener('click', () => {
      document.getElementById('sidebar').classList.toggle('open');
      overlay.classList.toggle('active');
    });
  }

  if (overlay) {
    overlay.addEventListener('click', closeMobileMenu);
  }
}

function closeMobileMenu() {
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('overlay').classList.remove('active');
}

// =============================================
//  SYNC BUTTON ANIMATION
// =============================================
document.getElementById('syncBtn')?.addEventListener('click', () => {
  const icon = document.querySelector('.sync-icon');
  icon.style.transition = 'transform 1s ease';
  icon.style.transform = 'rotate(360deg)';
  setTimeout(() => {
    icon.style.transition = 'none';
    icon.style.transform = 'rotate(0)';
  }, 1000);
});
