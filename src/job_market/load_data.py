import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv("data/jobs_cleaned.csv")

connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = connection.cursor()

insert_query = """
INSERT INTO jobs (
    job_id,
    job_title,
    company,
    location,
    salary_min,
    salary_max,
    salary_avg,
    posted_date,
    job_url,
    description
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

ON CONFLICT (job_id)
DO UPDATE SET
    job_title = EXCLUDED.job_title,
    company = EXCLUDED.company,
    location = EXCLUDED.location,
    salary_min = EXCLUDED.salary_min,
    salary_max = EXCLUDED.salary_max,
    salary_avg = EXCLUDED.salary_avg,
    posted_date = EXCLUDED.posted_date,
    job_url = EXCLUDED.job_url,
    description = EXCLUDED.description;
"""

for _, row in df.iterrows():
    cursor.execute(
        insert_query,
        (
            row["job_id"],
            row["job_title"],
            row["company"],
            row["location"],
            row["salary_min"],
            row["salary_max"],
            row["salary_avg"],
            row["posted_date"],
            row["job_url"],
            row["description"]
        )
    )

connection.commit()

cursor.close()
connection.close()

print(f"Successfully loaded {len(df)} jobs into PostgreSQL.")