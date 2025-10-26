import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

st.title("Firebase Test")

try:
    if not firebase_admin._apps:
        cred_dict = dict(st.secrets["firebase"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    # Test write to Firestore
    db.collection("test").document("connection").set({
        "status": "working", 
        "timestamp": "test"
    })
    
    st.success("✅ Firebase Firestore is working!")
    
except Exception as e:
    st.error(f"❌ Error: {e}")
