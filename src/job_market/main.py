import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

all_jobs = []

for page in range(1, 11):

    print(f"Fetching page {page}...")

    url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 50,
        "what": "data analyst",
        "where": "India",
    }

    response = requests.get(url, params=params)

    print("Status:", response.status_code)

    if response.status_code != 200:
        print("Request failed!")
        print(response.text)
        continue

    data = response.json()

    jobs = data.get("results", [])

    print("Jobs received:", len(jobs))

    for job in jobs:

        all_jobs.append({
            "job_id": job.get("id"),
            "job_title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "posted_date": job.get("created"),
            "job_url": job.get("redirect_url"),
            "description": job.get("description"),
        })


# Convert to DataFrame
df = pd.DataFrame(all_jobs)

# Remove duplicate jobs
df = df.drop_duplicates(subset="job_id")

# Create folder if needed
os.makedirs("data/raw", exist_ok=True)

# Save data
df.to_csv("data/raw/jobs.csv", index=False)

print("\n-----------------------------")
print("Total unique jobs:", len(df))
print("-----------------------------")
print("Data saved to data/raw/jobs.csv")