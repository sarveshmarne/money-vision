import psycopg2
import pandas as pd

# Load cleaned data
csv_file = r"D:\Projects\github-projects\moneyv-ision\data\clean_finance_data_for_postgres.csv"

df = pd.read_csv(csv_file)

print(f"Loaded {len(df)} rows from clean CSV")

# Connect
conn = psycopg2.connect(
    database="personal_finance",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()
print("Connected to PostgreSQL")

# --------- NEW: TRUNCATE TABLE ----------
print("Truncating table...")
cursor.execute("TRUNCATE TABLE public.transactions;")
conn.commit()
print("Table truncated.")
# ----------------------------------------

# Insert query
insert_query = """
INSERT INTO transactions 
(date, amount, type, category, subcategory, description, payment_mode,
 is_fixed_expense, recurring_frequency, recurring_id, is_anomaly,
 month, day_of_week, is_weekend)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
"""

success = 0
fail = 0

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

conn.commit()

print("==================================")
print("✔ SUCCESS:", success)
print("❌ FAILED:", fail)
print("==================================")

cursor.close()
conn.close()
print("Closed DB connection")