// ─────────────────────────────────────────────
// config.js — 모든 설정값 (AS 시 이 파일만 수정)
// ─────────────────────────────────────────────
const CONFIG = {
  // 브랜드
  brand: '청소년의 꿈을 그리는 공간',
  subtitle: 'Youth Canvas',
  version: '1.0',

  // 메뉴 (하단 탭바)
  menus: [
    { id: 'browse',   icon: '🔍', label: '찾아보기' },
    { id: 'calendar', icon: '📅', label: '전체 일정' },
    { id: 'student',  icon: '📖', label: '나의 이야기' },
    { id: 'parent',   icon: '👨‍👩‍👧', label: '학부모 라운지' },
    { id: 'admin',    icon: '🔒', label: '관계자 외 출입금지' }
  ],

  // 용어 설정
  terms: {
    super:  '시설장',
    staff:  '행정담당자',
    admin:  '선생님',
    user:   '수강생',
    parent: '보호자'
  },

  // 뉴모피즘 테마
  theme: {
    bg:            '#e0ddd4',
    surface:       '#e0ddd4',
    text:          '#3d3929',
    textSecondary: '#8a8472',
    accent:        '#8fbc8f',
    accentLight:   '#c5e1a5',
    danger:        '#d9534f',
    success:       '#5cb85c',
    warning:       '#f0ad4e',
    shadowDark:    'rgba(163,160,151,0.55)',
    shadowLight:   'rgba(255,255,248,0.85)',
  },

  // 출결 상태
  attendanceStatus: ['출석', '지각', '결석', '병결'],
  attendanceColors: {
    '출석': '#5cb85c',
    '지각': '#f0ad4e',
    '결석': '#d9534f',
    '병결': '#9b59b6'
  },

  // 데모 모드 안내
  demoMode: true,
  demoNotice: '⚠️ 이 사이트는 데모 버전입니다. 실제 데이터는 포함되어 있지 않습니다.'
};
