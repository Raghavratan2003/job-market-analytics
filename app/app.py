import os

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="Job Market Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       PAGE
       ====================================================== */

    .stApp {
        background-color: #F8FAFC;
        color: #000000;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ======================================================
       HEADINGS
       ====================================================== */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: #000000 !important;
    }


    /* ======================================================
       NORMAL TEXT
       ====================================================== */

    p {
        color: #000000 !important;
    }

    label {
        color: #000000 !important;
    }


    /* ======================================================
       CAPTIONS
       ====================================================== */

    [data-testid="stCaptionContainer"] {
        color: #333333 !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #333333 !important;
    }


    /* ======================================================
       KPI CARDS
       ====================================================== */

    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
    }

    [data-testid="stMetricLabel"] {
        color: #333333 !important;
    }

    [data-testid="stMetricLabel"] * {
        color: #333333 !important;
    }

    [data-testid="stMetricValue"] {
        color: #000000 !important;
    }

    [data-testid="stMetricValue"] * {
        color: #000000 !important;
    }


    /* ======================================================
       TEXT INPUTS
       ====================================================== */

    div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
    }

    div[data-baseweb="input"] input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #666666 !important;
        -webkit-text-fill-color: #666666 !important;
    }


    /* ======================================================
       SELECT BOXES
       ====================================================== */

    div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
    }

    div[data-baseweb="select"] span {
        color: #000000 !important;
    }

    div[data-baseweb="select"] input {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }


    /* ======================================================
       SELECTBOX DROPDOWN
       ====================================================== */

    ul[role="listbox"] {
        background-color: #FFFFFF !important;
    }

    ul[role="listbox"] li {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }

    ul[role="listbox"] li:hover {
        background-color: #F1F5F9 !important;
        color: #000000 !important;
    }


    /* ======================================================
       NUMBER INPUT
       ====================================================== */

    [data-testid="stNumberInput"] {
        background-color: #FFFFFF !important;
    }

    [data-testid="stNumberInput"] input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    div[data-testid="stHorizontalBlock"] button {
        color: #FFFFFF !important;
    }

    div[data-testid="stHorizontalBlock"] button p {
        color: #FFFFFF !important;
    }

    div[data-testid="stHorizontalBlock"] button span {
        color: #FFFFFF !important;
    }


    /* ======================================================
       DATAFRAME
       ====================================================== */

    [data-testid="stDataFrame"] {
        background-color: #FFFFFF !important;
    }


    /* ======================================================
       DIVIDERS
       ====================================================== */

    hr {
        border-color: #E2E8F0 !important;
    }


    /* ======================================================
       LINK BUTTONS
       ====================================================== */

    a {
        color: #2563EB;
    }


    /* ======================================================
       HIDE STREAMLIT FOOTER
       ====================================================== */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATABASE CONNECTION
# ============================================================


@st.cache_resource
def get_connection():
    """
    Create a PostgreSQL connection using credentials
    stored in the .env file.
    """

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


# ============================================================
# GENERIC QUERY FUNCTION
# ============================================================


@st.cache_data(ttl=300)
def run_query(query):
    """
    Execute a SQL query and return a DataFrame.
    """

    conn = get_connection()

    return pd.read_sql_query(
        query,
        conn,
    )


# ============================================================
# LOAD JOBS
# ============================================================


@st.cache_data(ttl=300)
def load_jobs():

    query = """
        SELECT
            job_id,
            job_title,
            company,
            location,
            salary_min,
            salary_max,
            salary_avg,
            posted_date,
            job_url
        FROM jobs
        ORDER BY posted_date DESC NULLS LAST;
    """

    return run_query(query)


# ============================================================
# LOAD SKILLS
# ============================================================


@st.cache_data(ttl=300)
def load_skills():

    query = """
        SELECT
            skill,
            job_count
        FROM skill_demand
        ORDER BY job_count DESC;
    """

    return run_query(query)


# ============================================================
# LOAD LOCATIONS
# ============================================================


@st.cache_data(ttl=300)
def load_locations():

    query = """
        SELECT
            location,
            job_count
        FROM location_demand
        ORDER BY job_count DESC
        LIMIT 10;
    """

    return run_query(query)


# ============================================================
# LOAD COMPANIES
# ============================================================


@st.cache_data(ttl=300)
def load_companies():

    query = """
        SELECT
            company,
            job_count
        FROM company_demand
        ORDER BY job_count DESC
        LIMIT 10;
    """

    return run_query(query)


# ============================================================
# LOAD HIRING TREND
# ============================================================


@st.cache_data(ttl=300)
def load_trend():

    query = """
        SELECT
            posting_date,
            job_count
        FROM hiring_trend
        ORDER BY posting_date;
    """

    return run_query(query)


# ============================================================
# LOAD JOB-SKILLS
# ============================================================


@st.cache_data(ttl=300)
def load_job_skills():

    query = """
        SELECT
            job_id,
            skill
        FROM job_skills;
    """

    return run_query(query)


# ============================================================
# LOAD DATA
# ============================================================

jobs = load_jobs()
skills = load_skills()
locations = load_locations()
companies = load_companies()
trend = load_trend()
job_skills = load_job_skills()


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Overview"


# ============================================================
# PAGE SWITCH FUNCTION
# ============================================================


def set_page(page_name):
    st.session_state.page = page_name


# ============================================================
# HEADER
# ============================================================

st.title("Job Market Analytics")

st.write(
    "Explore collected Data Analyst job listings, "
    "skills and market patterns."
)

st.write("")


# ============================================================
# NAVIGATION
# ============================================================

nav1, nav2, nav3, nav4 = st.columns(4)


with nav1:

    if st.button(
        "Overview",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page == "Overview"
            else "secondary"
        ),
    ):
        set_page("Overview")


with nav2:

    if st.button(
        "Job Explorer",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page == "Job Explorer"
            else "secondary"
        ),
    ):
        set_page("Job Explorer")


with nav3:

    if st.button(
        "Skills",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page == "Skills"
            else "secondary"
        ),
    ):
        set_page("Skills")


with nav4:

    if st.button(
        "Companies",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page == "Companies"
            else "secondary"
        ),
    ):
        set_page("Companies")


st.divider()


# ============================================================
# OVERVIEW PAGE
# ============================================================


if st.session_state.page == "Overview":

    st.header("Overview")

    st.caption(
        "A snapshot of the collected Data Analyst job listings."
    )

    # --------------------------------------------------------
    # KPI CALCULATIONS
    # --------------------------------------------------------

    total_jobs = len(jobs)

    total_companies = (
        jobs["company"]
        .replace("Unknown", pd.NA)
        .dropna()
        .nunique()
    )

    average_salary = (
        jobs["salary_avg"]
        .dropna()
        .mean()
    )

    total_skill_matches = len(job_skills)

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Collected Jobs",
            f"{total_jobs:,}",
        )

    with col2:

        st.metric(
            "Companies",
            f"{total_companies:,}",
        )

    with col3:

        if pd.notna(average_salary):

            salary_display = (
                f"₹{average_salary:,.0f}"
            )

        else:

            salary_display = "—"

        st.metric(
            "Average Listed Salary",
            salary_display,
        )

    with col4:

        st.metric(
            "Job-Skill Matches",
            f"{total_skill_matches:,}",
        )

    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Skills appearing most often"
    )

    st.caption(
        "Number of collected listings mentioning each tracked skill."
    )

    if not skills.empty:

        skill_chart = (
            skills
            .head(10)
            .set_index("skill")["job_count"]
        )

        st.bar_chart(
            skill_chart,
            horizontal=True,
        )

    # --------------------------------------------------------
    # LOCATION + COMPANY
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Where are the jobs?"
        )

        st.caption(
            "Locations with the highest number of collected listings."
        )

        if not locations.empty:

            location_chart = (
                locations
                .set_index("location")["job_count"]
            )

            st.bar_chart(
                location_chart,
                horizontal=True,
            )

    with col2:

        st.subheader(
            "Companies with the most listings"
        )

        st.caption(
            "Companies with the highest number of collected listings."
        )

        if not companies.empty:

            company_chart = (
                companies
                .set_index("company")["job_count"]
            )

            st.bar_chart(
                company_chart,
                horizontal=True,
            )

    # --------------------------------------------------------
    # TREND
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Collected job posting trend"
    )

    st.caption(
        "Quarterly volume of listings available in the dataset."
    )

    if not trend.empty:

        trend_chart = (
            trend
            .set_index("posting_date")["job_count"]
        )

        st.line_chart(
            trend_chart
        )

    # --------------------------------------------------------
    # DATA SOURCE
    # --------------------------------------------------------

    st.divider()

    st.caption(
        "Data source: Adzuna Jobs API. "
        "The dataset represents collected API listings "
        "and is not a complete census of Data Analyst "
        "vacancies in India."
    )


# ============================================================
# JOB EXPLORER PAGE
# ============================================================


elif st.session_state.page == "Job Explorer":

    st.header("Explore Jobs")

    st.caption(
        "Search and filter the collected job listings."
    )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    search = st.text_input(
        "Search",
        placeholder="Search job title, company or skill...",
    )

    # --------------------------------------------------------
    # FILTER OPTIONS
    # --------------------------------------------------------

    location_values = sorted(
        jobs["location"]
        .dropna()
        .unique()
        .tolist()
    )

    company_values = sorted(
        jobs["company"]
        .dropna()
        .unique()
        .tolist()
    )

    location_options = (
        ["All locations"]
        + location_values
    )

    company_options = (
        ["All companies"]
        + company_values
    )

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        selected_location = st.selectbox(
            "Location",
            location_options,
        )

    with col2:

        selected_company = st.selectbox(
            "Company",
            company_options,
        )

    with col3:

        min_salary = st.number_input(
            "Minimum salary (₹)",
            min_value=0,
            max_value=10_000_000,
            value=0,
            step=50_000,
        )

    # --------------------------------------------------------
    # FILTER JOBS
    # --------------------------------------------------------

    filtered = jobs.copy()

    # Search
    if search:

        search_text = search.strip()

        title_match = (
            filtered["job_title"]
            .fillna("")
            .str.contains(
                search_text,
                case=False,
                na=False,
            )
        )

        company_match = (
            filtered["company"]
            .fillna("")
            .str.contains(
                search_text,
                case=False,
                na=False,
            )
        )

        filtered = filtered[
            title_match
            | company_match
        ]

        # Skill search
        matching_skills = skills[
            skills["skill"]
            .fillna("")
            .str.contains(
                search_text,
                case=False,
                na=False,
            )
        ]["skill"].tolist()

        if matching_skills:

            skill_job_ids = job_skills[
                job_skills["skill"].isin(
                    matching_skills
                )
            ]["job_id"].unique()

            skill_matches = jobs[
                jobs["job_id"].isin(
                    skill_job_ids
                )
            ]

            filtered = pd.concat(
                [
                    filtered,
                    skill_matches,
                ],
                ignore_index=True,
            ).drop_duplicates(
                subset=["job_id"]
            )

    # Location
    if selected_location != "All locations":

        filtered = filtered[
            filtered["location"]
            == selected_location
        ]

    # Company
    if selected_company != "All companies":

        filtered = filtered[
            filtered["company"]
            == selected_company
        ]

    # Salary
    if min_salary > 0:

        filtered = filtered[
            filtered["salary_avg"]
            .fillna(0)
            >= min_salary
        ]

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    st.write(
        f"**{len(filtered):,} listings found**"
    )

    if filtered.empty:

        st.info(
            "No jobs matched your filters."
        )

    else:

        for _, row in filtered.head(50).iterrows():

            # -----------------------------------------------
            # JOB TITLE
            # -----------------------------------------------

            title = row["job_title"]

            if pd.isna(title):
                title = "Untitled position"

            # -----------------------------------------------
            # COMPANY
            # -----------------------------------------------

            company = row["company"]

            if pd.isna(company):
                company = "Unknown company"

            # -----------------------------------------------
            # LOCATION
            # -----------------------------------------------

            location = row["location"]

            if pd.isna(location):
                location = "Location unavailable"

            # -----------------------------------------------
            # SALARY
            # -----------------------------------------------

            salary_min = row["salary_min"]
            salary_max = row["salary_max"]
            salary_avg = row["salary_avg"]

            if (
                pd.notna(salary_min)
                and pd.notna(salary_max)
            ):

                salary_text = (
                    f"₹{salary_min:,.0f}"
                    f" – "
                    f"₹{salary_max:,.0f}"
                )

            elif pd.notna(salary_avg):

                salary_text = (
                    f"₹{salary_avg:,.0f}"
                )

            else:

                salary_text = (
                    "Salary not listed"
                )

            # -----------------------------------------------
            # POSTED DATE
            # -----------------------------------------------

            if pd.notna(row["posted_date"]):

                posted_text = (
                    pd.to_datetime(
                        row["posted_date"]
                    ).strftime(
                        "%d %b %Y"
                    )
                )

            else:

                posted_text = (
                    "Date unavailable"
                )

            # -----------------------------------------------
            # JOB CONTAINER
            # -----------------------------------------------

            with st.container(
                border=True
            ):

                st.subheader(
                    title
                )

                st.write(
                    company
                )

                st.caption(
                    f"{location}  ·  "
                    f"{salary_text}  ·  "
                    f"Posted {posted_text}"
                )

                if pd.notna(
                    row["job_url"]
                ):

                    st.link_button(
                        "View original listing",
                        row["job_url"],
                    )


# ============================================================
# SKILLS PAGE
# ============================================================


elif st.session_state.page == "Skills":

    st.header(
        "Skills in demand"
    )

    st.caption(
        "How frequently tracked technical skills appear "
        "in collected Data Analyst listings."
    )

    # --------------------------------------------------------
    # SKILL TABLE
    # --------------------------------------------------------

    skill_table = skills.rename(
        columns={
            "skill": "Skill",
            "job_count": "Job Listings",
        }
    )

    st.dataframe(
        skill_table,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # SKILL INSPECTION
    # --------------------------------------------------------

    if not skills.empty:

        selected_skill = st.selectbox(
            "Inspect a skill",
            skills["skill"].tolist(),
        )

        selected_skill_jobs = job_skills[
            job_skills["skill"]
            == selected_skill
        ]

        selected_job_ids = (
            selected_skill_jobs[
                "job_id"
            ].unique()
        )

        skill_jobs = jobs[
            jobs["job_id"].isin(
                selected_job_ids
            )
        ].copy()

        st.write(
            f"**{len(skill_jobs):,} collected listings "
            f"mention {selected_skill}.**"
        )

        if not skill_jobs.empty:

            skill_display = skill_jobs[
                [
                    "job_title",
                    "company",
                    "location",
                    "salary_avg",
                    "posted_date",
                    "job_url",
                ]
            ].copy()

            skill_display = (
                skill_display.rename(
                    columns={
                        "job_title": "Job Title",
                        "company": "Company",
                        "location": "Location",
                        "salary_avg": "Average Salary",
                        "posted_date": "Posted Date",
                        "job_url": "Job URL",
                    }
                )
            )

            st.dataframe(
                skill_display,
                use_container_width=True,
                hide_index=True,
            )


# ============================================================
# COMPANIES PAGE
# ============================================================


elif st.session_state.page == "Companies":

    st.header(
        "Companies"
    )

    st.caption(
        "Companies with the highest number of collected listings."
    )

    # --------------------------------------------------------
    # COMPANY TABLE
    # --------------------------------------------------------

    company_table = companies.rename(
        columns={
            "company": "Company",
            "job_count": "Job Listings",
        }
    )

    st.dataframe(
        company_table,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # COMPANY INSPECTION
    # --------------------------------------------------------

    if not companies.empty:

        selected_company = st.selectbox(
            "Inspect a company",
            companies["company"].tolist(),
        )

        company_jobs = jobs[
            jobs["company"]
            == selected_company
        ].copy()

        st.write(
            f"**{len(company_jobs):,} collected listings "
            f"from {selected_company}.**"
        )

        if not company_jobs.empty:

            company_display = company_jobs[
                [
                    "job_title",
                    "location",
                    "salary_avg",
                    "posted_date",
                    "job_url",
                ]
            ].copy()

            company_display = (
                company_display.rename(
                    columns={
                        "job_title": "Job Title",
                        "location": "Location",
                        "salary_avg": "Average Salary",
                        "posted_date": "Posted Date",
                        "job_url": "Job URL",
                    }
                )
            )

            st.dataframe(
                company_display,
                use_container_width=True,
                hide_index=True,
            )