import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
import pandas as pd

# -------------------------------
# STREAMLIT CONFIG
# -------------------------------
st.set_page_config(page_title="Faculty Text Evaluation", layout="wide")

# Hide Streamlit default UI
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
[data-testid="stToolbar"] {display:none;}
[data-testid="stHeader"] {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# -------------------------------
# FIREBASE INITIALIZATION
# -------------------------------
@st.cache_resource
def init_firebase():
    try:
        if firebase_admin._apps:
            return firestore.client()

        if "firebase" in st.secrets:
            config = st.secrets["firebase"]

            # Fix escaped newlines if present
            if "\\n" in config["private_key"]:
                config["private_key"] = config["private_key"].replace("\\n", "\n")

            cred = credentials.Certificate(config)
            firebase_admin.initialize_app(cred)
            return firestore.client()

        st.error("Firebase configuration NOT found under [firebase] in secrets.toml!")
        return None

    except Exception as e:
        st.error(f"Firebase initialization failed: {e}")
        return None


db = init_firebase()

if not db:
    st.stop()

st.success("Connected to Firebase!")

# -------------------------------
# LOAD QUESTION FILE
# -------------------------------
uploaded_csv = st.file_uploader("Upload the test CSV file:", type=["csv"])

if uploaded_csv:
    df_questions = pd.read_csv(uploaded_csv)
    st.write("### Questions Loaded:")
    st.dataframe(df_questions)

    # Filter only descriptive questions
    descriptive_qs = df_questions[df_questions["Type"] == "text"]

    if descriptive_qs.empty:
        st.warning("No descriptive questions found in the CSV!")
        st.stop()

    # -------------------------------
    # SELECT TEST COLLECTION
    # -------------------------------
    st.subheader("Select Firestore Test Collection")
    collections = [c.id for c in db.collections()]

    test_name = st.selectbox("Choose Test:", collections)

    if test_name:
        st.subheader(f"Evaluating: {test_name}")

        students = list(db.collection(test_name).stream())
        roll_numbers = [s.id for s in students]

        selected_roll = st.selectbox("Select Student Roll Number:", roll_numbers)

        if selected_roll:

            doc = db.collection(test_name).document(selected_roll).get()
            data = doc.to_dict()

            st.markdown(f"### 🧑‍🎓 Student Name: **{data.get('Name','Unknown')}**")
