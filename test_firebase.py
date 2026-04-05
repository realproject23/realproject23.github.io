import firebase_admin
from firebase_admin import credentials, firestore
import json

try:
    cred = credentials.Certificate("serviceAccountKey.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    
    # Check programs
    print("--- Programs in Firebase ---")
    programs = list(db.collection("programs").stream())
    if not programs:
        print("No programs found in 'programs' collection.")
    else:
        for p in programs:
            print(f"ID: {p.id}, Data: {p.to_dict().get('name')}")
            
    # Check users
    print("\n--- Student Users in Firebase ---")
    users = list(db.collection("users").where("role", "==", "student").stream())
    if not users:
        print("No student users found.")
    else:
        for u in users:
            print(f"User: {u.to_dict().get('name')}, Program: {u.to_dict().get('program')}")

except Exception as e:
    print(f"Error connecting to Firebase: {e}")
