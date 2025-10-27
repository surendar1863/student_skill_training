import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import json

# ---------------- FIREBASE CONNECTION ----------------
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------------- FETCH DATA ----------------
docs = db.collection("student_responses").stream()
records = []

for doc in docs:
    data = doc.to_dict()
    roll = data.get("Roll")
    name = data.get("Name")
    section = data.get("Section")
    timestamp = data.get("Timestamp")
    for r in data.get("Responses", []):
        records.append({
            "Roll": roll,
            "Name": name,
            "Section": section,
            "Timestamp": timestamp,
            "QuestionID": r.get("QuestionID"),
            "Question": r.get("Question"),
            "Response": r.get("Response"),
            "Type": r.get("Type")
        })

