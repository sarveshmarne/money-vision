import os
from dotenv import load_dotenv
import psycopg2
import pandas as pd

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()   # reads .env from project root

# -----------------------------
# Load cleaned CSV
# -----------------------------
csv_file = r"D:\Projects\github-projects\moneyv-ision\data\clean_finance_data_for_postgres.csv"

df = pd.read_csv(csv_file)
print(f"Loaded {len(df)} rows from clean CSV")

# -----------------------------
# Connect to PostgreSQL
# -----------------------------
conn = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cursor = conn.cursor()
print("Connected to PostgreSQL")

# -----------------------------
# Truncate table
# -----------------------------
print("Truncating table...")
cursor.execute("TRUNCATE TABLE public.transactions;")
conn.commit()
print("Table truncated.")

# -----------------------------
# Insert query
# -----------------------------
insert_query = """
INSERT INTO transactions 
(date, amount, type, category, subcategory, description, payment_mode,
 is_fixed_expense, recurring_frequency, recurring_id, is_anomaly,
 month, day_of_week, is_weekend)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
"""

success = 0
fail = 0

# -----------------------------
# Insert rows
# -----------------------------
for idx, row in df.iterrows():
    try:
        cursor.execute(insert_query, (
            row["date"],
            row["amount"],
            row["type"],
            row["category"],
            row["subcategory"],
            row["description"],
            row["payment_mode"],
            row["is_fixed_expense"],
            row["recurring_frequency"],
            row["recurring_id"],
            row["is_anomaly"],
            row["month"],
            row["day_of_week"],
            row["is_weekend"]
        ))
        success += 1

    except Exception as e:
        print(f"❌ Failed at row {idx}: {e}")
        fail += 1
        conn.rollback()

# -----------------------------
# Commit + Close
# -----------------------------
conn.commit()

print("==================================")
print("✔ SUCCESS:", success)
print("❌ FAILED:", fail)
print("==================================")

cursor.close()
conn.close()
print("Closed DB connection")