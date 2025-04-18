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
cur.execute('SELECT * FROM sample_data')
rows = cur.fetchall()
df = pd.DataFrame(rows, columns=['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country'])

# Sales analysis by country
country_sales = df.groupby('Country')['UnitPrice'].sum().reset_index()
plt.figure(figsize=(10, 6))
plt.bar(country_sales['Country'], country_sales['UnitPrice'])
plt.title('Sales by Country')
plt.xlabel('Country')
plt.ylabel('Sales Revenue')
plt.show()

# Product popularity
product_popularity = df.groupby('StockCode')['Quantity'].sum().reset_index()
plt.figure(figsize=(10, 6))
plt.bar(product_popularity['StockCode'], product_popularity['Quantity'])
plt.title('Product Popularity')
plt.xlabel('StockCode')
plt.ylabel('Quantity Sold')
plt.show()

# Customer segmentation
customer_segments = df.groupby('CustomerID')['UnitPrice'].sum().reset_index()
customer_segments['Segment'] = pd.qcut(customer_segments['UnitPrice'], q=4, labels=['Low', 'Medium', 'High', 'Very High'])
plt.figure(figsize=(10, 6))
plt.scatter(customer_segments['CustomerID'], customer_segments['UnitPrice'], c=customer_segments['Segment'].map({'Low': 'blue', 'Medium': 'green', 'High': 'red', 'Very High': 'yellow'}))
plt.title('Customer Segmentation')
plt.xlabel('CustomerID')
plt.ylabel('Sales Revenue')
plt.show()

# Time-series analysis
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Month'] = df['InvoiceDate'].dt.month
df['Year'] = df['InvoiceDate'].dt.year
monthly_sales = df.groupby(['Year', 'Month'])['UnitPrice'].sum().reset_index()
plt.figure(figsize=(10, 6))
plt.plot(monthly_sales['Year'], monthly_sales['UnitPrice'], marker='o')
plt.title('Monthly Sales')
plt.xlabel('Year')
plt.ylabel('Sales Revenue')
plt.show()

# Price elasticity analysis
price_elasticity = df.groupby('UnitPrice')['Quantity'].sum().reset_index()
plt.figure(figsize=(10, 6))
plt.scatter(price_elasticity['UnitPrice'], price_elasticity['Quantity'])
plt.title('Price Elasticity')
plt.xlabel('UnitPrice')
plt.ylabel('Quantity Sold')
plt.show()

# Geographic sales distribution
country_sales_map = df.groupby('Country')['UnitPrice'].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.set_style('whitegrid')
sns.barplot(x='Country', y='UnitPrice', data=country_sales_map)
plt.title('Geographic Sales Distribution')
plt.xlabel('Country')
plt.ylabel('Sales Revenue')
plt.show()

# Product recommendation engine
product_recommendations = df.groupby('StockCode')['Quantity'].sum().reset_index()
product_recommendations['Recommendation'] = product_recommendations['Quantity'].apply(lambda x: 'Recommended' if x > 100 else 'Not Recommended')
plt.figure(figsize=(10, 6))
plt.scatter(product_recommendations['StockCode'], product_recommendations['Quantity'], c=product_recommendations['Recommendation'].map({'Recommended': 'green', 'Not Recommended': 'red'}))
plt.title('Product Recommendations')
plt.xlabel('StockCode')
plt.ylabel('Quantity Sold')
plt.show()

# Close the database connection
cur.close()
conn.close()