import psycopg2

# Define the database connection details
host = 'postgres' 
username = 'airflow'
password = 'airflow'
database_name = 'airflow'

# Establish a connection to the database
conn = psycopg2.connect(
    host=host,
    user=username,
    password=password,
    dbname=database_name
)

# Create a cursor object to execute queries
cur = conn.cursor()

# Execute a query to retrieve data
query = 'SELECT * FROM my_table'
cur.execute(query)

# Fetch the results
results = cur.fetchall()

# Print the results
for row in results:
    print(row)

# Close the cursor and connection
cur.close()
conn.close()