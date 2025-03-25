import pandas as pd
from sqlalchemy import create_engine

# Database connection
engine = create_engine("postgresql://admin:password@localhost:5432/dta")

# Load CSV data
df_csv = pd.read_csv('data/DTA.csv')
df_csv.to_sql('dta_csv', engine, if_exists='replace', index=False)

# Load JSON data
df_json = pd.read_json('data/DTA.json')
df_json.to_sql('dta_json', engine, if_exists='replace', index=False)