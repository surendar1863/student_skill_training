import streamlit as st
import gspread
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Faculty Dashboard", layout="wide")
st.title("📊 Student Edge – Faculty Dashboard")

# Connect Google Sheets
@st.cache_data(ttl=300)
def get_sheet_data():
    try:
        gc = gspread.service_account_from_dict(st.secrets["google_service_account"])
        sh = gc.open("Student_Responses").sheet1
        data = sh.get_all_records()
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"❌ Failed to fetch data from Google Sheets: {e}")
        return pd.DataFrame()

df = get_sheet_data()

if df.empty:
    st.warning("No data available yet.")
    st.stop()

# Data Overview
st.subheader("📈 Summary Overview")
st.write(f"Total responses: **{len(df)}**")
st.dataframe(df, use_container_width=True)

# Filter Section
section_filter = st.selectbox("Filter by Section", ["All"] + sorted(df["Section"].unique()))
if section_filter != "All":
    df = df[df["Section"] == section_filter]

# Average rating display
avg_score = df["Q2"].mean() if not df.empty else 0
st.metric("Average Adaptability Score", f"{avg_score:.2f}")

# Download Option
def convert_df(df):
    return df.to_excel(BytesIO(), index=False)

excel_file = BytesIO()
df.to_excel(excel_file, index=False)
excel_file.seek(0)

st.download_button(
    label="📥 Download Data as Excel",
    data=excel_file,
    file_name="Student_Responses.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.success("✅ Dashboard loaded successfully.")
