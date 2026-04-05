// ─────────────────────────────────────────────
// utils.js — 유틸리티 함수
// ─────────────────────────────────────────────

function safeKey(str) {
  return str.replace(/[^a-zA-Z0-9가-힣]/g, '_');
}

function getToday() {
  const d = new Date();
  return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}

function getRecruitStatus(startDate, endDate) {
  const today = new Date();
  const s = new Date(startDate);
  const e = new Date(endDate);
  if (today < s) return { text: '모집 예정', cls: 'badge-info' };
  if (today > e) return { text: '모집 마감', cls: 'badge-danger' };
  return { text: '모집 중', cls: 'badge-success' };
}

function getProgress(workflow) {
  if (!workflow || workflow.length === 0) return 0;
  const done = workflow.filter(w => w.done).length;
  return Math.round((done / workflow.length) * 100);
}

function formatCurrency(num) {
  return num.toLocaleString('ko-KR') + ' 원';
}

function getDaysInMonth(year, month) {
  return new Date(year, month, 0).getDate();
}

function getFirstDayOfMonth(year, month) {
  return new Date(year, month - 1, 1).getDay();
}

function parseDate(dateStr) {
  const parts = dateStr.split('-');
  return { year: parseInt(parts[0]), month: parseInt(parts[1]), day: parseInt(parts[2]) };
}

function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = 'toast toast-' + type;
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.classList.add('show'), 10);
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}

// 보안: innerHTML 대신 안전한 텍스트 삽입
function setText(el, text) {
  el.textContent = text;
}

function createEl(tag, cls, text) {
  const el = document.createElement(tag);
  if (cls) el.className = cls;
  if (text) el.textContent = text;
  return el;
}
