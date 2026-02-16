import os


class InsightsGenerator:

    def __init__(self):

        os.makedirs("outputs", exist_ok=True)

    def generate(
        self,
        skills_df,
        city_df,
        exp_df,
        salary_stats,
        salary_exp_df
    ):

        insights = []

        insights.append(
            f"Top skill: {skills_df.iloc[0]['skill']}"
        )

        insights.append(
            f"Top hiring city: {city_df.iloc[0]['city']}"
        )

        insights.append(
            f"Average salary: {salary_stats['average_salary']:.2f}"
        )

        text = "\n".join(insights)

        with open("outputs/insights.txt", "w") as f:
            f.write(text)

        print("[Insights] Saved insights")

        return text
