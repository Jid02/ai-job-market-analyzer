import streamlit as st
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
st.markdown(
    "<p style='text-align: center; color: grey;'>Built by Jidnyasa Pawar | AI Job Market Analyzer 2026</p>",
    unsafe_allow_html=True
)


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

st.subheader("Raw Job Data")

st.dataframe(df)


# --------------------------
# Top Skills Chart
# --------------------------

st.subheader("Top Skills Demand")

st.bar_chart(
    skills_df.set_index("skill")["job_count"]
)


# --------------------------
# City Demand Chart
# --------------------------

st.subheader("City-wise Job Demand")

st.bar_chart(
    city_df.set_index("city")["job_count"]
)


# --------------------------
# Salary vs Experience
# --------------------------

st.subheader("Salary vs Experience")

st.line_chart(
    salary_exp_df.set_index("experience_years")["average_salary"]
)


# --------------------------
# Skill filter
# --------------------------

st.subheader("Filter by Skill")

selected_skill = st.selectbox(
    "Select skill",
    skills_df["skill"].tolist()
)

filtered_df = df[
    df["extracted_skills"].str.contains(selected_skill, na=False)
]

st.dataframe(filtered_df)


db.close()


