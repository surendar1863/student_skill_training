import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import time

# ---------------- FIREBASE CONNECTION ----------------
@st.cache_resource
def init_firebase():
    try:
        if not firebase_admin._apps:
            # Use the CORRECT secret name that matches your secrets.toml
            cred_dict = dict(st.secrets["firebase"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        st.error(f"❌ Firebase initialization failed: {e}")
        return None

db = init_firebase()

# ---------------- CSV FILES ----------------
files = {
    "Aptitude Test": "aptitude.csv",
    "Adaptability & Learning": "adaptability_learning.csv",
    "Communication Skills - Objective": "communication_skills_objective.csv",
    "Communication Skills - Descriptive": "communication_skills_descriptive.csv",
}

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Student Edge Assessment", layout="wide")
st.title("🧠 Student Edge Assessment Portal")

# ---------------- STUDENT DETAILS ----------------
name = st.text_input("Enter Your Name")
roll = st.text_input("Enter Roll Number (e.g., 24bbab110)")

# ---------------- MAIN APP ----------------
if name and roll:
    st.success(f"Welcome, {name}! Please choose a test section below.")
    section = st.selectbox("Select Section", list(files.keys()))

    if section:
        try:
            df = pd.read_csv(files[section])
        except FileNotFoundError:
            st.error(f"❌ File '{files[section]}' not found. Please check the file name.")
            st.stop()

        st.subheader(f"📘 {section}")
        st.write("Answer all the questions below and click **Submit**.")

        responses = []

        for idx, row in df.iterrows():
            qid = row.get("QuestionID", f"Q{idx+1}")
            qtext = str(row.get("Question", "")).strip()
            qtype = str(row.get("Type", "")).strip().lower()

            # ---- Instructional text only ----
            if qtype == "info":
                st.markdown(f"### 📝 {qtext}")
                st.markdown("---")
                continue

            st.markdown(f"**Q{idx+1}. {qtext}**")

            # ---- Likert scale ----
            if qtype == "likert":
                scale_min = int(row.get("ScaleMin", 1))
                scale_max = int(row.get("ScaleMax", 5))
                response = st.slider(
                    "Your Response:",
                    min_value=scale_min,
                    max_value=scale_max,
                    value=(scale_min + scale_max) // 2,
                    key=f"q{idx}_{section}"
                )

            # ---- Multiple Choice ----
            elif qtype == "mcq":
                options = [
                    str(row.get(f"Option{i}", "")).strip()
                    for i in range(1, 5)
                    if pd.notna(row.get(f"Option{i}")) and str(row.get(f"Option{i}")).strip() != ""
                ]
                if options:
                    response = st.radio("Your Answer:", options, key=f"q{idx}_{section}")
                else:
                    st.warning(f"No options available for {qid}")
                    response = ""

            # ---- Short / Descriptive ----
            elif qtype == "short":
                response = st.text_area("Your Answer:", key=f"q{idx}_{section}")

            # ---- Unknown / Empty ----
            else:
                st.info(f"⚠️ Unknown question type '{qtype}' for {qid}.")
                response = ""

            responses.append({
                "QuestionID": qid,
                "Question": qtext,
                "Response": response,
                "Type": qtype,
            })
            st.markdown("---")

        # ---------------- SUBMIT ----------------
        if st.button("✅ Submit"):
            if not db:
                st.error("❌ Database connection failed. Cannot save responses.")
            else:
                with st.spinner("Saving your responses..."):
                    data = {
                        "Name": name,
                        "Roll": roll,
                        "Section": section,
                        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "Responses": responses,
                    }
                    try:
                        db.collection("student_responses").document(
                            f"{roll}_{section.replace(' ', '_')}"
                        ).set(data)
                        st.success("✅ Your responses have been successfully submitted!")
                    except Exception as e:
                        st.error(f"❌ Error saving to database: {e}")

else:
    st.info("👆 Please enter your Name and Roll Number to start.")

# ---------------- BACK TO TOP BUTTON ----------------
st.markdown("""
<style>
#back-to-top {
    position: fixed;
    bottom: 40px;
    right: 40px;
    background-color: #007bff;
    color: white;
    border: none;
    padding: 12px 18px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    z-index: 1000;
}
</style>
<button id="back-to-top" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
    ⬆️ Back to Top
</button>
""", unsafe_allow_html=True)
