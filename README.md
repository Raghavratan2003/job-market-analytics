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
