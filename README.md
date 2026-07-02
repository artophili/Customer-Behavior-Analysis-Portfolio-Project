# Customer Behavior & Retention Risk Analysis

An end-to-end data analyst portfolio project covering business problem framing, data cleaning/feature engineering, SQL analysis, and Tableau dashboarding — modeled on real-world analyst workflow.

## Business Problem

Leadership doesn't know which customer segments are most likely to churn, or whether discount/promo spend is actually building loyalty. This project segments customers, tests promo effectiveness against repeat-purchase behavior, and flags a high-value "at-risk" segment for retention marketing.

Full write-up: [`01_business_understanding/business_problem_statement.md`](01_business_understanding/business_problem_statement.md)

## Project Structure

```
customer-behavior-analysis/
├── 01_business_understanding/
│   └── business_problem_statement.md      # Problem, objectives, KPIs, scope
├── 02_data/
│   ├── raw/                                # Original CSV (not committed if large/sensitive)
│   ├── processed/                          # Cleaned CSV + EDA outputs
│   └── data_dictionary.md                  # Schema and derived-field definitions
├── 03_data_preparation/
│   └── data_cleaning_eda.py                # Cleaning, feature engineering, EDA
├── 04_sql_analysis/
│   └── analysis_queries.sql                # Schema DDL + 8 analysis queries
├── 05_tableau/
│   ├── tableau_dashboard_guide.md          # Dashboard/chart spec
│   └── customer_behavior_dashboard.twbx    # (add your saved Tableau workbook here)
├── 06_reporting/
│   └── executive_summary_and_presentation_outline.md
└── README.md
```

## Tech Stack

- **Python** (pandas, matplotlib) — data cleaning & feature engineering
- **SQL** (PostgreSQL-compatible) — structured analysis
- **Tableau** — dashboarding & visual storytelling
- **Markdown** — documentation

## How to Reproduce

```bash
# 1. Clone repo
git clone https://github.com/<your-username>/customer-behavior-analysis.git
cd customer-behavior-analysis

# 2. Add your raw CSV
cp /path/to/customer_shopping_data.csv 02_data/raw/

# 3. Install dependencies
pip install pandas numpy matplotlib

# 4. Run the cleaning/feature engineering pipeline
cd 03_data_preparation
python data_cleaning_eda.py --input ../02_data/raw/customer_shopping_data.csv \
                             --output ../02_data/processed/cleaned_customer_data.csv

# 5. Load cleaned CSV into your SQL database and run 04_sql_analysis/analysis_queries.sql

# 6. Open Tableau, connect to the cleaned CSV or SQL table, and build dashboards
#    per 05_tableau/tableau_dashboard_guide.md
```

## Key Findings

> _Populate after running the analysis on your data — see `06_reporting/` for the summary template._

1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

## Dashboard

[Link to published Tableau Public dashboard] · ![dashboard preview](05_tableau/dashboard_preview.png)

## Author

[Your Name] — [LinkedIn] · [Portfolio site]
