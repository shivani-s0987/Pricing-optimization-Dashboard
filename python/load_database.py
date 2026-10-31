"""Load processed CSVs into PostgreSQL using DATABASE_URL; schema must exist."""
import os, sys, re
from pathlib import Path
import pandas as pd
try: import sqlalchemy
except ImportError: print('Install requirements first: pip install -r requirements.txt'); raise
ROOT=Path(__file__).resolve().parents[1]; url=os.getenv('DATABASE_URL')
if not url: print('DATABASE_URL is not set. Example: postgresql+psycopg2://user:password@localhost:5432/pricing_analytics'); raise SystemExit(2)
engine=sqlalchemy.create_engine(url)
frames={'dim_product':'dim_product.csv','dim_region':'dim_region.csv','dim_channel':'dim_channel.csv','dim_customer_segment':'dim_customer_segment.csv','dim_date':'dim_date.csv','fact_sales':'fact_sales_clean.csv'}
# This portable loader is intended for an empty schema and loads dimensions before facts.
with engine.begin() as conn:
 for table,file in frames.items():
  df=pd.read_csv(ROOT/'data/processed'/file)
  def snake(name):
   return re.sub(r'(?<!^)(?=[A-Z])','_',name).lower()
  df.columns=[snake(c) for c in df.columns]
  if table=='dim_date': df['date']=pd.to_datetime(df['date']).dt.date
  if table=='fact_sales': df['order_date']=pd.to_datetime(df['order_date']).dt.date
  df.to_sql(table,conn,if_exists='append',index=False,method='multi',chunksize=1000)
  print(f'Loaded {len(df):,} rows into {table}')
