import pandas as pd

#Laod raw data
df = pd.read_csv("data/raw/jobs.csv")

print("Original rows:", len(df))

#Remove duplicate jobs
df = df.drop_duplicates(subset="job_id")

#Convert posted date
df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")

#Clean text columns
text_columns = ["job_title", "company", "location"]

for column in text_columns:
    df[column] = df[column].fillna("Unknown").str.strip()

#Convert salary columns to numeric
df["salary_min"] = pd.to_numeric(df["salary_min"], errors="coerce")
df["salary_max"] = pd.to_numeric(df["salary_max"], errors="coerce")

#Create average salary
df["salary_avg"] = (df["salary_max"] + df["salary_min"]) / 2

#Remove rows without job ID 
df = df.dropna(subset= ["job_id"])

#Save cleaned data
df.to_csv("data/jobs_cleaned.csv", index=False)

print("Cleaned rows:", len(df))
print("\nMissing values:")
print(df.isnull().sum())

print("\nCleaning completed.")