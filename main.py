import streamlit as st
import pandas as pd
import time
import json
import firebase_admin
from firebase_admin import credentials, firestore

st.set_page_config(page_title="Student Edge – Submit", layout="wide")
st.title("🧠 Student Edge Assessment Portal")

# ---------- Firebase init (Firestore only) ----------
def get_firestore():
    try:
        key_dict = dict(st.secrets["google_service_account"])
        # normalize PEM newlines (prevents Invalid JWT Signature)
        key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(key_dict)
    except Exception:
        # optional local fallback if you ever run locally with a file:
        cred = credentials.Certificate("firebase_key.json")

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = get_firestore()

# ---------- CSV files per section ----------
files = {
    "Aptitude Test": "aptitude.csv",
    "Adaptability & Learning": "adaptability_learning.csv",
    "Communication Skills - Objective": "communcation_skills_objective.csv",
    "Communication Skills - Descriptive": "communcation_skills_descriptive.csv",
}

# ---------- Student details ----------
name = st.text_input("Enter Your Name")
roll = st.text_input("Enter Roll Number (e.g., 25BBAB170)")

if not (name and roll):
    st.info("👆 Please enter your Name and Roll Number to start.")
    st.stop()

section = st.selectbox("Select Section", list(files.keys()))
if not section:
    st.stop()

df = pd.read_csv(files[section])
st.subheader(f"📘 {section}")
st.write("Answer all the questions below and click **Submit**.")

responses = []
for idx, row in df.iterrows():
    qid = row.get("QuestionID", f"Q{idx+1}")
    text = str(row.get("Question", "")).strip()
    qtype = str(row.get("Type", "")).strip().lower()

    if qtype == "info":
        st.markdown(f"### 📝 {text}")
        st.markdown("---")
        continue

    st.markdown(f"**Q{idx+1}. {text}**")

    if qtype == "likert":
        v = st.slider("Your Response:", 1, 5, 3, key=f"q{idx}")
    elif qtype == "mcq":
        options = [str(row.get(f"Option{i}", "")).strip()
                   for i in range(1, 5)
                   if pd.notna(row.get(f"Option{i}")) and str(row.get(f"Option{i}")).strip()]
        v = st.radio("Your Answer:", options, key=f"q{idx}") if options else ""
    else:  # short / descriptive
        v = st.text_area("Your Answer:", key=f"q{idx}")

    responses.append({"QuestionID": qid, "Question": text, "Response": v, "Type": qtype})
    st.markdown("---")

# ---------- Submit ----------
if st.button("✅ Submit"):
    with st.spinner("Saving your responses..."):
        data = {
            "Name": name,
            "Roll": roll,
            "Section": section,
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "Responses": responses,
        }
        try:
            # Use a doc per (Roll, Section)
            doc_id = f"{roll}_{section.replace(' ', '_')}"
            db.collection("student_responses").document(doc_id).set(data)
            st.success("✅ Saved to Firestore.")
        except Exception as e:
            st.error(f"❌ Firestore save error: {e}")
