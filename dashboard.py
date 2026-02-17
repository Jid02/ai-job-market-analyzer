import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd

from src.database import DatabaseManager
from src.analyzer import Analyzer


# --------------------------
# Page config
# --------------------------

st.set_page_config(
    page_title="AI Job Market Analyzer",
    layout="wide"
)

st.title("AI Job Market Analyzer Dashboard")


# --------------------------
# Load data from database
# --------------------------

db = DatabaseManager()

df = db.load_jobs()


analyzer = Analyzer()

skills_df = analyzer.get_top_skills(df)

city_df = analyzer.get_city_job_count(df)

salary_exp_df = analyzer.get_salary_by_experience(df)


# --------------------------
# Show raw data
# --------------------------
#st.subheader("Raw Job Data")
#st.dataframe(df)

st.sidebar.header("Filters")

# City filter
if "city" in df.columns:
    selected_city = st.sidebar.selectbox(
        "Select City",
        ["All"] + sorted(df["city"].dropna().unique().tolist())
    )

    if selected_city != "All":
        df = df[df["city"] == selected_city]


# Skill filter
if "extracted_skills" in df.columns:
    selected_skill = st.sidebar.selectbox(
        "Select Skill",
        ["All"] + sorted(skills_df["skill"].unique().tolist())
    )

    if selected_skill != "All":
        df = df[df["extracted_skills"].str.contains(selected_skill, na=False)]

# --------------------------
# Skill filter
# --------------------------
st.divider()

st.subheader("Filter by Skill")

filtered_df = df[
    df["extracted_skills"].str.contains(selected_skill, na=False)
]

st.dataframe(filtered_df)



st.download_button(
    label="Download Data as CSV",
    data=df.to_csv(index=False),
    file_name="job_data.csv",
    mime="text/csv"
)


# ===== KPI SECTION =====
st.subheader("📊 Key Metrics")

total_jobs = len(df)

top_skill = skills_df.iloc[0]["skill"] if not skills_df.empty else "N/A"
top_city = city_df.iloc[0]["city"] if not city_df.empty else "N/A"

avg_salary = df["salary"].mean() if "salary" in df.columns else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Jobs", total_jobs)
col2.metric("Top Skill", top_skill)
col3.metric("Top City", top_city)
col4.metric("Avg Salary", f"{round(avg_salary, 2)}")


# --------------------------
# Top Skills Chart
# --------------------------
st.divider()

st.subheader("Top Skills Demand")

st.bar_chart(
    skills_df.set_index("skill")["job_count"]
)


# --------------------------
# City Demand Chart
# --------------------------
st.divider()

st.subheader("City-wise Job Demand")

st.bar_chart(
    city_df.set_index("city")["job_count"]
)


# --------------------------
# Salary vs Experience
# --------------------------
st.divider()

st.subheader("Salary vs Experience")

st.line_chart(
    salary_exp_df.set_index("experience_years")["average_salary"]
)
db.close()



st.markdown(
    """
    Built by Jidnyasa Pawar  
    AI Engineer | Python | Machine Learning  

    🔗 **Connect With Me:**  
    GitHub: https://github.com/Jid02  
    LinkedIn: https://linkedin.com/in/jidnyasa-pawar-505639301
    """
)

