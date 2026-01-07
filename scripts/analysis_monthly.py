# analysis_monthly.py
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    dbname="personal_finance",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

# Monthly totals
sql_month = "SELECT month, SUM(amount) AS total_spent FROM public.transactions GROUP BY month ORDER BY month;"
df_month = pd.read_sql(sql_month, conn)

# Category totals overall
sql_cat = "SELECT category, SUM(amount) as total_spent FROM public.transactions GROUP BY category ORDER BY total_spent DESC LIMIT 30;"
df_cat = pd.read_sql(sql_cat, conn)

conn.close()

# Plot monthly spending line
plt.figure(figsize=(10,5))
plt.plot(df_month['month'], df_month['total_spent'], marker='o')
plt.title('Monthly Spending')
plt.xlabel('Month (1-12)')
plt.ylabel('Total Spent')
plt.grid(True)
plt.tight_layout()
plt.savefig('monthly_spending.png')
plt.show()

# Top categories bar
plt.figure(figsize=(10,6))
plt.barh(df_cat['category'][::-1], df_cat['total_spent'][::-1])
plt.title('Top Categories by Spend (overall)')
plt.xlabel('Total Spent')
plt.tight_layout()
plt.savefig('top_categories.png')
plt.show()