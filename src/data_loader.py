import pandas as pd
import os


class DataLoader:

    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):

        print("\n[DataLoader] Loading dataset...")

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Dataset not found at: {self.file_path}")

        df = pd.read_csv(self.file_path)

        # standardize column names
        df.columns = (
           df.columns
           .str.lower()
           .str.strip()
           .str.replace(" ", "_")
        )

        # fix column naming differences
        column_mapping = {

            "job_location": "location",
            "salary_range": "salary",
            "skills_required": "job_description",
            "company_name": "company"
        }

        df = df.rename(columns=column_mapping)

        print(f"[DataLoader] Rows loaded: {len(df)}")

        return df
    
    def basic_info(self, df):

        print("\n[DataLoader] Dataset Info:")
        print(df.info())

        print("\n[DataLoader] Sample Data:")
        print(df.head())
