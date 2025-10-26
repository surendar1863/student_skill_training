import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import gspread
import time

st.set_page_config(page_title="Student Edge Assessment", layout="wide")
st.title("🎓 Student Edge Assessment Portal")

# ---------------------- FIREBASE ----------------------
try:
    key_dict = dict(st.secrets["google_service_account"])
    cred = credentials.Certificate(key_dict)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    st.error(f"❌ Firebase init failed: {e}")
    st.stop()

# ---------------------- GOOGLE SHEETS ----------------------
def connect_sheet(sheet_name="Student_Responses"):
    try:
        gc = gspread.service_account_from_dict(st.secrets["google_service_account"])
        sh = gc.open(sheet_name)
        ws = sh.sheet1
        return ws
    except Exception as e:
        st.error(f"❌ Google Sheets connection failed: {e}")
        return None

sheet = connect_sheet()

# ---------------------- FORM ----------------------
with st.form("student_form"):
    name = st.text_input("Name")
    roll = st.text_input("Roll Number (e.g., 25BCAR123)")
    section = st.selectbox("Section", ["Aptitude", "Communication Skills", "Adaptability"])
    q1 = st.text_area("1️⃣ Describe a situation where you solved a problem creatively.")
    q2 = st.slider("2️⃣ Rate your adaptability to change (1–5)", 1, 5, 3)
    submitted = st.form_submit_button("Submit Response ✅")

if submitted:
    if not name or not roll:
        st.warning("⚠️ Please fill all details before submitting.")
        st.stop()

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "Timestamp": timestamp,
        "Name": name,
        "Roll": roll,
        "Section": section,
        "Responses": {"Q1": q1, "Q2": q2},
    }

    try:
        # Save to Firestore
        db.collection("student_responses").document(f"{roll}_{section}").set(data)

        # Save to Google Sheet (flat row)
        if sheet:
            sheet.append_row([timestamp, name, roll, section, "Q1", q1])
            sheet.append_row([timestamp, name, roll, section, "Q2", str(q2)])

        st.success("✅ Submission saved successfully (Firestore + Sheets).")
    except Exception as e:
        st.error(f"❌ Error saving data: {e}")
