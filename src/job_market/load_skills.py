import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv("data/job_skills.csv")

connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = connection.cursor()

query = """
INSERT INTO job_skills (job_id, skill)
VALUES (%s, %s)
ON CONFLICT (job_id, skill) DO NOTHING;
"""
cursor.execute("TRUNCATE TABLE job_skills;")

for _, row in df.iterrows():

    cursor.execute(
        query,
        (
            row["job_id"],
            row["skill"]
        )
    )

connection.commit()

cursor.close()
connection.close()

print(f"Successfully loaded {len(df)} skill records.")