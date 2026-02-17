import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Job Market Analyzer",
    layout="wide"
)

# -----------------------------
# DATABASE CONNECTION
# -----------------------------

@st.cache_data
def load_data():
    conn = sqlite3.connect("jobs.db")
    df = pd.read_sql("SELECT * FROM jobs", conn)
    conn.close()
    return df

df = load_data()

# -----------------------------
# BASIC DATA CLEANING
# -----------------------------

# Ensure extracted_skills exists
if "extracted_skills" not in df.columns:
    df["extracted_skills"] = ""

# Convert salary to numeric safely
if "salary" in df.columns:
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")

if "experience" in df.columns:
    df["experience"] = pd.to_numeric(df["experience"], errors="coerce")

# -----------------------------
# TITLE
# -----------------------------

st.title("AI Job Market Analyzer")

st.caption(
    "Built by Jidnayasa Pawar | Python • Data Analysis • Machine Learning"
)

st.divider()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------

st.sidebar.title("Filters")

# Location Filter
if "city" in df.columns:
    cities = df["city"].dropna().unique()
    selected_city = st.sidebar.multiselect(
        "Select Location",
        cities,
        default=cities
    )
else:
    selected_city = []

# Skills Filter
skills_list = []

for skills in df["extracted_skills"].dropna():
    skills_list.extend(skills.split(","))

skills_list = sorted(set(skills_list))

selected_skills = st.sidebar.multiselect(
    "Select Skills",
    skills_list
)

# Salary Filter
if "salary" in df.columns:
    min_salary = int(df["salary"].min()) if df["salary"].notna().any() else 0
    max_salary = int(df["salary"].max()) if df["salary"].notna().any() else 100000

    salary_range = st.sidebar.slider(
        "Salary Range",
        min_salary,
        max_salary,
        (min_salary, max_salary)
    )
else:
    salary_range = (0, 100000)

# Experience Filter
if "experience" in df.columns:
    min_exp = int(df["experience"].min()) if df["experience"].notna().any() else 0
    max_exp = int(df["experience"].max()) if df["experience"].notna().any() else 10

    exp_range = st.sidebar.slider(
        "Experience Range",
        min_exp,
        max_exp,
        (min_exp, max_exp)
    )
else:
    exp_range = (0, 10)

# -----------------------------
# APPLY FILTERS
# -----------------------------

filtered_df = df.copy()

if selected_city and "city" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["city"].isin(selected_city)]

if selected_skills:
    filtered_df = filtered_df[
        filtered_df["extracted_skills"].apply(
            lambda x: any(skill in str(x) for skill in selected_skills)
        )
    ]

if "salary" in filtered_df.columns:
    filtered_df = filtered_df[
        (filtered_df["salary"] >= salary_range[0]) &
        (filtered_df["salary"] <= salary_range[1])
    ]

if "experience" in filtered_df.columns:
    filtered_df = filtered_df[
        (filtered_df["experience"] >= exp_range[0]) &
        (filtered_df["experience"] <= exp_range[1])
    ]

# -----------------------------
# KPI METRICS
# -----------------------------

st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

total_jobs = len(filtered_df)

# Top Skill
all_skills = []

for skills in filtered_df["extracted_skills"].dropna():
    all_skills.extend(skills.split(","))

top_skill = max(set(all_skills), key=all_skills.count) if all_skills else "N/A"

# Top City
if "city" in filtered_df.columns and not filtered_df.empty:
    top_city = filtered_df["city"].value_counts().idxmax()
else:
    top_city = "N/A"

# Avg Salary
if "salary" in filtered_df.columns:
    avg_salary = int(filtered_df["salary"].mean()) if filtered_df["salary"].notna().any() else 0
else:
    avg_salary = 0

col1.metric("Total Jobs", total_jobs)
col2.metric("Top Skill", top_skill)
col3.metric("Top City", top_city)
col4.metric("Avg Salary", avg_salary)

st.divider()

# -----------------------------
# TOP SKILLS CHART
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Top Skills Demand")

    skill_counts = pd.Series(all_skills).value_counts().head(10)

    fig, ax = plt.subplots()

    sns.barplot(
        x=skill_counts.values,
        y=skill_counts.index,
        ax=ax
    )

    ax.set_xlabel("Job Count")
    ax.set_ylabel("Skill")

    st.pyplot(fig)

# -----------------------------
# TOP CITIES CHART
# -----------------------------

with col2:

    if "city" in filtered_df.columns:

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

# -----------------------------
# SALARY VS EXPERIENCE
# -----------------------------

if "salary" in filtered_df.columns and "experience" in filtered_df.columns:

    st.subheader("Salary vs Experience")

    fig, ax = plt.subplots()

    sns.scatterplot(
        data=filtered_df,
        x="experience",
        y="salary",
        ax=ax
    )

    ax.set_xlabel("Experience (Years)")
    ax.set_ylabel("Salary")

    st.pyplot(fig)

st.divider()

# -----------------------------
# SKILL FREQUENCY TABLE
# -----------------------------

st.subheader("Skill Demand Frequency")

skill_freq = pd.Series(all_skills).value_counts()

st.dataframe(skill_freq)

st.divider()

# -----------------------------
# DOWNLOAD BUTTON
# -----------------------------

st.subheader("Download Filtered Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_jobs.csv",
    mime="text/csv"
)

st.divider()

# -----------------------------
# FOOTER
# -----------------------------

st.markdown(
    """Built by Jidnayasa Pawar  
    AI Job Market Analyzer | Streamlit | Python | SQLite
    """
)



