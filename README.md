# Money Vision

Money Vision is a personal finance analysis project.

The goal of this project is to clean raw expense data, store it in PostgreSQL, and analyze spending patterns using Python and Power BI.

It follows a simple ETL process:
Excel → Python → PostgreSQL → Analysis → Dashboard

---

## Tools Used

- Python
- pandas
- PostgreSQL
- psycopg2
- SQL
- Matplotlib
- Power BI

---

## Project Structure

money-vision/
- data/ → raw and cleaned files
- scripts/ → Python scripts for cleaning, loading, and analysis
- sql/ → table creation queries
- PowerBI Dashboard/ → dashboard file
- .env → database credentials
- README.md

---

## How to Run

1. Clean the data
python scripts/clean_data.py

2. Load data into PostgreSQL
python scripts/load_to_postgres.py

3. Run analysis
python scripts/analysis_monthly.py

4. Open the Power BI dashboard file

---

## Database Setup

Create a `.env` file in the project folder:

DB_NAME=personal_finance
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

---

## What this project shows

- Data cleaning with pandas
- Loading data into PostgreSQL
- Writing SQL queries for analysis
- Creating basic visualizations
- Building a simple dashboard

---

Author
Sarvesh Marne