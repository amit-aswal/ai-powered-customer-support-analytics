# Interview Explanation

## Short Explanation

I built an AI-powered customer support analytics platform using Python, SQL, DuckDB, Power BI, and NLP.

The project takes raw customer support tickets and converts them into cleaned data, SQL models, KPI reports, Power BI dashboards, sentiment insights, urgency scores, and AI-style executive recommendations.

---

## Detailed Explanation

The project simulates how a real company can analyze customer support tickets to improve support operations.

I started by ingesting a support ticket dataset from Hugging Face and storing it in a bronze layer. Then I profiled the raw data to understand missing values, duplicates, text fields, categorical distributions, and business gaps.

In the next phase, I cleaned the data and created a silver layer. Since the original dataset did not include operational lifecycle fields such as ticket status, created date, resolved date, agent name, resolution time, and SLA status, I simulated these fields using documented logic and clearly marked them as simulated.

After that, I created a SQL analytics layer using DuckDB. I designed a star schema with one fact table and multiple dimension tables such as date, queue, priority, language, agent, category, status, and type. I also created SQL-based KPI reports for ticket volume, SLA compliance, queue performance, agent workload, category analysis, and monthly trends.

Then I created EDA reports and business insights using Python. I used these outputs to prepare Power BI dashboard datasets and built a 6-page Power BI dashboard covering executive overview, queue performance, SLA performance, agent workload, ticket category analysis, and monthly trend analysis.

Finally, I added an NLP layer for sentiment analysis, urgency scoring, keyword extraction, and negative ticket identification. I combined the business KPI outputs and NLP outputs into an AI-style executive summary and business recommendation report.

---

## Business Problem Solved

The project helps support leaders answer:

- Which queues are overloaded?
- Which tickets are breaching SLA?
- Which agents have high workload?
- Which categories create the most support demand?
- Which tickets show negative sentiment?
- Which tickets are high urgency?
- What should the business fix first?

---

## Tools Used

- Python
- Pandas
- DuckDB
- SQL
- Power BI
- DAX
- Matplotlib
- Rule-based NLP scoring
- Git
- GitHub

---

## Why This Project Is Strong

This project is strong because it covers the full analytics lifecycle:

- Raw data ingestion
- Data profiling
- Data cleaning
- Feature engineering
- Data validation
- SQL data modeling
- Business KPI creation
- Dashboard development
- NLP analysis
- Executive reporting
- Business recommendations

It is not only a charting project. It shows end-to-end analytics engineering and business intelligence workflow.
