import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

st.set_page_config(page_title="Student Edge Assessment", layout="wide")
st.title("🎓 Student Edge Assessment Portal")

# Initialize data file
DATA_FILE = "student_responses.json"

def load_data():
    """Load existing data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def export_to_excel():
    """Export data to Excel format"""
    data = load_data()
    if data:
        df = pd.DataFrame(data)
        return df
    return pd.DataFrame()

# Student Form
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
                     height=120)
    
    submitted = st.form_submit_button("Submit Response ✅")

if submitted:
    if not all([name, roll, q1]):
        st.warning("⚠️ Please fill all required fields")
        st.stop()

    # Create response data
    response_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name.strip(),
        "roll": roll.strip().upper(),
        "section": section,
        "problem_solving_response": q1.strip(),
        "adaptability_rating": q2
    }

    # Load existing data
    all_data = load_data()
    
    # Add new response
    all_data.append(response_data)
    
    # Save to file
    save_data(all_data)
    
    st.success("✅ Response saved successfully!")
    st.balloons()

# Admin Section
st.sidebar.header("📊 Admin Panel")

# Show statistics
data = load_data()
if data:
    st.sidebar.success(f"Total Responses: {len(data)}")
    
    # Section breakdown
    sections = [item['section'] for item in data]
    section_counts = pd.Series(sections).value_counts()
    
    st.sidebar.write("**Responses by Section:**")
    for section, count in section_counts.items():
        st.sidebar.write(f"- {section}: {count}")
else:
    st.sidebar.info("No responses yet")

# Export to Excel
if st.sidebar.button("📥 Export to Excel"):
    df = export_to_excel()
    if not df.empty:
        # Create Excel file
        excel_file = "student_responses.xlsx"
        df.to_excel(excel_file, index=False)
        
        # Provide download link
        with open(excel_file, "rb") as f:
            excel_data = f.read()
        
        st.sidebar.download_button(
            label="⬇️ Download Excel File",
            data=excel_data,
            file_name=f"student_responses_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Show preview
        st.sidebar.write("**Data Preview:**")
        st.sidebar.dataframe(df.tail(5))
    else:
        st.sidebar.warning("No data to export")

# Display all responses (optional)
if st.checkbox("Show All Responses"):
    data = load_data()
    if data:
        st.dataframe(pd.DataFrame(data))
    else:
        st.info("No responses yet")
