import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import gspread
from datetime import datetime

st.set_page_config(page_title="Student Edge Assessment", layout="wide")
st.title("🎓 Student Edge Assessment Portal")

# Initialize Firebase
if not firebase_admin._apps:
    try:
        cred_dict = {
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        }
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Firebase init error: {e}")

db = firestore.client()

# Google Sheets setup
def init_sheets():
    try:
        gc = gspread.service_account_from_dict({
            "type": st.secrets["firebase"]["type"],
            "project_id": st.secrets["firebase"]["project_id"],
            "private_key_id": st.secrets["firebase"]["private_key_id"],
            "private_key": st.secrets["firebase"]["private_key"].replace('\\n', '\n'),
            "client_email": st.secrets["firebase"]["client_email"],
            "client_id": st.secrets["firebase"]["client_id"],
            "auth_uri": st.secrets["firebase"]["auth_uri"],
            "token_uri": st.secrets["firebase"]["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"]
        })
        sheet = gc.open("Student_Responses").sheet1
        return sheet
    except Exception as e:
        st.error(f"Sheets error: {e}")
        return None

sheet = init_sheets()

# Form
with st.form("student_form"):
    name = st.text_input("Name")
    roll = st.text_input("Roll Number")
    section = st.selectbox("Section", ["Aptitude", "Communication Skills", "Adaptability"])
    q1 = st.text_area("Describe a situation where you solved a problem creatively.")
    q2 = st.slider("Rate your adaptability to change (1-5)", 1, 5, 3)
    submitted = st.form_submit_button("Submit")

if submitted:
    if name and roll:
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": name,
            "roll": roll,
            "section": section,
            "q1": q1,
            "q2": q2
        }
        
        try:
            # Save to Firestore
            db.collection("responses").add(data)
            
            # Save to Sheets
            if sheet:
                sheet.append_row([data["timestamp"], name, roll, section, q1, q2])
            
            st.success("Data saved successfully!")
        except Exception as e:
            st.error(f"Save error: {e}")
    else:
        st.warning("Please fill name and roll number")
