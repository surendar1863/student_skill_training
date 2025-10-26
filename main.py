import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import gspread
from datetime import datetime

st.set_page_config(page_title="Student Edge Assessment", layout="wide")
st.title("🎓 Student Edge Assessment Portal")

# ---------------------- FIREBASE ----------------------
@st.cache_resource
def init_firebase():
    try:
        # Check if secrets exist
        if "firebase" not in st.secrets:
            st.error("❌ Firebase secrets not found in Streamlit secrets")
            return None
        
        # Create service account dict from secrets
        service_account_info = {
            "type": "service_account",
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        }
        
        # Initialize Firebase
        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred)
        
        return firestore.client()
    except Exception as e:
        st.error(f"❌ Firebase initialization failed: {str(e)}")
        return None

db = init_firebase()

# ---------------------- GOOGLE SHEETS ----------------------
@st.cache_resource
def connect_sheet(sheet_name="Student_Responses"):
    try:
        # Use the same service account for Sheets
        service_account_info = {
            "type": "service_account",
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        }
        
        gc = gspread.service_account_from_dict(service_account_info)
        sh = gc.open(sheet_name)
        return sh.sheet1
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

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "Timestamp": timestamp,
        "Name": name,
        "Roll": roll,
        "Section": section,
        "Responses": {"Q1": q1, "Q2": q2},
    }

    success_firestore = False
    success_sheets = False

    try:
        # Save to Firestore
        if db:
            db.collection("student_responses").document(f"{roll}_{section}").set(data)
            success_firestore = True
            st.success("✅ Data saved to Firestore")
        else:
            st.warning("⚠️ Firebase not available - skipping Firestore save")
    except Exception as e:
        st.error(f"❌ Firestore save error: {e}")

    try:
        # Save to Google Sheet
        if sheet:
            sheet.append_row([timestamp, name, roll, section, q1, str(q2)])
            success_sheets = True
            st.success("✅ Data saved to Google Sheets")
        else:
            st.warning("⚠️ Google Sheets not available - skipping Sheets save")
    except Exception as e:
        st.error(f"❌ Google Sheets save error: {e}")

    if success_firestore and success_sheets:
        st.balloons()
        st.success("🎉 Submission saved successfully to both Firestore and Google Sheets!")
    elif success_firestore or success_sheets:
        st.info("📝 Submission partially saved (check above for details)")
    else:
        st.error("❌ Failed to save data. Please try again.")
