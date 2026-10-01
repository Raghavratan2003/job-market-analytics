--Total jobs
SELECT COUNT(*) AS total_jobs
FROM jobs;


--Jobs by location
SELECT
	LOCATION,
	COUNT(*) AS JOB_COUNT
FROM
	JOBS
GROUP BY
	LOCATION
ORDER BY
	JOB_COUNT DESC;
	
	
-- Top companies hiring
SELECT
	COMPANY,
	COUNT(*) AS JOB_COUNT
FROM
	JOBS
WHERE
	COMPANY IS NOT NULL
GROUP BY
	COMPANY
ORDER BY
	JOB_COUNT DESC LIMIT
	10;


-- Most common job title
SELECT
job_title,
COUNT(*) AS job_count
FROM JOBS
GROUP BY job_title
ORDER BY job_count DESC
LIMIT 10;


-- Salary analysis
SELECT 
ROUND(AVG(salary_avg), 2) AS average_salary,
ROUND(MIN(salary_avg), 2) AS minimum_salary,
ROUND(MAX(salary_avg), 2) AS maximum_salary
FROM JOBS
WHERE salary_avg IS NOT NULL;


-- Jobs with salary information
SELECT
COUNT(*) AS jobs_with_salary
FROM JOBS
WHERE salary_avg IS NOT NULL;


-- Jobs posted by date
SELECT
    DATE(posted_date) AS posting_date,
    COUNT(*) AS job_count
FROM jobs
GROUP BY DATE(posted_date)
ORDER BY posting_date;



-- Salary by job title
SELECT
    job_title,
    COUNT(*) AS job_count,
    ROUND(AVG(salary_avg), 2) AS average_salary
FROM jobs
WHERE salary_avg IS NOT NULL
GROUP BY job_title
HAVING COUNT(*) >= 3
ORDER BY average_salary DESC;