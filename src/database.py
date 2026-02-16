import sqlite3
import pandas as pd
import os


class DatabaseManager:

    def __init__(self, db_path="data/jobs.db"):

        os.makedirs("data", exist_ok=True)

        self.conn = sqlite3.connect(db_path)

        print("[Database] Connected to SQLite database")

    def save_jobs(self, df, table_name="jobs"):

        df.to_sql(
            table_name,
            self.conn,
            if_exists="replace",
            index=False
        )

        print(f"[Database] Saved {len(df)} records to '{table_name}' table")

    def load_jobs(self, table_name="jobs"):
        query = f"""SELECT name FROM sqlite_master
        WHERE type='table' AND name='{table_name}'
        """
        table_exists = pd.read_sql(query, self.conn)
        if table_exists.empty:
            raise Exception(
                "Table 'jobs' not found. Run main.py first to create database."
            )

        df = pd.read_sql(f"SELECT * FROM {table_name}", self.conn)

        print(f"[Database] Loaded {len(df)} records")

        return df


    def close(self):

        self.conn.close()

        print("[Database] Connection closed")
