from src.data_loader import DataLoader
from src.cleaner import DataCleaner
from src.extractor import SkillExtractor
from src.analyzer import Analyzer
from src.visualizer import Visualizer
from src.insights_generator import InsightsGenerator
from src.database import DatabaseManager


def main():

    print("\nAI Job Market Analyzer Started\n")

    loader = DataLoader("data/jobs_raw.csv")

    df = loader.load_data()

    cleaner = DataCleaner()

    df = cleaner.clean_all(df)

    db = DatabaseManager()

    

    df = db.load_jobs()

    extractor = SkillExtractor()

    df = extractor.extract_skills(df)

    db.save_jobs(df)

    analyzer = Analyzer()

    skills_df = analyzer.get_top_skills(df)

    city_df = analyzer.get_city_job_count(df)

    exp_df = analyzer.get_experience_distribution(df)

    salary_stats = analyzer.get_salary_stats(df)

    salary_exp_df = analyzer.get_salary_by_experience(df)

    print(skills_df.columns)
    print(skills_df.head())

    print(city_df.columns)
    print(city_df.head())



    visualizer = Visualizer()

    visualizer.plot_top_skills(skills_df)
    visualizer.plot_city_demand(city_df)
    visualizer.plot_experience_vs_salary(salary_exp_df)
    visualizer.plot_wordcloud(skills_df)

    insights = InsightsGenerator()

    insights.generate(
        skills_df,
        city_df,
        exp_df,
        salary_stats,
        salary_exp_df
    )

    print("\nPROJECT COMPLETED SUCCESSFULLY\n")


if __name__ == "__main__":
    main()
