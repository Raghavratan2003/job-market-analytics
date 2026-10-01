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

query = """
CREATE TABLE IF NOT EXISTS job_skills (
    job_id BIGINT REFERENCES jobs(job_id),
    skill TEXT,
    PRIMARY KEY (job_id, skill)
);
"""

cursor.execute(query)

connection.commit()

cursor.close()
connection.close()

print("job_skills table created successfully!")