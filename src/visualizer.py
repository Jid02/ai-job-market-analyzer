import matplotlib.pyplot as plt
import seaborn as sns
import os
from wordcloud import WordCloud

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


class Visualizer:

    def __init__(self, show=False):
        self.show = show
        sns.set_style("whitegrid")

    def plot_top_skills(self, df):

        plt.figure(figsize=(10, 6))

        sns.barplot(data=df, x="job_count", y="skill")

        plt.title("Top Skills")

        path = f"{OUTPUT_DIR}/top_10_skills.png"
        plt.savefig(path)

        if self.show:
            plt.show()

        plt.close()

    def plot_city_demand(self, df):

        plt.figure(figsize=(10, 6))

        sns.barplot(data=df, x="job_count", y="city")

        path = f"{OUTPUT_DIR}/city_job_demand.png"
        plt.savefig(path)

        plt.close()

    def plot_experience_vs_salary(self, df):

        plt.figure(figsize=(10, 6))

        sns.scatterplot(
            data=df,
            x="experience_years",
            y="average_salary"
        )

        path = f"{OUTPUT_DIR}/experience_vs_salary.png"
        plt.savefig(path)

        plt.close()

    def plot_wordcloud(self, skill_df):

        freq = dict(zip(skill_df.skill, skill_df.job_count))

        wc = WordCloud().generate_from_frequencies(freq)

        plt.imshow(wc)
        plt.axis("off")

        path = f"{OUTPUT_DIR}/wordcloud_skills.png"
        plt.savefig(path)

        plt.close()
