import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="Student Edge Assessment", layout="wide")
st.title("🎓 Student Edge Assessment Portal")

# ---------------------- FIREBASE ONLY ----------------------
@st.cache_resource
def init_firebase():
    try:
        if not firebase_admin._apps:
            # Use a simpler approach with direct secrets
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
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        st.error(f"❌ Firebase init failed: {e}")
        return None

db = init_firebase()

# ---------------------- DOWNLOAD DATA AS EXCEL ----------------------
def download_excel():
    try:
        if not db:
            st.error("Firebase not connected")
            return None
            
        # Get all data from Firestore
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
            
            # Create Excel file in memory
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Student Responses', index=False)
                
                # Auto-adjust column widths
                worksheet = writer.sheets['Student Responses']
                for i, col in enumerate(df.columns):
                    max_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
                    worksheet.set_column(i, i, max_len)
            
            output.seek(0)
            return output
        else:
            st.warning("No data available to download")
            return None
    except Exception as e:
        st.error(f"Error generating Excel file: {e}")
        return None

# ---------------------- ADMIN DOWNLOAD SECTION ----------------------
st.sidebar.title("Admin Panel")
if st.sidebar.button("📥 Download Excel Report"):
    excel_file = download_excel()
    if excel_file:
        st.sidebar.download_button(
            label="⬇️ Download Excel File",
            data=excel_file,
            file_name=f"student_responses_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ---------------------- STUDENT FORM ----------------------
st.header("Student Response Form")

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

    try:
        # Save to Firestore only
        doc_ref = db.collection("student_responses").document(f"{roll}_{section}")
        doc_ref.set(data)
        
        st.success("✅ Response submitted successfully!")
        st.balloons()
        
        # Show confirmation
        st.info(f"""
        **Submission Details:**
        - Name: {name}
        - Roll Number: {roll}
        - Section: {section}
        - Submitted at: {timestamp}
        """)
        
    except Exception as e:
        st.error(f"❌ Error saving data: {e}")
        st.info("Please try again in a few moments.")

# ---------------------- LIVE DATA PREVIEW ----------------------
st.sidebar.header("Data Preview")
if st.sidebar.button("🔄 Refresh Data"):
    try:
        responses_ref = db.collection("student_responses")
        docs = responses_ref.limit(5).stream()  # Show last 5 entries
        
        recent_data = []
        for doc in docs:
            doc_data = doc.to_dict()
            recent_data.append(doc_data)
        
        if recent_data:
            st.sidebar.write("**Recent Submissions:**")
            for data in recent_data:
                st.sidebar.write(f"• {data.get('Name')} - {data.get('Roll')}")
        else:
            st.sidebar.write("No submissions yet")
    except Exception as e:
        st.sidebar.error("Error loading data")
