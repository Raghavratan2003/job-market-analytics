import pandas as pd
import re

df = pd.read_csv("data/jobs_cleaned.csv")

skills = {
    "Python",
    "SQL",
    "Excel",
    "Power BI",
    "Tableau",
    "Statistics",
    "Machine Learning",
    "AWS",
    "Azure",
    "GCP",
    "Java",
    "R",
    "Spark",
    "Hadoop",
    "Snowflake",
    "Databricks",
}

skill_rows = []

for _, job in df.iterrows():
    description = str(job["description"]).lower()

    for skill in skills:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, description):
            skill_rows.append({
                "job_id": job["job_id"],
                "skill": skill
            })

skill_df = pd.DataFrame(skill_rows)

skill_df = skill_df.drop_duplicates(subset=["job_id", "skill"])

skill_df.to_csv("data/job_skills.csv", index=False)

print("Total job-skill records:", len(skill_df))
print("\nSkill demand:")
print(
    skill_df["skill"]
    .value_counts()
)