import subprocess
import sys

steps = [
    ("Fetching latest jobs", "main.py"),
    ("Cleaning job data", "clean_data.py"),
    ("Extracting skills", "extract_skills.py"),
    ("Creating skill table", "create_skill_table.py"),
    ("Loading job into PostgreSQL", "load_data.py"),
    ("Loading skills into PostgreSQL", "load_skills.py"),
]

for description, script in steps:
    print("\n" + "=" * 50)
    print(description)
    print("=" * 50)

    result = subprocess.run(
        [sys.executable, f"src/job_market/{script}"]
    )

    if result.returncode != 0:
        print(f"\nPipeline stopped: {script} failed.")
        sys.exit(1)

print("\n" + "=" * 50)
print("PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 50)