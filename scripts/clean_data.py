import pandas as pd
import numpy as np

# Load RAW Excel
df = pd.read_excel(r"D:\Projects\github-projects\money-vision\data\personal_finance_raw.xlsx")

# ============================
# BASIC CLEANING
# ============================

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.sort_values(by="Date").reset_index(drop=True)
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

for col in ['Category','Subcategory','Payment_Mode','Description','Type']:
    df[col] = df[col].astype(str).str.title()

df['Category'] = df['Category'].replace(["Nan","None",""], "Unknown")
df['Subcategory'] = df['Subcategory'].replace(["Nan","None",""], "Other")
df['Description'] = df['Description'].replace(["Nan","None",""], "No Description")

df = df.drop_duplicates()

df['Payment_Mode'] = df['Payment_Mode'].replace({
    'Upi':'UPI', 'Upi ':'UPI', ' Upi':'UPI',
    'Card ':'Card',' Card':'Card',
    'Cash ':'Cash',' Cash':'Cash'
})

df = df[df['Amount'] > 0]

# ============================
# RECOMPUTE NEW COLUMNS
# ============================

df['day_of_week'] = df['Date'].dt.day_name()
df['month'] = df['Date'].dt.month
df['is_weekend'] = df['day_of_week'].isin(['Saturday','Sunday'])

# BOOLEAN FIELDS
df['Is_Fixed_Expense'] = df['Is_Fixed_Expense'].map({'Yes': True, 'No': False})
df['Is_Anomaly'] = df['Is_Anomaly'].fillna(0).astype(int).astype(bool)
df['Recurring_ID'] = df['Recurring_ID'].replace(["NaN","nan"], None)

# ============================
# FINAL COLUMN ORDER
# ============================

df = df.rename(columns={
    "Date":"date",
    "Amount":"amount",
    "Type":"type",
    "Category":"category",
    "Subcategory":"subcategory",
    "Description":"description",
    "Payment_Mode":"payment_mode",
    "Is_Fixed_Expense":"is_fixed_expense",
    "Recurring_Frequency":"recurring_frequency",
    "Recurring_ID":"recurring_id",
    "Is_Anomaly":"is_anomaly"
})

final_columns = [
    "date","amount","type","category","subcategory","description",
    "payment_mode","is_fixed_expense","recurring_frequency","recurring_id",
    "is_anomaly","month","day_of_week","is_weekend"
]

df = df[final_columns]
df = df.where(pd.notnull(df), None)

print("Data cleaned and ready for PostgreSQL!")

output_path = r"D:\Projects\github-projects\money-vision\data\clean_finance_data_for_postgres.csv"

df.to_csv(output_path, index=False)

print("Saved:", output_path)