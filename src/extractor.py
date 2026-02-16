import pandas as pd
from src.skillslist import SKILLS



class SkillExtractor:

    def __init__(self):
        self.skills = [skill.lower() for skill in SKILLS]

    def extract_from_text(self, text):

        if pd.isna(text):
            return ""

        text = text.lower()

        found = set()

        for skill in self.skills:
            if skill in text:
                found.add(skill)

        return ", ".join(found)

    def extract_skills(self, df):

        print("\n[Extractor] Extracting skills...")

        df["extracted_skills"] = (
            df["job_description"]
            .apply(self.extract_from_text)
        )

        print("[Extractor] Skills extraction completed")

        return df
