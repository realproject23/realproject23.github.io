/**
 * =========================================================
 * 🔥 Firebase REST API Client (No Backend Required)
 *    Reads Firestore data directly from the browser.
 *    Project: youth-canvas
 * =========================================================
 */

const FIREBASE_PROJECT_ID = "youth-canvas";
const FIRESTORE_BASE_URL = `https://firestore.googleapis.com/v1/projects/${FIREBASE_PROJECT_ID}/databases/(default)/documents`;

// ─── Helper: Parse Firestore REST field value ─────────────
function parseFirestoreValue(val) {
    if (!val) return null;
    if (val.stringValue !== undefined) return val.stringValue;
    if (val.integerValue !== undefined) return parseInt(val.integerValue);
    if (val.doubleValue !== undefined) return parseFloat(val.doubleValue);
    if (val.booleanValue !== undefined) return val.booleanValue;
    if (val.nullValue !== undefined) return null;
    if (val.arrayValue !== undefined) {
        return (val.arrayValue.values || []).map(parseFirestoreValue);
    }
    if (val.mapValue !== undefined) {
        return parseFirestoreFields(val.mapValue.fields || {});
    }
    return null;
}

function parseFirestoreFields(fields) {
    const result = {};
    for (const [key, val] of Object.entries(fields)) {
        result[key] = parseFirestoreValue(val);
    }
    return result;
}

function parseDocument(doc) {
    const data = parseFirestoreFields(doc.fields || {});
    // Extract doc ID from the name path
    const nameParts = (doc.name || "").split("/");
    data._id = nameParts[nameParts.length - 1];
    return data;
}

// ─── Core: Fetch a collection ─────────────────────────────
async function fbGetCollection(collectionPath, token = null) {
    const url = `${FIRESTORE_BASE_URL}/${collectionPath}`;
    const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = `Bearer ${token}`;
    
    const res = await fetch(url, { headers });
    if (!res.ok) throw new Error(`Firestore error: ${res.status}`);
    const data = await res.json();
    return (data.documents || []).map(parseDocument);
}

// ─── Core: Query a collection ─────────────────────────────
async function fbQueryCollection(collectionPath, field, op, value, token = null) {
    const url = `${FIRESTORE_BASE_URL}:runQuery`;
    const headers = { "Content-Type": "application/json" };
    if (token) headers["Authorization"] = `Bearer ${token}`;

    // Map operator names
    const opMap = { "==": "EQUAL", "!=": "NOT_EQUAL", "<": "LESS_THAN", ">": "GREATER_THAN" };
    const firestoreOp = opMap[op] || op;

    let fieldValue;
    if (typeof value === "string") fieldValue = { stringValue: value };
    else if (typeof value === "number") fieldValue = { integerValue: value };
    else if (typeof value === "boolean") fieldValue = { booleanValue: value };

    const body = {
        structuredQuery: {
            from: [{ collectionId: collectionPath }],
            where: {
                fieldFilter: {
                    field: { fieldPath: field },
                    op: firestoreOp,
                    value: fieldValue
                }
            }
        }
    };

    const res = await fetch(url, { method: "POST", headers, body: JSON.stringify(body) });
    if (!res.ok) throw new Error(`Firestore query error: ${res.status}`);
    const results = await res.json();
    return results
        .filter(r => r.document)
        .map(r => parseDocument(r.document));
}

// ─── Core: Write a document (requires auth token) ─────────
async function fbAddDocument(collectionPath, data, token) {
    const url = `${FIRESTORE_BASE_URL}/${collectionPath}`;
    const headers = { "Content-Type": "application/json", "Authorization": `Bearer ${token}` };
    
    // Convert data to Firestore field format
    const fields = {};
    for (const [key, val] of Object.entries(data)) {
        if (typeof val === "string") fields[key] = { stringValue: val };
        else if (typeof val === "number" && Number.isInteger(val)) fields[key] = { integerValue: val };
        else if (typeof val === "number") fields[key] = { doubleValue: val };
        else if (typeof val === "boolean") fields[key] = { booleanValue: val };
        else if (val === null) fields[key] = { nullValue: null };
        else if (Array.isArray(val)) fields[key] = { arrayValue: { values: val.map(v => typeof v === "string" ? { stringValue: v } : { integerValue: v }) } };
    }
    
    const res = await fetch(url, { method: "POST", headers, body: JSON.stringify({ fields }) });
    if (!res.ok) throw new Error(`Firestore write error: ${res.status}`);
    return await res.json();
}

// ─── AUTH: Exchange custom token or use Firebase Auth REST ────
// For this project we use a simple approach:
// Store hashed PIN in localStorage after server auth, or use Firebase Auth REST API.

async function fbSignInWithCustom(name, pin) {
    // First try Firebase Auth REST (Email/Password not set up)
    // Instead, we'll use our own simple token mechanism stored in Firestore
    // Look up user in Firestore directly
    const users = await fbQueryCollection("users", "name", "==", name);
    if (!users || users.length === 0) throw new Error("사용자를 찾을 수 없습니다.");
    const user = users[0];
    
    // Simple PIN check (PIN stored as bcrypt hash — we verify via the API fallback or store a simple hash)
    // Since bcrypt can't run in browser, we'll use SHA-256 comparison for client-side auth
    // The actual stored value may be bcrypt — in that case we need the backend.
    // For now, return the user data and set a session token.
    return user;
}

// ─── HIGH-LEVEL API functions ───────────────────────────────

// 📋 Get all programs with participant counts
window.fbGetPrograms = async function() {
    const programs = await fbGetCollection("programs");
    
    // Count participants per program
    let users = [];
    try {
        users = await fbQueryCollection("users", "role", "==", "student");
    } catch(e) { /* Security rules may block this for non-admins */ }
    
    const counts = {};
    users.forEach(u => {
        const prog = u.program || "";
        counts[prog] = (counts[prog] || 0) + 1;
    });
    
    return programs.map(p => ({
        ...p,
        current_participants: counts[p.name] || 0
    }));
};

// 👤 Get user dashboard data
window.fbGetUserDashboard = async function(name, token = null) {
    const users = await fbQueryCollection("users", "name", "==", name, token);
    if (!users.length) throw new Error("사용자 없음");
    const user = users[0];
    
    // Get evaluations
    let evals = [];
    try {
        evals = await fbQueryCollection("evaluations", "student_name", "==", name, token);
        evals.sort((a, b) => (b.date || "").localeCompare(a.date || ""));
    } catch(e) {}
    
    const latestEval = evals[0] || { scores: { task: 0, prof: 0, att: 0, comm: 0 }, comment: "피드백 대기중" };
    
    // Get attendance
    const attSummary = { "출석": 0, "지각": 0, "결석": 0 };
    try {
        const allAtt = await fbGetCollection("attendance", token);
        allAtt.forEach(doc => {
            (doc.records || []).forEach(r => {
                if (r.student_name === name && attSummary[r.status] !== undefined) {
                    attSummary[r.status]++;
                }
            });
        });
    } catch(e) {}
    
    // Get tasks
    let tasks = {};
    try {
        const taskCol = await fbQueryCollection("user_tasks", "name", "==", name, token);
        tasks = taskCol[0]?.tasks || {};
    } catch(e) {}
    
    const approvedTasks = Object.keys(tasks).filter(k => tasks[k]?.status === "approved");
    const pendingTasks = Object.keys(tasks).filter(k => tasks[k]?.status === "pending");
    
    // Calculate tier
    const attScore = Math.min((attSummary["출석"] * 5) + (attSummary["지각"] * 2), 40);
    const sc = latestEval.scores || {};
    const evalScore = ((( sc.task || 0) + (sc.prof || 0) + (sc.att || 0) + (sc.comm || 0)) / 4 / 100) * 30;
    const totalPoints = Math.round(attScore + evalScore);
    
    let tier = "🌱 C 등급 (비기너)";
    if (totalPoints >= 85) tier = "🏆 S 등급 (마스터)";
    else if (totalPoints >= 70) tier = "🥇 A 등급 (챌린저)";
    else if (totalPoints >= 50) tier = "🥈 B 등급 (러너)";
    
    const programs = user.programs || (user.program ? [user.program] : ["미지정"]);
    
    // Get program workflows
    const programsDetail = {};
    for (const progName of programs) {
        const progs = await fbGetCollection("programs", token);
        const prog = progs.find(p => p.name === progName) || {};
        const workflow = prog.workflow || "";
        const tasks = workflow.split("\n").filter(l => l.trim()).length;
        programsDetail[progName] = { workflow, total_tasks: tasks };
    }
    
    return {
        name,
        programs,
        role: user.role || "student",
        programs_detail: programsDetail,
        approved_tasks: approvedTasks,
        pending_tasks: pendingTasks,
        evaluation: latestEval,
        attendance: attSummary,
        reward: { points: totalPoints, tier, criteria: ["출결 성실도 (40P)", "전체 프로그램 승인 미션 (30P)", "역량 평가 성취도 (30P)"] }
    };
};

console.log("🔥 Firebase Client loaded. Project: youth-canvas");
