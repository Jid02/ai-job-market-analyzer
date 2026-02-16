import pandas as pd


class Analyzer:

    def get_top_skills(self, df, top_n=10):

        print("[Analyzer] Calculating top skills...")

        # Drop missing values
        skills_series = df["extracted_skills"].dropna()

        # Collect all skills into one list
        all_skills = []

        for skills in skills_series:
            all_skills.extend([skill.strip() for skill in skills.split(",")])

        # Create dataframe
        skills_df = pd.DataFrame(all_skills, columns=["skill"])

        # Count frequency
        skills_count = (
            skills_df["skill"]
            .value_counts()
            .reset_index()
        )

        # Rename columns PROPERLY
        skills_count.columns = ["skill", "job_count"]

        return skills_count.head(top_n)


    def get_city_job_count(self, df, top_n=10):


        print("[Analyzer] Calculating city demand...")

        city_count = (
            df["city"]
            .dropna()
            .value_counts()
            .reset_index()
        )

        city_count.columns = ["city", "job_count"]

        return city_count.head(top_n)


    def get_experience_distribution(self, df):

        return (
            df["experience_years"]
            .value_counts()
            .sort_index()
            .reset_index()
            .rename(columns={
                "index": "experience_years",
                "experience_years": "job_count"
            })
        )

    def get_salary_stats(self, df):

        return {

            "average_salary": df["salary"].mean(),
            "median_salary": df["salary"].median(),
            "min_salary": df["salary"].min(),
            "max_salary": df["salary"].max()

        }

    def get_salary_by_experience(self, df):

        return (
            df.groupby("experience_years")["salary"]
            .mean()
            .reset_index()
            .rename(columns={
                "salary": "average_salary"
            })
        )
