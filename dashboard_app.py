import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Debug: Check current directory and files
st.write("## Debug Information")
st.write(f"Current working directory: `{os.getcwd()}`")
st.write(f"Files in directory: `{os.listdir('.')}`")

# Check if firebase_key.json exists
json_path = "firebase_key.json"
if os.path.exists(json_path):
    st.success(f"✅ Found: {json_path}")
    file_size = os.path.getsize(json_path)
    st.write(f"File size: {file_size} bytes")
else:
    st.error(f"❌ Missing: {json_path}")

# Try multiple initialization methods
try:
    # Method 1: Direct file path
    if os.path.exists(json_path):
        cred = credentials.Certificate(json_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        st.success("✅ Firebase connected via file!")
        
        # Test connection
        test_doc = db.collection('test').document('connection_test')
        st.success("✅ Firebase Firestore connection test passed!")
        
except Exception as e:
    st.error(f"❌ Method 1 failed: {str(e)}")
    
    try:
        # Method 2: Using secrets (for Streamlit Cloud)
        if 'FIREBASE_KEY' in st.secrets:
            firebase_config = st.secrets['FIREBASE_KEY']
            if isinstance(firebase_config, str):
                # If it's stored as string, parse it
                firebase_config = json.loads(firebase_config)
            
            cred = credentials.Certificate(firebase_config)
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
            db = firestore.client()
            st.success("✅ Firebase connected via secrets!")
            
    except Exception as e2:
        st.error(f"❌ Method 2 failed: {str(e2)}")

# Rest of your app code...
st.write("App continues...")
