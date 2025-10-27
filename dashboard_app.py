import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import json

import os
import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

def load_firebase_credentials():
    # 1) Streamlit secrets: stringified JSON (most common)
    if "firebase_key" in st.secrets:
        try:
            return credentials.Certificate(json.loads(st.secrets["firebase_key"]))
        except Exception:
            pass  # will try other forms

    # 2) Streamlit secrets: dict-style (e.g., [google_service_account] in secrets.toml)
    if "google_service_account" in st.secrets:
        try:
            return credentials.Certificate(dict(st.secrets["google_service_account"]))
        except Exception:
            pass

    # 3) Local file fallback (only works if file is actually deployed with the app)
    if os.path.exists("firebase_key.json"):
        return credentials.Certificate("firebase_key.json")

    # Nothing worked
    raise RuntimeError(
        "No Firebase credentials found. Add your service-account JSON to "
        "Streamlit Secrets as 'firebase_key' (stringified JSON) or "
        "as a [google_service_account] table, or deploy firebase_key.json with the app."
    )

# Initialize Firebase
cred = load_firebase_credentials()
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()


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


