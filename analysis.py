import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2

# Load the data from the PostgreSQL database
conn = psycopg2.connect(
    host='postgres',
    user='airflow',
    password='airflow',
    dbname='airflow'
)
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
rows = cur.fetchall()
df = pd.DataFrame(rows, columns=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'])

# Add a total price column
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Parse InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')

# --- 1. Top 10 selling products ---
top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
top_products.plot(kind='bar', color='skyblue')
plt.title('Top 10 Selling Products')
plt.ylabel('Total Quantity Sold')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# --- 2. Total sales over time (daily) ---
sales_by_date = df.groupby(df['InvoiceDate'].dt.date)['TotalPrice'].sum()

plt.figure(figsize=(12, 5))
sales_by_date.plot()
plt.title('Total Sales Over Time')
plt.ylabel('Sales (£)')
plt.xlabel('Date')
plt.grid(True)
plt.tight_layout()
plt.show()

# --- 3. Total sales by country ---
sales_by_country = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 5))
sales_by_country.plot(kind='bar', color='orange')
plt.title('Top 10 Countries by Sales')
plt.ylabel('Total Sales (£)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# --- 4. Average order value ---
avg_order_value = df.groupby('InvoiceNo')['TotalPrice'].sum().mean()
print(f'💰 Average Order Value: £{avg_order_value:.2f}')

# --- 5. Percent of orders missing CustomerID ---
missing_cust = df['CustomerID'].isna().mean() * 100
print(f'🕵️‍♂️ Orders with missing CustomerID: {missing_cust:.2f}%')