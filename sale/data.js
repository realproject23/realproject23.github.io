// ─────────────────────────────────────────────
// data.js — JSON 백업 → 정적 데이터 (민감 정보 제거)
// ─────────────────────────────────────────────
const APP_DATA = {
  programs: [
    {
      title: '입시 특강',
      desc: '입시 특강',
      color: '#4ee546',
      recruit_start: '2026-03-01',
      recruit_end: '2026-06-30',
      roles_capacity: { '수강생': 10 },
      roles_workflow: {
        '수강생': [
          { start_date: '2026-03-23', end_date: '2026-03-23', time: '14:00~16:00', task: '1차 특강', subtasks: [], done: false, score: 0, comment: '' },
          { start_date: '2026-03-30', end_date: '2026-03-30', time: '14:00~16:00', task: '2차 특강', subtasks: [], done: false, score: 0, comment: '' }
        ]
      }
    },
    {
      title: '우쿨렐레',
      desc: '우쿨렐레 교실',
      color: '#ff9800',
      recruit_start: '2026-03-01',
      recruit_end: '2026-12-31',
      roles_capacity: { '수강생': 15 },
      roles_workflow: {
        '수강생': [
          { start_date: '2026-04-01', end_date: '2026-04-01', time: '10:00~12:00', task: '기초 과정', subtasks: [{ desc: '코드 익히기', done: false }], done: false, score: 0, comment: '' },
          { start_date: '2026-04-08', end_date: '2026-04-08', time: '10:00~12:00', task: '연주 실습', subtasks: [], done: false, score: 0, comment: '' },
          { start_date: '2026-04-15', end_date: '2026-04-15', time: '10:00~12:00', task: '합주', subtasks: [], done: false, score: 0, comment: '' }
        ]
      }
    },
    {
      title: '요리 교실',
      desc: '건강한 요리 만들기',
      color: '#e91e63',
      recruit_start: '2026-03-15',
      recruit_end: '2026-09-30',
      roles_capacity: { '수강생': 12 },
      roles_workflow: {
        '수강생': [
          { start_date: '2026-04-05', end_date: '2026-04-05', time: '15:00~17:00', task: '한식 기본', subtasks: [{ desc: '재료 준비', done: true }, { desc: '조리 실습', done: false }], done: false, score: 85, comment: '잘 하고 있습니다' },
          { start_date: '2026-04-12', end_date: '2026-04-12', time: '15:00~17:00', task: '양식 기본', subtasks: [], done: false, score: 0, comment: '' }
        ]
      }
    },
    {
      title: '코딩 교실',
      desc: '파이썬 기초 프로그래밍',
      color: '#2196f3',
      recruit_start: '2026-04-01',
      recruit_end: '2026-08-31',
      roles_capacity: { '수강생': 20 },
      roles_workflow: {
        '수강생': [
          { start_date: '2026-04-10', end_date: '2026-04-10', time: '13:00~15:00', task: 'Python 기초', subtasks: [{ desc: '변수와 자료형', done: false }], done: false, score: 0, comment: '' },
          { start_date: '2026-04-17', end_date: '2026-04-17', time: '13:00~15:00', task: '조건문과 반복문', subtasks: [], done: false, score: 0, comment: '' },
          { start_date: '2026-04-24', end_date: '2026-04-24', time: '13:00~15:00', task: '함수와 모듈', subtasks: [], done: false, score: 0, comment: '' }
        ]
      }
    },
    {
      title: '미술 치료',
      desc: '미술을 통한 마음 치유',
      color: '#9c27b0',
      recruit_start: '2026-03-20',
      recruit_end: '2026-07-31',
      roles_capacity: { '수강생': 8 },
      roles_workflow: {
        '수강생': [
          { start_date: '2026-04-02', end_date: '2026-04-02', time: '16:00~18:00', task: '자기 탐색', subtasks: [], done: true, score: 90, comment: '적극적으로 참여' },
          { start_date: '2026-04-09', end_date: '2026-04-09', time: '16:00~18:00', task: '감정 표현', subtasks: [], done: false, score: 0, comment: '' }
        ]
      }
    }
  ],

  // 데모 사용자 (PIN 제거, 이름만 표시)
  users: [
    { name: '김서연', program: '우쿨렐레', attendance: { '2026-04-01': '출석', '2026-04-08': '지각' } },
    { name: '이준호', program: '요리 교실', attendance: { '2026-04-05': '출석' } },
    { name: '박지민', program: '코딩 교실', attendance: {} },
    { name: '최유나', program: '미술 치료', attendance: { '2026-04-02': '출석' } },
    { name: '정하늘', program: '입시 특강', attendance: {} },
    { name: '강민재', program: '우쿨렐레', attendance: { '2026-04-01': '출석', '2026-04-08': '출석' } },
    { name: '윤서영', program: '요리 교실', attendance: { '2026-04-05': '결석' } },
    { name: '한도윤', program: '코딩 교실', attendance: {} }
  ],

  // 데모 학부모 (PIN 제거)
  parents: [
    { name: '김부모', children: ['김서연'] },
    { name: '이부모', children: ['이준호', '정하늘'] }
  ],

  // 관리자 역할 표시용 (PIN 제거)
  admins: [
    { name: '마스터', role: 'super' },
    { name: '행정1', role: 'staff' },
    { name: '김선생', role: 'normal', programs: ['우쿨렐레', '입시 특강'] },
    { name: '이선생', role: 'normal', programs: ['요리 교실'] },
    { name: '박선생', role: 'normal', programs: ['코딩 교실'] },
    { name: '최선생', role: 'normal', programs: ['미술 치료'] }
  ],

  // 데모 결제 내역
  payments: [
    { date: '2026-03-20', student: '김서연 (우쿨렐레)', category: '수강료', amount: 50000, method: '카드결제', note: '3월 수강료' },
    { date: '2026-03-22', student: '이준호 (요리 교실)', category: '수강료', amount: 45000, method: '계좌이체', note: '3월 수강료' },
    { date: '2026-03-25', student: '최유나 (미술 치료)', category: '교재비', amount: 15000, method: '현금', note: '미술 재료비' },
    { date: '2026-04-01', student: '강민재 (우쿨렐레)', category: '수강료', amount: 50000, method: '카드결제', note: '4월 수강료' }
  ],

  // UI 설정
  settings: {
    page1_title: '우리 기관 프로그램 찾아보기',
    page2_title: '전체 일정 캘린더',
    page3_title: '나의 이야기',
    page4_title: '학부모 라운지',
    page5_title: '관계자 외 출입금지'
  }
};
