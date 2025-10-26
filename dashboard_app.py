import streamlit as st
import pandas as pd
import io
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

st.set_page_config(page_title="Faculty Evaluation Dashboard", layout="wide")
st.title("🎓 Faculty Evaluation Dashboard")

# ---------- Firebase init ----------
def get_firestore():
    try:
        key_dict = dict(st.secrets["google_service_account"])
        key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(key_dict)
    except Exception:
        cred = credentials.Certificate("firebase_key.json")
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = get_firestore()

# ---------- Load student responses from Firestore ----------
docs = list(db.collection("student_responses").stream())
if not docs:
    st.warning("No student data found in Firestore.")
    st.stop()

rows = []
for d in docs:
    rec = d.to_dict()
    for r in rec.get("Responses", []):
        if str(r.get("Type", "")).lower() in ["mcq", "info"]:
            continue  # faculty grades only non-auto
        rows.append({
            "Name": rec.get("Name"),
            "Roll": rec.get("Roll"),
            "Section": rec.get("Section"),
            "QuestionID": r.get("QuestionID"),
            "Question": r.get("Question"),
            "Response": r.get("Response"),
            "Type": r.get("Type"),
            "Timestamp": rec.get("Timestamp"),
        })

df = pd.DataFrame(rows)
if df.empty:
    st.info("No gradable questions found.")
    st.stop()

rolls = sorted(df["Roll"].unique().tolist())
selected_roll = st.selectbox("Select Student Roll Number", rolls)
student_df = df[df["Roll"] == selected_roll]

st.subheader(f"📋 Evaluation for {student_df.iloc[0]['Name']} ({selected_roll})")

# ---------- Marks entry ----------
marks_state = {}
sections = student_df["Section"].unique().tolist()
grand_total = 0
grand_max = 0

for section in sections:
    sec_df = student_df[student_df["Section"] == section]
    st.markdown(f"## 🧾 {section}")

    section_total = 0
    section_max = len(sec_df)
    q_counter = 0

    for _, row in sec_df.sort_values("QuestionID").iterrows():
        q_counter += 1
        qid = row["QuestionID"]
        qtext = row["Question"]
        resp = "" if pd.isna(row["Response"]) else str(row["Response"])

        col1, col2 = st.columns([10, 2])
        with col1:
            st.markdown(f"**Q{q_counter}: {qtext}**")
            st.markdown(f"🧩 *Student Response:* **{resp}**")
        with col2:
            marks_state[(selected_roll, qid)] = st.radio(
                label="", options=[0, 1], index=0, horizontal=True,
                key=f"{selected_roll}_{section}_{qid}"
            )
            section_total += marks_state[(selected_roll, qid)]

    st.markdown(f"**Subtotal for {section}: {section_total}/{section_max}**")
    st.markdown("---")
    grand_total += section_total
    grand_max += section_max

st.metric("🏅 Total Marks (All Sections)", f"{grand_total}/{grand_max}")

# ---------- Save marks to Firestore ----------
if st.button("💾 Save All Marks"):
    try:
        batch = db.batch()
        for (roll, qid), mark in marks_state.items():
            doc_id = f"{roll}_{qid}"
            ref = db.collection("faculty_marks").document(doc_id)
            batch.set(ref, {
                "Roll": roll,
                "QuestionID": qid,
                "Marks": int(mark),
                "Evaluator": "Faculty",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        batch.commit()
        st.success("✅ All marks saved.")
    except Exception as e:
        st.error(f"❌ Failed to save marks: {e}")

# ---------- Export all data to Excel ----------
st.markdown("### ⬇️ Export to Excel")
expander = st.expander("Preview export data")
expander.dataframe(df, use_container_width=True)

output = io.BytesIO()
with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Responses", index=False)
excel_bytes = output.getvalue()

st.download_button(
    "📥 Download Excel",
    data=excel_bytes,
    file_name=f"student_responses_{datetime.now():%Y%m%d_%H%M}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
