-- Skill Demand
CREATE OR REPLACE VIEW skill_demand AS
SELECT
    skill,
    COUNT(*) AS job_count
FROM job_skills
GROUP BY skill
ORDER BY job_count DESC;


--Jobs by location
CREATE OR REPLACE VIEW location_demand AS
SELECT
    location,
    COUNT(*) AS job_count
FROM jobs
GROUP BY location
ORDER BY job_count DESC;


--Jobs by company
CREATE OR REPLACE VIEW company_demand AS
SELECT
    company,
    COUNT(*) AS job_count
FROM jobs
WHERE company IS NOT NULL
GROUP BY company
ORDER BY job_count DESC;


--Hiring trend
CREATE OR REPLACE VIEW hiring_trend AS
SELECT
    DATE(posted_date) AS posting_date,
    COUNT(*) AS job_count
FROM jobs
WHERE posted_date IS NOT NULL
GROUP BY DATE(posted_date)
ORDER BY posting_date;


--Job title analysis
CREATE OR REPLACE VIEW job_title_demand AS
SELECT
    job_title,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_avg), 2) AS average_salary
FROM jobs
GROUP BY job_title
ORDER BY job_count DESC;