import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

st.set_page_config(page_title="Student Edge Assessment", layout="wide")
st.title("🎓 Student Edge Assessment Portal")

# ---------------------- FIREBASE INITIALIZATION ----------------------
@st.cache_resource
def init_firebase():
    try:
        if not firebase_admin._apps:
            # Use the credentials from secrets.toml
            cred_dict = {
                "type": st.secrets["firebase"]["type"],
                "project_id": st.secrets["firebase"]["project_id"],
                "private_key_id": st.secrets["firebase"]["private_key_id"],
                "private_key": st.secrets["firebase"]["private_key"],
                "client_email": st.secrets["firebase"]["client_email"],
                "client_id": st.secrets["firebase"]["client_id"],
                "auth_uri": st.secrets["firebase"]["auth_uri"],
                "token_uri": st.secrets["firebase"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
            }
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        st.error(f"❌ Firebase initialization failed: {e}")
        return None

db = init_firebase()

# ---------------------- STUDENT FORM ----------------------
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
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "Timestamp": timestamp,
            "Name": name,
            "Roll": roll,
            "Section": section,
            "Responses": {"Q1": q1, "Q2": q2},
        }

        try:
            if db:
                # Save to Firestore
                db.collection("student_responses").document(f"{roll}_{section}").set(data)
                st.success("✅ Data saved to Firebase successfully!")
                st.balloons()
            else:
                st.error("❌ Database connection failed")
                
        except Exception as e:
            st.error(f"❌ Error saving data: {e}")
