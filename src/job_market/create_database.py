import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")

)

cursor = connection.cursor()

create_table_query="""
CREATE TABLE IF NOT EXISTS JOBS (
    job_id BIGINT PRIMARY KEY,
    job_title TEXT,
    company TEXT,
    location TEXT,
    salary_min NUMERIC,
    salary_max NUMERIC,
    salary_avg NUMERIC,
    posted_date TIMESTAMP,
    job_url TEXT,
    description TEXT 
);
"""

cursor.execute(create_table_query)

connection.commit()

cursor.close()
connection.close()

print("Job table created successfully!")