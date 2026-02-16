import pandas as pd
import re
import os


class DataCleaner:

    def __init__(self, output_path="data/jobs_cleaned.csv"):

        self.output_path = output_path
        os.makedirs("data", exist_ok=True)

    # -------------------------
    # Clean text
    # -------------------------

    def clean_text(self, text):

        if pd.isna(text):
            return ""

        text = str(text).lower().strip()

        text = re.sub(r"[^a-z0-9+#\s]", "", text)

        text = re.sub(r"\s+", " ", text)

        return text

    # -------------------------
    # Clean text columns
    # -------------------------

    def clean_text_columns(self, df, columns):

        for col in columns:
            if col in df.columns:
                df[col] = df[col].apply(self.clean_text)

        return df

    # -------------------------
    # Extract city
    # -------------------------

    def extract_city(self, location):

        if pd.isna(location):
            return "unknown"

        return location.split(",")[0].strip().lower()

    # -------------------------
    # Extract experience range
    # -------------------------

    def extract_experience(self, exp):

        if pd.isna(exp):
            return pd.Series([0, 0, 0])

        exp = str(exp)

        numbers = re.findall(r"\d+", exp)

        if len(numbers) == 0:
            return pd.Series([0, 0, 0])

        if len(numbers) == 1:
            val = int(numbers[0])
            return pd.Series([val, val, val])

        min_exp = int(numbers[0])
        max_exp = int(numbers[1])
        avg_exp = (min_exp + max_exp) / 2

        return pd.Series([min_exp, max_exp, avg_exp])

    # -------------------------
    # Clean salary
    # -------------------------

    def clean_salary(self, df):

        if "salary" not in df.columns:
            return df

        df["salary"] = (
            df["salary"]
            .astype(str)
            .str.replace(",", "")
            .str.extract(r"(\d+\.?\d*)")
        )

        df["salary"] = pd.to_numeric(df["salary"], errors="coerce")

        return df

    # -------------------------
    # Remove duplicates
    # -------------------------

    def remove_duplicates(self, df):

        before = len(df)

        df = df.drop_duplicates(
            subset=["job_title", "company"],
            keep="first"
        )

        after = len(df)

        print(f"[Cleaner] Removed {before - after} duplicates")

        return df

    # -------------------------
    # Save cleaned data
    # -------------------------

    def save_cleaned_data(self, df):

        df.to_csv(self.output_path, index=False)

        print(f"[Cleaner] Cleaned data saved to {self.output_path}")

    # -------------------------
    # Full pipeline
    # -------------------------

    def clean_all(self, df):

        print("\n[Cleaner] Cleaning started...")

        df = self.clean_text_columns(
            df,
            ["job_title", "company", "location", "job_description"]
        )

        # city extraction
        df["city"] = df["location"].apply(self.extract_city)

        # experience extraction
        df[["experience_min", "experience_max", "experience_years"]] = (
            df["experience_required"]
            .apply(self.extract_experience)
        )

        # salary cleaning
        df = self.clean_salary(df)

        # remove duplicates
        df = self.remove_duplicates(df)

        # save
        self.save_cleaned_data(df)

        print("[Cleaner] Cleaning completed")

        return df
