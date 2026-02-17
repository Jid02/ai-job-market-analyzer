# ============================================================
# AI JOB MARKET ANALYZER - FAANG LEVEL DASHBOARD
# Author: Jidnayasa Pawar
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Job Market Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# LOAD DATA (Production Safe)
# ============================================================

DATA_PATH = Path("data/jobs_cleaned.csv")


@st.cache_data
def load_data():

    try:
        df = pd.read_csv(DATA_PATH)

        # Standardize column names
        df.columns = df.columns.str.lower().str.strip()

        return df

    except Exception as e:

        st.error("Dataset not found. Please upload jobs_cleaned.csv to data folder.")
        return pd.DataFrame()


df = load_data()

if df.empty:
    st.stop()

# ============================================================
# SAFE COLUMN HANDLING
# ============================================================

def safe_column(df, col, default=""):

    if col not in df.columns:
        df[col] = default

    return df


df = safe_column(df, "city")
df = safe_column(df, "salary")
df = safe_column(df, "experience")
df = safe_column(df, "extracted_skills")

# Convert numeric safely
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
df["experience"] = pd.to_numeric(df["experience"], errors="coerce")

# ============================================================
# HEADER
# ============================================================

st.title("AI Job Market Analyzer Dashboard")

st.markdown(
"""
Interactive dashboard to analyze AI/ML job demand, skills, salary trends, and hiring locations.

Built using:

• Python  
• Pandas  
• Streamlit  
• Data Analysis  
• Data Visualization  
"""
)

st.divider()

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Filters")

filtered_df = df.copy()

# ---------------- CITY FILTER ----------------

cities = sorted(filtered_df["city"].dropna().unique())

selected_cities = st.sidebar.multiselect(
    "Select Location",
    cities,
    default=cities
)

if selected_cities:

    filtered_df = filtered_df[
        filtered_df["city"].isin(selected_cities)
    ]


# ---------------- SKILL FILTER ----------------

all_skills = []

for skills in filtered_df["extracted_skills"].dropna():
    all_skills.extend(str(skills).split(","))

all_skills = sorted(set([s.strip() for s in all_skills if s]))

selected_skills = st.sidebar.multiselect(
    "Select Skills",
    all_skills
)

if selected_skills:

    filtered_df = filtered_df[
        filtered_df["extracted_skills"].apply(
            lambda x: any(skill in str(x) for skill in selected_skills)
        )
    ]


# ---------------- SALARY FILTER ----------------

if filtered_df["salary"].notna().any():

    min_salary = int(filtered_df["salary"].min())
    max_salary = int(filtered_df["salary"].max())

else:

    min_salary = 0
    max_salary = 100000

salary_range = st.sidebar.slider(
    "Salary Range",
    min_salary,
    max_salary,
    (min_salary, max_salary)
)

filtered_df = filtered_df[
    (filtered_df["salary"] >= salary_range[0]) &
    (filtered_df["salary"] <= salary_range[1])
]


# ---------------- EXPERIENCE FILTER ----------------

if filtered_df["experience"].notna().any():

    min_exp = int(filtered_df["experience"].min())
    max_exp = int(filtered_df["experience"].max())

else:

    min_exp = 0
    max_exp = 10

exp_range = st.sidebar.slider(
    "Experience Range",
    min_exp,
    max_exp,
    (min_exp, max_exp)
)

filtered_df = filtered_df[
    (filtered_df["experience"] >= exp_range[0]) &
    (filtered_df["experience"] <= exp_range[1])
]

# ============================================================
# KPI METRICS
# ============================================================

st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_jobs = len(filtered_df)

# Top skill
skills_flat = []

for skills in filtered_df["extracted_skills"].dropna():
    skills_flat.extend(str(skills).split(","))

top_skill = max(set(skills_flat), key=skills_flat.count) if skills_flat else "N/A"

# Top city
top_city = (
    filtered_df["city"].value_counts().idxmax()
    if not filtered_df["city"].empty else "N/A"
)

# Avg salary
avg_salary = int(filtered_df["salary"].mean()) if filtered_df["salary"].notna().any() else 0

col1.metric("Total Jobs", total_jobs)
col2.metric("Top Skill", top_skill)
col3.metric("Top City", top_city)
col4.metric("Average Salary", avg_salary)

st.divider()

# ============================================================
# CHARTS ROW 1
# ============================================================

col1, col2 = st.columns(2)

# -------- TOP SKILLS --------

with col1:

    st.subheader("Top Skills Demand")

    skill_counts = pd.Series(skills_flat).value_counts().head(10)

    fig, ax = plt.subplots()

    sns.barplot(
        x=skill_counts.values,
        y=skill_counts.index,
        ax=ax
    )

    ax.set_xlabel("Job Count")
    ax.set_ylabel("Skill")

    st.pyplot(fig)


# -------- CITY DEMAND --------

with col2:

    st.subheader("Top Hiring Cities")

    city_counts = filtered_df["city"].value_counts().head(10)

    fig, ax = plt.subplots()

    sns.barplot(
        x=city_counts.values,
        y=city_counts.index,
        ax=ax
    )

    ax.set_xlabel("Job Count")
    ax.set_ylabel("City")

    st.pyplot(fig)


st.divider()

# ============================================================
# SALARY VS EXPERIENCE
# ============================================================

st.subheader("Salary vs Experience")

fig, ax = plt.subplots()

sns.scatterplot(
    data=filtered_df,
    x="experience",
    y="salary",
    ax=ax
)

ax.set_xlabel("Experience")
ax.set_ylabel("Salary")

st.pyplot(fig)

st.divider()

# ============================================================
# SKILL FREQUENCY TABLE
# ============================================================

st.subheader("Skill Demand Frequency")

skill_freq = pd.Series(skills_flat).value_counts()

st.dataframe(skill_freq)

# ============================================================
# RAW DATA VIEW
# ============================================================

st.subheader("Filtered Job Listings")

st.dataframe(filtered_df)

# ============================================================
# DOWNLOAD BUTTON
# ============================================================

csv = filtered_df.to_csv(index=False)

st.download_button(
    "Download Filtered Data",
    csv,
    "filtered_jobs.csv",
    "text/csv"
)

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
"""
Built by **Jidnayasa Pawar**

Tech Stack:
Python • Pandas • Streamlit • Data Analysis • Visualization
"""
)
