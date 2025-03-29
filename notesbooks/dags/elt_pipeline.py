from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

import boto3
import pandas as pd
import json
import os
import logging
from datetime import datetime, timedelta
import io

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('airflow.elt_pipeline')

# Default arguments for the DAG
default_args = {
    'owner': 'Group6_DTA',
    'depends_on_past': False,
    'email': ['group6@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'elt_pipeline',
    default_args=default_args,
    description='ELT pipeline for processing CSV, JSON, and PDF data',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=['elt', 'group6', 'DTA'],
)

# Functions for the pipeline

def load_minio_config():
    """Load MinIO configuration from config file"""
    try:
        with open('/opt/airflow/minio-config/config.json', 'r') as config_file:
            config = json.load(config_file)
            minio_config = config.get('minio', {})
            
            return {
                'endpoint': f"http://{minio_config.get('endpoint', 'minio:9000')}",
                'access_key': minio_config.get('access_key', 'minioadmin'),
                'secret_key': minio_config.get('secret_key', 'minioadmin'),
                'bucket_name': minio_config.get('bucket_name', 'dta_bucket')
            }
    except Exception as e:
        logger.warning(f"Could not load config file, using defaults: {str(e)}")
        # Default MinIO configuration
        return {
            'endpoint': "http://minio:9000",
            'access_key': "minioadmin",
            'secret_key': "minioadmin",
            'bucket_name': "dta_bucket"
        }

def ingest_data(**context):
    """Run the ingest_data.py script to process data files and upload to MinIO"""
    logger.info("Running data ingestion script")
    
    # In a real implementation, you'd use BashOperator or better yet, 
    # refactor the ingest_data.py script to be importable here
    # For this example, we'll simulate success
    return "Data ingestion completed successfully"

def load_csv_data_from_minio(**context):
    """Load e-commerce CSV data from MinIO and store in PostgreSQL"""
    logger.info("Loading CSV data from MinIO to PostgreSQL")
    
    try:
        # Get MinIO config
        minio_config = load_minio_config()
        
        # Connect to MinIO
        s3 = boto3.client('s3', 
                      endpoint_url=minio_config['endpoint'], 
                      aws_access_key_id=minio_config['access_key'], 
                      aws_secret_access_key=minio_config['secret_key'])
        
        # List objects in bucket to find cleaned CSV files
        objects = s3.list_objects_v2(Bucket=minio_config['bucket_name'])
        
        # Find cleaned CSV files
        csv_files = [obj['Key'] for obj in objects.get('Contents', []) 
                  if obj['Key'].startswith('cleaned_') and obj['Key'].endswith('.csv')]
        
        # For each CSV file, load into PostgreSQL
        for file_key in csv_files:
            logger.info(f"Processing file {file_key} from MinIO")
            
            # Get the file from MinIO
            response = s3.get_object(Bucket=minio_config['bucket_name'], Key=file_key)
            csv_content = response['Body'].read()
            
            # Load into pandas DataFrame
            df = pd.read_csv(io.BytesIO(csv_content))
            
            # Create table name from file name
            table_name = f"ecommerce_{os.path.splitext(file_key)[0].replace('cleaned_', '')}"
            
            # Connect to PostgreSQL and load data
            pg_hook = PostgresHook(postgres_conn_id="postgres_default")
            engine = pg_hook.get_sqlalchemy_engine()
            
            # Load data to PostgreSQL
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            logger.info(f"Loaded {len(df)} rows into table {table_name}")
            
        return f"Loaded {len(csv_files)} CSV files from MinIO to PostgreSQL"
        
    except Exception as e:
        logger.error(f"Error loading CSV data: {str(e)}")
        raise

def load_json_data_from_minio(**context):
    """Load customer review JSON data from MinIO and store in PostgreSQL"""
    logger.info("Loading JSON data from MinIO to PostgreSQL")
    
    try:
        # Get MinIO config
        minio_config = load_minio_config()
        
        # Connect to MinIO
        s3 = boto3.client('s3', 
                      endpoint_url=minio_config['endpoint'], 
                      aws_access_key_id=minio_config['access_key'], 
                      aws_secret_access_key=minio_config['secret_key'])
        
        # List objects in bucket to find processed JSON files
        objects = s3.list_objects_v2(Bucket=minio_config['bucket_name'])
        
        # Find processed JSON files
        json_files = [obj['Key'] for obj in objects.get('Contents', []) 
                   if obj['Key'].startswith('processed_') and obj['Key'].endswith('.json')]
        
        # For each JSON file, load into PostgreSQL
        for file_key in json_files:
            logger.info(f"Processing file {file_key} from MinIO")
            
            # Get the file from MinIO
            response = s3.get_object(Bucket=minio_config['bucket_name'], Key=file_key)
            json_content = response['Body'].read()
            
            # Load into pandas DataFrame
            df = pd.read_json(io.BytesIO(json_content))
            
            # Create table name from file name
            table_name = f"reviews_{os.path.splitext(file_key)[0].replace('processed_', '')}"
            
            # Connect to PostgreSQL and load data
            pg_hook = PostgresHook(postgres_conn_id="postgres_default")
            engine = pg_hook.get_sqlalchemy_engine()
            
            # Load data to PostgreSQL
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            logger.info(f"Loaded {len(df)} rows into table {table_name}")
            
        return f"Loaded {len(json_files)} JSON files from MinIO to PostgreSQL"
        
    except Exception as e:
        logger.error(f"Error loading JSON data: {str(e)}")
        raise

def load_pdf_data_from_minio(**context):
    """Load financial report PDF data from MinIO and store in PostgreSQL"""
    logger.info("Loading PDF-extracted data from MinIO to PostgreSQL")
    
    try:
        # Get MinIO config
        minio_config = load_minio_config()
        
        # Connect to MinIO
        s3 = boto3.client('s3', 
                      endpoint_url=minio_config['endpoint'], 
                      aws_access_key_id=minio_config['access_key'], 
                      aws_secret_access_key=minio_config['secret_key'])
        
        # List objects in bucket to find processed PDF files (as CSV)
        objects = s3.list_objects_v2(Bucket=minio_config['bucket_name'])
        
        # Find processed PDF data files (saved as CSV)
        pdf_files = [obj['Key'] for obj in objects.get('Contents', []) 
                  if obj['Key'].startswith('processed_') and '.pdf' in obj['Key'] and obj['Key'].endswith('.csv')]
        
        # For each PDF data file, load into PostgreSQL
        for file_key in pdf_files:
            logger.info(f"Processing file {file_key} from MinIO")
            
            # Get the file from MinIO
            response = s3.get_object(Bucket=minio_config['bucket_name'], Key=file_key)
            csv_content = response['Body'].read()
            
            # Load into pandas DataFrame
            df = pd.read_csv(io.BytesIO(csv_content))
            
            # Create table name from file name (extract original PDF name)
            base_name = os.path.splitext(file_key)[0].replace('processed_', '')
            table_name = f"financial_{base_name.replace('.pdf', '')}"
            
            # Connect to PostgreSQL and load data
            pg_hook = PostgresHook(postgres_conn_id="postgres_default")
            engine = pg_hook.get_sqlalchemy_engine()
            
            # Load data to PostgreSQL
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            logger.info(f"Loaded {len(df)} rows into table {table_name}")
            
        return f"Loaded {len(pdf_files)} PDF data files from MinIO to PostgreSQL"
        
    except Exception as e:
        logger.error(f"Error loading PDF data: {str(e)}")
        raise

def create_analytics_views(**context):
    """Create analytics views combining data from different sources"""
    logger.info("Creating analytics views in PostgreSQL")
    
    try:
        # Connect to PostgreSQL
        pg_hook = PostgresHook(postgres_conn_id="postgres_default")
        
        # Example view creation - this would need to be adapted to actual table structure
        # and business requirements
        sql = """
        -- Create a view for e-commerce sales analysis
        CREATE OR REPLACE VIEW sales_analysis AS
        SELECT * FROM ecommerce_sample_data;
        
        -- Create a view for customer sentiment analysis
        CREATE OR REPLACE VIEW customer_sentiment AS
        SELECT * FROM reviews_DTA;
        
        -- Create a view for financial performance analysis
        CREATE OR REPLACE VIEW financial_performance AS
        SELECT * FROM financial_DTA;
        """
        
        # Execute SQL
        pg_hook.run(sql)
        
        return "Analytics views created successfully"
        
    except Exception as e:
        logger.error(f"Error creating analytics views: {str(e)}")
        raise

# Define the tasks

# Task to run data ingestion script
t1_ingest_data = BashOperator(
    task_id='ingest_data',
    bash_command='python /opt/airflow/scripts/ingest_data.py',
    dag=dag,
)

# Task to load CSV data from MinIO to PostgreSQL
t2_load_csv = PythonOperator(
    task_id='load_csv_data',
    python_callable=load_csv_data_from_minio,
    provide_context=True,
    dag=dag,
)

# Task to load JSON data from MinIO to PostgreSQL
t3_load_json = PythonOperator(
    task_id='load_json_data',
    python_callable=load_json_data_from_minio,
    provide_context=True,
    dag=dag,
)

# Task to load PDF data from MinIO to PostgreSQL
t4_load_pdf = PythonOperator(
    task_id='load_pdf_data',
    python_callable=load_pdf_data_from_minio,
    provide_context=True,
    dag=dag,
)

# Task to create analytics views
t5_create_views = PythonOperator(
    task_id='create_analytics_views',
    python_callable=create_analytics_views,
    provide_context=True,
    dag=dag,
)

# Set up task dependencies
t1_ingest_data >> [t2_load_csv, t3_load_json, t4_load_pdf] >> t5_create_views