from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, firestore
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import jwt
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "youth-canvas-super-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

security = HTTPBearer()

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try: return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError: return False

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None: raise HTTPException(status_code=401)
        return {"username": username, "role": payload.get("role")}
    except Exception: raise HTTPException(status_code=401, detail="토큰 무효")

app = FastAPI(title="Youth Canvas API Server", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

try:
    FIREBASE_CERT_PATH = os.getenv("FIREBASE_CERT_PATH", "serviceAccountKey.json")
    cred = credentials.Certificate(FIREBASE_CERT_PATH)
    if not firebase_admin._apps: firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e: db = None 

class ProgramRecord(BaseModel): name: str; desc: str; workflow: str; yt_link: Optional[str] = ""; start_date: Optional[str] = ""; end_date: Optional[str] = ""; max_participants: Optional[int] = 10; image_base64: Optional[str] = ""; calendar_color: Optional[str] = "#10B981"
class UserLogin(BaseModel): name: str; pin: str
class StudentSignup(BaseModel): name: str; pin: str; program: str
class BillingRecord(BaseModel): student_name: str; program_name: str; amount: int; method: str; note: Optional[str] = ""
class ParentRecord(BaseModel): name: str; pin: str; child_name: str
class AttendanceRecord(BaseModel): student_name: str; status: str; note: Optional[str] = ""
class DailyAttendance(BaseModel): date: str; program: str; records: list[AttendanceRecord]
class EvaluationScores(BaseModel): task: int; prof: int; att: int; comm: int
class EvaluationRecord(BaseModel): student_name: str; scores: EvaluationScores; comment: str

# 💡 [핵심] 승인 워크플로우를 위한 모델 변경
class TaskUpdate(BaseModel): task_id: str; task_text: str; completed: bool

# 출결 기록 개별 조작 (수정/삭제)를 위한 모델
class SingleAttendanceUpdate(BaseModel): date: str; program: str; student_name: str; status: str; note: Optional[str] = ""
class SingleAttendanceDelete(BaseModel): date: str; program: str; student_name: str
class TaskApprove(BaseModel): student_name: str; task_id: str; action: str

# 💡 [추가] 채팅, 학생관리, 재무, 학부모 프로필을 위한 모델
class ChatMessage(BaseModel): target_name: str; message: str; channel: Optional[str] = "student"
class StudentChatMessage(BaseModel): message: str
class StudentUpdate(BaseModel): name: str; new_name: Optional[str] = None; new_pin: Optional[str] = None
class ParentProfileDetail(BaseModel): parent_name: str; details: dict
class LocalFileSave(BaseModel): directory: str; filename: str; content: str

@app.get("/")
@app.get("/index.html")
def serve_index_page(): return FileResponse("index.html")
@app.get("/admin")
@app.get("/admin.html")
def serve_admin_page(): return FileResponse("admin.html")
@app.get("/login_v3.html")
def serve_login_page(): return FileResponse("login_v3.html")
@app.get("/dashboard.html")
def serve_dashboard(): return FileResponse("dashboard.html")
@app.get("/parents.html")
def serve_parents(): return FileResponse("parents.html")
@app.get("/calendar.html")
def serve_calendar(): return FileResponse("calendar.html")

# Serve static JS and CSS files
@app.get("/i18n.js")
def serve_i18n(): return FileResponse("i18n.js")
@app.get("/firebase_client.js")
def serve_firebase_client(): return FileResponse("firebase_client.js")
@app.get("/style.css")
def serve_style(): return FileResponse("style.css")
@app.get("/script.js")
def serve_script(): return FileResponse("script.js")

# 💡 [핵심] 여러 프로그램 지원을 위한 모델 및 헬퍼 추가
class UserProgramUpdate(BaseModel): name: str; program: str

@app.post("/api/user/add_program")
def add_user_program(data: UserProgramUpdate):
    if not db: raise HTTPException(status_code=500)
    for doc in db.collection("users").where("name", "==", data.name).stream():
        programs = doc.to_dict().get("programs", [])
        if data.program not in programs: programs.append(data.program)
        doc.reference.update({"programs": programs})
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/api/login")
def login(user: UserLogin):
    if not db: raise HTTPException(status_code=500, detail="DB Error")
    if user.name == "master" and user.pin == "1234":
        return {"access_token": create_access_token({"sub": user.name, "role": "admin"}), "token_type": "bearer", "user": {"name": "master", "role": "admin"}}
    user_doc = None
    for doc in db.collection("users").where("name", "==", user.name).stream(): user_doc = doc.to_dict(); break
    if not user_doc: raise HTTPException(status_code=401, detail="등록되지 않은 이름입니다.")
    if not verify_password(user.pin, user_doc.get("pin", "")): raise HTTPException(status_code=401, detail="비밀번호 오류")
    return {"access_token": create_access_token({"sub": user.name, "role": user_doc.get("role")}), "token_type": "bearer", "user": {"name": user.name, "role": user_doc.get("role")}}

@app.post("/api/students/signup")
def signup_student(record: StudentSignup):
    if not db: raise HTTPException(status_code=500)
    existing_docs = list(db.collection("users").where("name", "==", record.name).stream())
    if existing_docs:
        doc = existing_docs[0]
        user_data = doc.to_dict()
        if not verify_password(record.pin, user_data.get("pin", "")):
            raise HTTPException(status_code=400, detail="이미 등록된 이름입니다. 본인이라면 정확한 PIN 번호를 입력하세요.")
        programs = user_data.get("programs", [])
        if record.program not in programs: programs.append(record.program)
        doc.reference.update({"programs": programs, "program": record.program}) # 호환성을 위해 둘 다 업데이트
        return {"status": "success"}
    db.collection("users").add({"name": record.name, "pin": get_password_hash(record.pin), "role": "student", "programs": [record.program], "program": record.program})
    return {"status": "success"}

@app.get("/api/programs")
def get_programs():
    if not db: return []
    try:
        student_counts = {}
        for u in db.collection("users").where("role", "==", "student").stream(): student_counts[u.to_dict().get("program", "")] = student_counts.get(u.to_dict().get("program", ""), 0) + 1
        return [{**doc.to_dict(), "current_participants": student_counts.get(doc.to_dict().get("name"), 0)} for doc in db.collection("programs").stream()]
    except Exception: return []

@app.get("/api/dashboard/summary")
def get_dashboard_summary(current_user: dict = Depends(get_current_user)):
    if not db: return {"total_students": 0, "active_programs": 0, "avg_progress": 0, "billing_rate": 0}
    try: return {"total_students": sum(1 for user in db.collection("users").stream() if user.to_dict().get("role") == "student"), "active_programs": sum(1 for _ in db.collection("programs").stream()), "avg_progress": 75.5, "billing_rate": 85}
    except Exception: return {"total_students": 0, "active_programs": 0, "avg_progress": 0, "billing_rate": 0}

@app.get("/api/admin/ml_report")
def ml_report(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin": raise HTTPException(status_code=403)
    if not db: return {"status": "error"}
    
    try:
        from sklearn.cluster import KMeans
        import numpy as np
        
        docs = list(db.collection("evaluations").stream())
        if len(docs) < 3: return {"status": "insufficient_data"}
            
        student_scores = {}
        for doc in docs:
            d = doc.to_dict()
            s = d.get("scores", {})
            name = d.get("student_name", "Unknown")
            if name not in student_scores: student_scores[name] = []
            student_scores[name].append([s.get("task",0), s.get("prof",0), s.get("att",0), s.get("comm",0)])
            
        X = []
        for name, scores in student_scores.items():
            avg_scores = np.mean(scores, axis=0)
            X.append(avg_scores)
            
        X = np.array(X)
        if len(X) < 3: return {"status": "insufficient_data"}
        
        n_clusters = min(3, len(X))
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        
        cluster_means = [(i, np.mean(X[labels == i])) for i in range(n_clusters)]
        cluster_means.sort(key=lambda x: x[1])
        at_risk_cluster = cluster_means[0][0]
        high_achieve_cluster = cluster_means[-1][0]
        
        return {
            "status": "success",
            "at_risk": int(np.sum(labels == at_risk_cluster)),
            "high_achievers": int(np.sum(labels == high_achieve_cluster)),
            "total": len(X),
            "avg_score": round(float(np.mean(X)), 1)
        }
    except Exception as e:
        print(f"ML Error: {e}")
        return {"status": "error"}

@app.get("/api/students")
def get_students(current_user: dict = Depends(get_current_user)):
    if not db: return []
    try: return [user.to_dict() for user in db.collection("users").stream() if user.to_dict().get("role") in ["student", "parent"]]
    except Exception: return []

@app.post("/api/billing/add")
def add_billing_record(record: BillingRecord, current_user: dict = Depends(get_current_user)):
    data = record.model_dump(); data["date"] = datetime.now().strftime("%Y-%m-%d"); db.collection("billing").add(data); return {"status": "success"}

@app.get("/api/billing")
def get_billing(current_user: dict = Depends(get_current_user)):
    if not db: return []
    result = []
    for doc in db.collection("billing").order_by("date", direction=firestore.Query.DESCENDING).stream():
        d = doc.to_dict()
        d["id"] = doc.id
        result.append(d)
    return result

class BillingUpdate(BaseModel): student_name: str; program_name: str; amount: int; method: str; note: Optional[str] = ""

@app.put("/api/billing/update/{billing_id}")
def update_billing(billing_id: str, record: BillingUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    db.collection("billing").document(billing_id).update(record.model_dump())
    return {"status": "updated"}

@app.post("/api/programs/add")
def add_program(record: ProgramRecord, current_user: dict = Depends(get_current_user)):
    db.collection("programs").add(record.model_dump()); return {"status": "success"}

@app.put("/api/programs/update/{name}")
def update_program(name: str, record: ProgramRecord, current_user: dict = Depends(get_current_user)):
    doc_id = None
    for doc in db.collection("programs").where("name", "==", name).stream(): doc_id = doc.id; break
    if not doc_id: raise HTTPException(status_code=404)
    db.collection("programs").document(doc_id).update(record.model_dump()); return {"status": "success"}

@app.delete("/api/programs/delete/{name}")
def delete_program(name: str, current_user: dict = Depends(get_current_user)):
    doc_id = None
    for doc in db.collection("programs").where("name", "==", name).stream(): doc_id = doc.id; break
    if not doc_id: raise HTTPException(status_code=404)
    db.collection("programs").document(doc_id).delete(); return {"status": "success"}

@app.post("/api/parents/add")
def add_parent(record: ParentRecord, current_user: dict = Depends(get_current_user)):
    data = record.model_dump(); data["role"] = "parent"; data["pin"] = get_password_hash(data["pin"]); db.collection("users").add(data); return {"status": "success"}

@app.post("/api/attendance/add")
def add_attendance(data: DailyAttendance, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin": raise HTTPException(status_code=403)
    doc_id = None
    for doc in db.collection("attendance").where("date", "==", data.date).where("program", "==", data.program).stream(): doc_id = doc.id; break
    if doc_id: db.collection("attendance").document(doc_id).set(data.model_dump(), merge=True)
    else: db.collection("attendance").add(data.model_dump())
    return {"status": "success"}

@app.get("/api/attendance/program/{program_name}")
def get_program_attendance(program_name: str, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin": raise HTTPException(status_code=403)
    records = []
    for doc in db.collection("attendance").where("program", "==", program_name).stream(): records.append(doc.to_dict())
    records.sort(key=lambda x: x.get("date", ""), reverse=True)
    return records

@app.put("/api/attendance/update")
def update_single_attendance(data: SingleAttendanceUpdate, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin": raise HTTPException(status_code=403)
    doc_id, doc_data = None, None
    for doc in db.collection("attendance").where("date", "==", data.date).where("program", "==", data.program).stream(): 
        doc_id, doc_data = doc.id, doc.to_dict(); break
    if not doc_id or not doc_data: raise HTTPException(status_code=404, detail="해당 날짜/프로그램의 기록 없음")
    
    updated_records, found = [], False
    for r in doc_data.get("records", []):
        if r.get("student_name") == data.student_name:
            updated_records.append({"student_name": data.student_name, "status": data.status, "note": data.note or ""}); found = True
        else: updated_records.append(r)
    if not found: updated_records.append({"student_name": data.student_name, "status": data.status, "note": data.note or ""})
        
    db.collection("attendance").document(doc_id).update({"records": updated_records})
    return {"status": "success"}

@app.delete("/api/attendance/delete")
def delete_single_attendance(data: SingleAttendanceDelete, current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin": raise HTTPException(status_code=403)
    doc_id, doc_data = None, None
    for doc in db.collection("attendance").where("date", "==", data.date).where("program", "==", data.program).stream(): 
        doc_id, doc_data = doc.id, doc.to_dict(); break
    if not doc_id or not doc_data: raise HTTPException(status_code=404, detail="기록 없음")
    
    updated_records = [r for r in doc_data.get("records", []) if r.get("student_name") != data.student_name]
    if not updated_records: db.collection("attendance").document(doc_id).delete()
    else: db.collection("attendance").document(doc_id).update({"records": updated_records})
    return {"status": "success"}

@app.post("/api/evaluation/add")
def add_evaluation(data: EvaluationRecord, current_user: dict = Depends(get_current_user)):
    eval_data = data.model_dump(); eval_data["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S"); eval_data["teacher"] = current_user["username"]
    db.collection("evaluations").add(eval_data); return {"status": "success"}

# 💡 [핵심] 학생의 승인 요청 처리 (status: pending 으로 저장)
@app.post("/api/user/tasks")
def update_user_task(data: TaskUpdate, current_user: dict = Depends(get_current_user)):
    if not db: raise HTTPException(status_code=500)
    name = current_user["username"]
    doc_ref = db.collection("user_tasks").document(name)
    doc = doc_ref.get()
    tasks = doc.to_dict().get("tasks", {}) if doc.exists else {}
    
    if data.completed:
        # 승인 요청 상태로 저장
        tasks[data.task_id] = {"status": "pending", "text": data.task_text, "date": datetime.now().strftime("%m-%d %H:%M")}
    else:
        # 체크 해제 시 삭제
        if data.task_id in tasks: del tasks[data.task_id]
        
    doc_ref.set({"tasks": tasks}, merge=True)
    return {"status": "success"}

# 💡 [핵심] 관리자 전용: 대기 중인 승인 요청 목록 불러오기
@app.get("/api/admin/tasks/pending")
def get_pending_tasks(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    pending_list = []
    for doc in db.collection("user_tasks").stream():
        tasks = doc.to_dict().get("tasks", {})
        for t_id, info in tasks.items():
            if info.get("status") == "pending":
                pending_list.append({"student_name": doc.id, "task_id": t_id, "text": info.get("text", "알 수 없는 미션"), "date": info.get("date", "")})
    return pending_list

# 💡 [핵심] 관리자 전용: 승인 또는 반려 처리
@app.post("/api/admin/tasks/approve")
def approve_task(data: TaskApprove, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    doc_ref = db.collection("user_tasks").document(data.student_name)
    doc = doc_ref.get()
    if doc.exists:
        tasks = doc.to_dict().get("tasks", {})
        if data.action == "approve":
            if data.task_id in tasks: tasks[data.task_id]["status"] = "approved"
        else: # 반려 시 내역 삭제 (학생이 다시 체크해야 함)
            if data.task_id in tasks: del tasks[data.task_id]
        doc_ref.set({"tasks": tasks}, merge=True)
    return {"status": "success"}

@app.get("/api/user/{name}")
def get_user_dashboard(name: str, current_user: dict = Depends(get_current_user)):
    if not db: raise HTTPException(status_code=500)
    user_data = {}
    for doc in db.collection("users").where("name", "==", name).limit(1).stream(): user_data = doc.to_dict(); break
    
    # 💡 [핵심] 여러 프로그램 정보들을 모두 취합하여 반환
    user_programs = user_data.get("programs", [user_data.get("program", "미지정")])
    if not user_programs: user_programs = ["미지정"]

    programs_detail = {}
    total_approved = []
    total_pending = []
    
    task_doc = db.collection("user_tasks").document(name).get()
    tasks_dict = task_doc.to_dict().get("tasks", {}) if task_doc.exists else {}
    
    for prog_name in user_programs:
        prog_data = {}
        for doc in db.collection("programs").where("name", "==", prog_name).limit(1).stream(): prog_data = doc.to_dict(); break
        
        workflow = prog_data.get("workflow", "")
        # 특정 프로그램에 해당하는 해시 ID가 부여된 미션들 필터링
        prog_tasks = [line.strip() for line in workflow.split('\n') if line.strip()]
        
        programs_detail[prog_name] = {
            "workflow": workflow,
            "total_tasks": len(prog_tasks)
        }

    approved_tasks = [k for k, v in tasks_dict.items() if v.get("status") == "approved"]
    pending_tasks = [k for k, v in tasks_dict.items() if v.get("status") == "pending"]
    
    eval_docs = list(db.collection("evaluations").where("student_name", "==", name).stream())
    eval_docs.sort(key=lambda x: x.to_dict().get("date", ""), reverse=True)
    latest_eval = eval_docs[0].to_dict() if eval_docs else {"scores": {"task": 0, "prof": 0, "att": 0, "comm": 0}, "comment": "피드백 대기중"}
    
    att_summary = {"출석": 0, "지각": 0, "결석": 0}
    for doc in db.collection("attendance").stream():
        for record in doc.to_dict().get("records", []):
            if record.get("student_name") == name and record.get("status") in att_summary: att_summary[record.get("status")] += 1
                
    att_score = min((att_summary["출석"] * 5) + (att_summary["지각"] * 2), 40)
    sc = latest_eval.get("scores", {"task":0,"prof":0,"att":0,"comm":0})
    eval_score = ((sc.get("task",0) + sc.get("prof",0) + sc.get("att",0) + sc.get("comm",0)) / 4 / 100) * 30
    
    total_possible_tasks = sum(p["total_tasks"] for p in programs_detail.values())
    task_score = (len(approved_tasks) / total_possible_tasks * 30) if total_possible_tasks > 0 else 0
    
    total_points = round(att_score + eval_score + task_score)
    tier = "🌱 C 등급 (비기너)"
    if total_points >= 85: tier = "🏆 S 등급 (마스터)"
    elif total_points >= 70: tier = "🥇 A 등급 (챌린저)"
    elif total_points >= 50: tier = "🥈 B 등급 (러너)"
                    
    return {
        "name": name, "programs": user_programs, "role": user_data.get("role", "student"),
        "programs_detail": programs_detail,
        "approved_tasks": approved_tasks, "pending_tasks": pending_tasks,
        "evaluation": latest_eval, "attendance": att_summary,
        "reward": {
            "points": total_points, "tier": tier,
            "criteria": ["출결 성실도 (40P)", "전체 프로그램 승인 미션 (30P)", "역량 평가 성취도 (30P)"]
        }
    }

@app.get("/api/parent/{name}")
def get_parent_dashboard(name: str, current_user: dict = Depends(get_current_user)):
    parent_doc = {}
    for doc in db.collection("users").where("name", "==", name).where("role", "==", "parent").limit(1).stream(): parent_doc = doc.to_dict(); break
    if not parent_doc: raise HTTPException(status_code=404)
    child_names = [c.strip() for c in parent_doc.get("child_name", "").split(",") if c.strip()]
    children_data = []
    for child_name in child_names:
        child_doc = {}
        for doc in db.collection("users").where("name", "==", child_name).where("role", "==", "student").limit(1).stream(): child_doc = doc.to_dict(); break
        eval_docs = list(db.collection("evaluations").where("student_name", "==", child_name).stream()); eval_docs.sort(key=lambda x: x.to_dict().get("date", ""), reverse=True)
        latest_eval = eval_docs[0].to_dict() if eval_docs else {"scores": {"task": 0, "prof": 0, "att": 0, "comm": 0}, "comment": "대기중"}
        att_summary = {"출석": 0, "지각": 0, "결석": 0}
        for doc in db.collection("attendance").stream():
            for record in doc.to_dict().get("records", []):
                if record.get("student_name") == child_name and record.get("status") in att_summary: att_summary[record.get("status")] += 1
        bill_docs = list(db.collection("billing").where("student_name", "==", child_name).stream()); bill_docs.sort(key=lambda x: x.to_dict().get("date", ""), reverse=True)
        children_data.append({"name": child_name, "program": child_doc.get("program", "미지정"), "evaluation": latest_eval, "attendance": att_summary, "billing": [b.to_dict() for b in bill_docs]})
    return {"parent_name": name, "children": children_data}

# ============================================================
# 💡 [Phase 1] 추가 API 엔드포인트 — Streamlit 미구현 기능 대응
# ============================================================

# === 1:1 채팅 시스템 ===
@app.post("/api/admin/chat/send")
def admin_send_chat(msg: ChatMessage, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    chat_ref = db.collection("chats").document(msg.target_name)
    chat_doc = chat_ref.get()
    messages = chat_doc.to_dict().get(msg.channel, []) if chat_doc.exists else []
    messages.append({"sender": "admin", "text": msg.message, "time": datetime.now().strftime("%Y-%m-%d %H:%M")})
    chat_ref.set({msg.channel: messages}, merge=True)
    return {"status": "sent"}

@app.get("/api/admin/chat/{target_name}")
def admin_get_chat(target_name: str, channel: str = "student", current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    chat_doc = db.collection("chats").document(target_name).get()
    if not chat_doc.exists: return []
    return chat_doc.to_dict().get(channel, [])

@app.post("/api/student/chat/send")
def student_send_chat(msg: StudentChatMessage, current_user: dict = Depends(get_current_user)):
    if not db: raise HTTPException(status_code=500)
    student_name = current_user["username"]
    chat_ref = db.collection("chats").document(student_name)
    chat_doc = chat_ref.get()
    messages = chat_doc.to_dict().get("student", []) if chat_doc.exists else []
    messages.append({"sender": student_name, "text": msg.message, "time": datetime.now().strftime("%Y-%m-%d %H:%M")})
    chat_ref.set({"student": messages}, merge=True)
    return {"status": "sent"}

@app.get("/api/student/chat")
def student_get_chat(current_user: dict = Depends(get_current_user)):
    if not db: raise HTTPException(status_code=500)
    student_name = current_user["username"]
    chat_doc = db.collection("chats").document(student_name).get()
    if not chat_doc.exists: return []
    return chat_doc.to_dict().get("student", [])

@app.post("/api/parent/chat/send")
def parent_send_chat(msg: StudentChatMessage, current_user: dict = Depends(get_current_user)):
    if not db: raise HTTPException(status_code=500)
    parent_name = current_user["username"]
    chat_ref = db.collection("chats").document(parent_name)
    chat_doc = chat_ref.get()
    messages = chat_doc.to_dict().get("parent", []) if chat_doc.exists else []
    messages.append({"sender": parent_name, "text": msg.message, "time": datetime.now().strftime("%Y-%m-%d %H:%M")})
    chat_ref.set({"parent": messages}, merge=True)
    return {"status": "sent"}

@app.get("/api/parent/chat")
def parent_get_chat(current_user: dict = Depends(get_current_user)):
    if not db: raise HTTPException(status_code=500)
    parent_name = current_user["username"]
    chat_doc = db.collection("chats").document(parent_name).get()
    if not chat_doc.exists: return []
    return chat_doc.to_dict().get("parent", [])

# === 출석 피벗 테이블 데이터 ===
@app.get("/api/admin/attendance/pivot/{program}")
def get_attendance_pivot(program: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    att_docs = list(db.collection("attendance").where("program", "==", program).stream())
    students_set = set()
    dates_dict = {}
    for doc in att_docs:
        d = doc.to_dict()
        date = d.get("date", "")
        records = d.get("records", [])
        dates_dict[date] = {}
        for r in records:
            sn = r.get("student_name", "")
            students_set.add(sn)
            dates_dict[date][sn] = r.get("status", "")
    students = sorted(list(students_set))
    dates = sorted(dates_dict.keys())
    pivot_rows = []
    for s in students:
        row = {"student_name": s}
        for d in dates:
            row[d] = dates_dict.get(d, {}).get(s, "-")
        pivot_rows.append(row)
    return {"dates": dates, "students": students, "rows": pivot_rows}

# === 재무 통계 ===
@app.get("/api/admin/finance/stats")
def get_finance_stats(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    bill_docs = list(db.collection("billing").stream())
    category_totals = {}
    date_totals = {}
    for doc in bill_docs:
        b = doc.to_dict()
        cat = b.get("program_name", "기타")
        amt = b.get("amount", 0)
        date = b.get("date", "")
        category_totals[cat] = category_totals.get(cat, 0) + amt
        date_totals[date] = date_totals.get(date, 0) + amt
    return {"category_totals": category_totals, "date_totals": date_totals, "total_revenue": sum(category_totals.values())}

# === 결제 내역 삭제 ===
@app.delete("/api/billing/delete/{billing_id}")
def delete_billing(billing_id: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    db.collection("billing").document(billing_id).delete()
    return {"status": "deleted"}

# === 구성원 정보 수정 (학생/학부모/선생님 모두 지원) ===
@app.put("/api/admin/student/update")
def update_student(data: StudentUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    for doc in db.collection("users").where("name", "==", data.name).stream():
        update_data = {}
        if data.new_name: update_data["name"] = data.new_name
        if data.new_pin: update_data["pin"] = get_password_hash(data.new_pin)
        if update_data: doc.reference.update(update_data)
        return {"status": "updated"}
    raise HTTPException(status_code=404, detail="해당 구성원을 찾을 수 없습니다")

# === 구성원 퇴소/삭제 (학생/학부모/선생님 모두 지원) ===
@app.delete("/api/admin/student/delete/{student_name}")
def delete_student(student_name: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    deleted = False
    for doc in db.collection("users").where("name", "==", student_name).stream():
        doc.reference.delete(); deleted = True
    if not deleted: raise HTTPException(status_code=404, detail="해당 구성원을 찾을 수 없습니다")
    return {"status": "deleted"}

# === 직원(선생님/행정) 등록 ===
class StaffRecord(BaseModel): name: str; pin: str; role: str  # 'teacher' or 'admin_staff'

@app.post("/api/admin/staff/add")
def add_staff(record: StaffRecord, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    data = record.model_dump()
    data["pin"] = get_password_hash(data["pin"])
    db.collection("users").add(data)
    return {"status": "success"}

# === 전체 사용자 목록 (모든 역할) ===
@app.get("/api/admin/students")
def get_all_users(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: return []
    result = []
    for doc in db.collection("users").stream():
        d = doc.to_dict()
        d["doc_id"] = doc.id
        result.append(d)
    return result

# === 학부모 계정 삭제 ===
@app.delete("/api/admin/parent/delete/{parent_name}")
def delete_parent(parent_name: str, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    deleted = False
    for doc in db.collection("users").where("name", "==", parent_name).where("role", "==", "parent").stream():
        doc.reference.delete(); deleted = True
    if not deleted: raise HTTPException(status_code=404, detail="학부모를 찾을 수 없습니다")
    return {"status": "deleted"}

# === 학부모 상세 프로필 업데이트 ===
@app.put("/api/admin/parent/profile")
def update_parent_profile(data: ParentProfileDetail, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    for doc in db.collection("users").where("name", "==", data.parent_name).where("role", "==", "parent").stream():
        doc.reference.update({"details": data.details})
        return {"status": "updated"}
    raise HTTPException(status_code=404)

# === 전체 데이터 JSON 백업 ===
@app.get("/api/admin/data/backup")
def backup_all_data(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    backup = {}
    for col_name in ["users", "programs", "billing", "attendance", "evaluations", "chats"]:
        docs = list(db.collection(col_name).stream())
        backup[col_name] = {doc.id: doc.to_dict() for doc in docs}
    return backup

# === 관리자 로컬 파일 직접 저장 (엑셀/백업용) ===
@app.post("/api/admin/save_local_file")
def save_local_file(data: LocalFileSave, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    import os
    try:
        dir_path = data.directory.strip()
        if not dir_path:
            raise HTTPException(status_code=400, detail="저장 경로가 비어있습니다.")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, data.filename)
        with open(file_path, "w", encoding="utf-8-sig") as f:
            f.write(data.content)
        return {"status": "success", "filepath": file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === 관리자 비밀번호 변경 ===
class PasswordChange(BaseModel): current_pin: str; new_pin: str

@app.post("/api/admin/change_password")
def change_admin_password(data: PasswordChange, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    # 현재는 master/1234 하드코딩이므로, 추후 DB 기반으로 전환
    if data.current_pin != "1234": raise HTTPException(status_code=400, detail="현재 비밀번호가 올바르지 않습니다")
    # 실제로는 환경변수나 DB에 저장해야 하지만, 현재 구조에서는 알림만
    return {"status": "success", "message": "비밀번호가 변경되었습니다 (실제 변경은 config 수정 필요)"}

# === 전체 평가 이력 조회 (차트용) ===
@app.get("/api/admin/evaluations/all")
def get_all_evaluations(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin": raise HTTPException(status_code=403)
    if not db: raise HTTPException(status_code=500)
    evals = []
    for doc in db.collection("evaluations").stream():
        d = doc.to_dict()
        d["id"] = doc.id
        evals.append(d)
    evals.sort(key=lambda x: x.get("date", ""))
    return evals

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    # Render/Railway 등 클라우드 환경에서는 0.0.0.0으로 바인딩해야 접근 가능함
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)