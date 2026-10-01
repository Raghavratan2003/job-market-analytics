# Job Market Analytics

An end-to-end job market analytics pipeline that collects Data Analyst job listings, processes the data, stores it in PostgreSQL, and presents market insights through Power BI.

## Dashboard

The Power BI dashboard provides an overview of:

- Job demand by skill
- Job postings by location
- Top hiring companies
- Common job titles
- Average salary by job title
- Quarterly job posting trends

## Tech Stack

- **Python** — data extraction and processing
- **Adzuna REST API** — job listing source
- **Pandas** — data cleaning and transformation
- **PostgreSQL** — data storage
- **SQL** — analytical views and aggregations
- **Power BI** — dashboard and visualization
- **uv** — Python environment and dependency management

## Architecture

```text
Adzuna API
    ↓
Python Data Ingestion
    ↓
Pandas Data Cleaning
    ↓
Skill Extraction
    ↓
PostgreSQL
    ↓
SQL Analytical Views
    ↓
Power BI Dashboard
```

## Project Structure

```text
job-market-analytics/
│
├── data/
│   └── .gitkeep
│
├── sql/
│   └── dashboard_views.sql
│
├── src/
│   └── job_market/
│       ├── __init__.py
│       ├── main.py
│       ├── clean_data.py
│       ├── extract_skills.py
│       ├── create_skill_table.py
│       ├── load_data.py
│       ├── load_skills.py
│       └── pipeline.py
│
├── dashboard/
│
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
└── uv.lock
```

## Data Pipeline

The pipeline performs the following steps:

1. Fetches Data Analyst job listings from the Adzuna API.
2. Removes duplicate job listings.
3. Cleans job titles, companies, locations, and salary fields.
4. Extracts selected technical skills from job descriptions.
5. Creates job-skill relationships.
6. Loads job data into PostgreSQL.
7. Loads extracted skills into PostgreSQL.
8. Creates SQL views for dashboard analysis.
9. Refreshes the Power BI dashboard from PostgreSQL.

The complete pipeline can be executed using:

```bash
python src/job_market/pipeline.py
```

## Database

The PostgreSQL database contains two main tables:

### `jobs`

Stores:

- Job ID
- Job title
- Company
- Location
- Minimum salary
- Maximum salary
- Average salary
- Posting date
- Job URL
- Job description

### `job_skills`

Stores:

- Job ID
- Extracted skill

SQL views are used to generate:

- Skill demand
- Location demand
- Company demand
- Job title demand
- Posting trends

## Skill Extraction

The project extracts selected skills from job descriptions using rule-based pattern matching.

Tracked skills include:

```text
Python
SQL
Excel
Power BI
Tableau
Statistics
Machine Learning
AWS
Azure
GCP
Java
R
Spark
Hadoop
Snowflake
Databricks
```

## Dashboard

The Power BI dashboard contains:

- Total Jobs
- Companies
- Average Salary
- Job-Skill Matches
- Most In-Demand Skills
- Top Companies
- Jobs by Location
- Most Common Job Titles
- Salary by Job Title
- Quarterly Job Posting Trend — Collected Listings

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/job-market-analytics.git
cd job-market-analytics
```

### 2. Install dependencies

This project uses `uv`.

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file based on `.env.example`.

```env
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key

DB_HOST=localhost
DB_PORT=5432
DB_NAME=job_market
DB_USER=postgres
DB_PASSWORD=your_password
```

**Never commit `.env` or API credentials to GitHub.**

### 4. Create the PostgreSQL database

Create a PostgreSQL database named:

```text
job_market
```

Then configure the database credentials in `.env`.

### 5. Run the pipeline

```bash
python src/job_market/pipeline.py
```

## Data Source

Job listings are collected using the Adzuna Jobs API.

The dashboard represents the **collected API listings** and should not be interpreted as a complete census of the Indian job market.

## Key Analysis

The dashboard can be used to investigate questions such as:

- Which technical skills appear most frequently in Data Analyst listings?
- Which locations contain the most collected listings?
- Which companies have the most listings?
- Which job titles are most common?
- What salary ranges are associated with different job titles?
- How does the volume of collected listings vary over time?

## Limitations

- The dataset consists of listings returned by the Adzuna API.
- API results do not represent every Data Analyst vacancy in India.
- Skill extraction uses predefined rule-based matching rather than NLP.
- Salary information is missing for some listings.
- Posting volume can vary depending on API availability and collection time.

## Future Improvements

Possible extensions include:

- Automated scheduled data collection
- More comprehensive skill extraction
- Additional job categories
- Cloud database deployment
- Automated Power BI refresh

## Author

**Raghav Ratan Yadav**

Integrated M.Sc. Mathematics  
NIT Rourkela
