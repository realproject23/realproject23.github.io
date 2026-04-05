import firebase_admin
from firebase_admin import credentials, firestore

try:
    cred = credentials.Certificate("serviceAccountKey.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    print("--- Programs workflow check ---")
    docs = db.collection("programs").stream()
    for doc in docs:
        d = doc.to_dict()
        print(f"Program: {d.get('name')}")
        print(f"Workflow: {d.get('workflow')}")
        print("---")

except Exception as e:
    print(f"Error: {e}")
