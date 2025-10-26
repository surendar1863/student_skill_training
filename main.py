import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime
from io import BytesIO
import json
import os

st.set_page_config(page_title="Student Edge Assessment", layout="wide")
st.title("🎓 Student Edge Assessment Portal")

# ---------------------- FIREBASE SETUP ----------------------
@st.cache_resource
def init_firebase():
    try:
        # Method 1: Check for service account JSON file
        if os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")
        # Method 2: Check for secrets as fallback
        elif "firebase" in st.secrets:
            cred_dict = {
                "type": st.secrets["firebase"]["type"],
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
            cred = credentials.Certificate(cred_dict)
        else:
            st.error("❌ No Firebase credentials found. Please add serviceAccountKey.json file.")
            return None
        
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        
        st.success("✅ Firebase connected successfully!")
        return firestore.client()
        
    except Exception as e:
        st.error(f"❌ Firebase initialization failed: {str(e)}")
        st.info("💡 Please check your service account credentials")
        return None

db = init_firebase()

# ---------------------- LOCAL JSON BACKUP ----------------------
def save_to_local_backup(data):
    """Save data to local JSON file as backup"""
    try:
        backup_file = "local_responses.json"
        
        # Load existing data
        if os.path.exists(backup_file):
            with open(backup_file, 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []
        
        # Add new data
        existing_data.append(data)
        
        # Save back to file
        with open(backup_file, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        return True
    except Exception as e:
        st.error(f"Local backup failed: {e}")
        return False

def get_local_data():
    """Get data from local backup"""
    try:
        backup_file = "local_responses.json"
        if os.path.exists(backup_file):
            with open(backup_file, 'r') as f:
                return json.load(f)
        return []
    except:
        return []

# ---------------------- DOWNLOAD FUNCTIONS ----------------------
def download_excel_from_firestore():
    """Download data from Firestore as Excel"""
    try:
        if not db:
            return None
            
        responses_ref = db.collection("student_responses")
        docs = responses_ref.stream()
        
        data = []
        for doc in docs:
            doc_data = doc.to_dict()
            data.append({
                "Timestamp": doc_data.get("Timestamp", ""),
                "Name": doc_data.get("Name", ""),
                "Roll Number": doc_data.get("Roll", ""),
                "Section": doc_data.get("Section", ""),
                "Problem Solving Response": doc_data.get("Responses", {}).get("Q1", ""),
                "Adaptability Rating": doc_data.get("Responses", {}).get("Q2", "")
            })
        
        if data:
            df = pd.DataFrame(data)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Student Responses', index=False)
            output.seek(0)
            return output
        return None
    except Exception as e:
        st.error(f"Firestore download error: {e}")
        return None

def download_excel_from_local():
    """Download data from local backup as Excel"""
    try:
        local_data = get_local_data()
        if local_data:
            # Convert to the same format
            formatted_data = []
            for item in local_data:
                formatted_data.append({
                    "Timestamp": item.get("Timestamp", ""),
                    "Name": item.get("Name", ""),
                    "Roll Number": item.get("Roll", ""),
                    "Section": item.get("Section", ""),
                    "Problem Solving Response": item.get("Responses", {}).get("Q1", ""),
                    "Adaptability Rating": item.get("Responses", {}).get("Q2", "")
                })
            
            df = pd.DataFrame(formatted_data)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Student Responses', index=False)
            output.seek(0)
            return output
        return None
    except Exception as e:
        st.error(f"Local download error: {e}")
        return None

# ---------------------- ADMIN PANEL ----------------------
st.sidebar.title("📊 Admin Panel")

# Download from Firestore
if st.sidebar.button("📥 Download from Firestore"):
    excel_file = download_excel_from_firestore()
    if excel_file:
        st.sidebar.download_button(
            label="⬇️ Download Firestore Data",
            data=excel_file,
            file_name=f"firestore_responses_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.sidebar.warning("No data in Firestore")

# Download from local backup
if st.sidebar.button("💾 Download Local Backup"):
    excel_file = download_excel_from_local()
    if excel_file:
        st.sidebar.download_button(
            label="⬇️ Download Local Data",
            data=excel_file,
            file_name=f"local_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.sidebar.warning("No local backup data")

# Show data statistics
local_data = get_local_data()
if local_data:
    st.sidebar.info(f"📈 Local backup: {len(local_data)} responses")

# ---------------------- STUDENT FORM ----------------------
st.header("📝 Student Response Form")

with st.form("student_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name *")
        roll = st.text_input("Roll Number * (e.g., 25BCAR123)")
    
    with col2:
        section = st.selectbox("Section *", 
                             ["Aptitude", "Communication Skills", "Adaptability"])
        q2 = st.slider("Rate your adaptability to change (1-5) *", 1, 5, 3)
    
    q1 = st.text_area("Describe a situation where you solved a problem creatively. *", 
                     height=120,
                     placeholder="Share a specific example of how you approached and solved a challenging problem...")
    
    submitted = st.form_submit_button("Submit Response ✅")

if submitted:
    if not all([name, roll, q1]):
        st.warning("⚠️ Please fill all required fields (marked with *)")
        st.stop()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "Timestamp": timestamp,
        "Name": name.strip(),
        "Roll": roll.strip().upper(),
        "Section": section,
        "Responses": {
            "Q1": q1.strip(),
            "Q2": q2
        },
    }

    success = False
    
    # Try Firestore first
    if db:
        try:
            doc_ref = db.collection("student_responses").document(f"{roll}_{section}")
            doc_ref.set(data)
            st.success("✅ Response submitted to Firestore!")
            success = True
        except Exception as e:
            st.error(f"❌ Firestore save failed: {e}")
    
    # Always save to local backup
    if save_to_local_backup(data):
        st.success("✅ Response saved to local backup!")
        success = True
    
    if success:
        st.balloons()
        st.info(f"""
        **Submission Confirmed:**
        - Name: {name}
        - Roll Number: {roll}
        - Section: {section}
        - Time: {timestamp}
        """)
    else:
        st.error("❌ Failed to save data. Please contact administrator.")
