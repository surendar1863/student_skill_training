import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.title("Firebase Connection Test")

try:
    if not firebase_admin._apps:
        # Use the credentials directly from secrets
        cred = credentials.Certificate(dict(st.secrets["firebase"]))
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    # Test connection
    db.collection("test").document("connection").set({"timestamp": "test", "status": "connected"})
    st.success("✅ Firebase connected successfully!")
    
except Exception as e:
    st.error(f"❌ Connection failed: {e}")
