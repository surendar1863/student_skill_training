import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import gspread
import time

st.set_page_config(page_title="Student Edge Assessment", layout="wide")
st.title("🎓 Student Edge Assessment Portal")

# 1️⃣ Initialize Firebase
try:
    key_dict = dict(st.secrets["google_service_account"])
    cred = credentials.Certificate(key_dict)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    st.success("✅ Firestore connected successfully.")
except Exception as e:
    st.error(f"❌ Firebase connection failed: {e}")
    st.stop()

# 2️⃣ Connect Google Sheet
def connect_sheet():
    try:
        gc = gspread.service_account_from_dict(st.secrets["google_service_account"])
        sh = gc.open("Student_Responses")  # Must exist in your Drive
        return sh.sheet1
    except Exception as e:
        st.error(f"⚠️ Could not connect to Google Sheet: {e}")
        return None

sheet = connect_sheet()

# 3️⃣ Student Form
with st.form("student_form", clear_on_submit=True):
    st.subheader("🧾 Fill in your details")
    name = st.text_input("Full Name")
    roll = st.text_input("Roll Number (e.g., 23BCAR105)")
    section = st.selectbox("Section", ["Aptitude", "Communication Skills", "Adaptability"])
    q1 = st.text_area("Describe a situation where you solved a problem creatively:")
    q2 = st.slider("Rate your adaptability (1–5)", 1, 5, 3)
    submitted = st.form_submit_button("Submit ✅")

if submitted:
    if not name or not roll:
        st.warning("⚠️ Please fill all details before submitting.")
    else:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "Timestamp": timestamp,
            "Name": name,
            "Roll": roll,
            "Section": section,
            "Q1": q1,
            "Q2": q2
        }
        try:
            # Save to Firestore
            db.collection("student_responses").document(f"{roll}_{section}").set(data)
            # Save to Sheet
            if sheet:
                sheet.append_row([timestamp, name, roll, section, q1, q2])
            st.success("✅ Response recorded successfully!")
        except Exception as e:
            st.error(f"❌ Failed to save data: {e}")
