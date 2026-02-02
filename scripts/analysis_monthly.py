# analysis_monthly.py

import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# =====================================
# Load environment variables
# =====================================
load_dotenv()

# =====================================
# Connect to PostgreSQL securely
# =====================================
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

print("Connected to DB")

# =====================================
# SQL Queries
# =====================================

# Monthly totals
sql_month = """
SELECT month, SUM(amount) AS total_spent
FROM public.transactions
GROUP BY month
ORDER BY month;
"""

# Category totals
sql_cat = """
SELECT category, SUM(amount) AS total_spent
FROM public.transactions
GROUP BY category
ORDER BY total_spent DESC
LIMIT 30;
"""

df_month = pd.read_sql(sql_month, conn)
df_cat = pd.read_sql(sql_cat, conn)

conn.close()

print("Data loaded for analysis")

# =====================================
# Plot monthly spending
# =====================================
plt.figure(figsize=(10, 5))
plt.plot(df_month['month'], df_month['total_spent'], marker='o')
plt.title('Monthly Spending')
plt.xlabel('Month (1-12)')
plt.ylabel('Total Spent')
plt.grid(True)
plt.tight_layout()
plt.show()

# =====================================
# Plot category spending
# =====================================
plt.figure(figsize=(10, 6))
plt.barh(df_cat['category'][::-1], df_cat['total_spent'][::-1])
plt.title('Top Categories by Spend (overall)')
plt.xlabel('Total Spent')
plt.tight_layout()
plt.show()