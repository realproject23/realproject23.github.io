import firebase_admin
from firebase_admin import credentials, firestore

try:
    cred = credentials.Certificate("serviceAccountKey.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    # 1. Update Kim Soo-ah to have 2 programs
    # Programs IDs: 고독한 독서가, 봉사활동을 하자
    docs = list(db.collection("users").where("name", "==", "김수아").stream())
    if docs:
        for doc in docs:
            # Add both programs to the list
            doc.reference.update({
                "programs": ["고독한 독서가", "봉사활동을 하자"],
                "program": "고독한 독서가" # Legacy field for safety
            })
            print(f"Updated {doc.id} (김수아) with 2 programs.")
    else:
        print("User 김수아 not found.")

except Exception as e:
    print(f"Error: {e}")
