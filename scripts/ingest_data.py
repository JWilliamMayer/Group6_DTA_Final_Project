import boto3
import os
import pandas as pd
import json
import logging
import re
from datetime import datetime
import PyPDF2
import io

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('data_ingestion')

# MinIO configuration - load from config.json
try:
    with open('./minio-config/config.json', 'r') as config_file:
        config = json.load(config_file)
        minio_config = config.get('minio', {})
        
        endpoint = f"http://{minio_config.get('endpoint', 'localhost:9000')}"
        access_key = minio_config.get('access_key', 'minioadmin')
        secret_key = minio_config.get('secret_key', 'minioadmin')
        bucket_name = minio_config.get('bucket_name', 'dta_bucket')
except Exception as e:
    logger.warning(f"Could not load config file, using defaults: {str(e)}")
    # Default MinIO configuration
    endpoint = "http://localhost:9000"
    access_key = "minioadmin"
    secret_key = "minioadmin"
    bucket_name = "dta_bucket"

logger.info(f"Connecting to MinIO at {endpoint}")

# Initialize MinIO client
try:
    s3 = boto3.client('s3', 
                   endpoint_url=endpoint, 
                   aws_access_key_id=access_key, 
                   aws_secret_access_key=secret_key)
    
    # Check if bucket exists, create if not
    try:
        s3.head_bucket(Bucket=bucket_name)
        logger.info(f"Bucket {bucket_name} exists")
    except:
        logger.info(f"Creating bucket {bucket_name}")
        s3.create_bucket(Bucket=bucket_name)
        
except Exception as e:
    logger.error(f"Failed to connect to MinIO: {str(e)}")
    raise

def clean_csv_data(df):
    """Clean and preprocess e-commerce CSV data"""
    logger.info("Cleaning CSV data")
    
    # Make column names lowercase and replace spaces with underscores
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    
    # Drop duplicate rows
    original_count = len(df)
    df = df.drop_duplicates()
    logger.info(f"Removed {original_count - len(df)} duplicate rows")
    
    # Handle missing values
    for col in df.columns:
        missing_count = df[col].isna().sum()
        if missing_count > 0:
            logger.info(f"Column {col} has {missing_count} missing values")
            
            # For numeric columns, fill with median
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            # For string columns, fill with 'Unknown'
            elif pd.api.types.is_string_dtype(df[col]):
                df[col] = df[col].fillna('Unknown')
    
    return df

def process_json_data(file_path):
    """Process customer reviews JSON data"""
    logger.info(f"Processing JSON data from {file_path}")
    
    try:
        # Read the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Convert to DataFrame if it's not already
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            # Handle case where JSON is a dict of records or has a specific structure
            if 'reviews' in data:
                df = pd.DataFrame(data['reviews'])
            else:
                df = pd.DataFrame([data])
        else:
            logger.error(f"Unexpected JSON format in {file_path}")
            return None
        
        # Make column names lowercase and replace spaces with underscores
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        # Basic cleaning
        if 'text' in df.columns:
            # Remove extra whitespace from text
            df['text'] = df['text'].str.strip().str.replace(r'\s+', ' ', regex=True)
        
        # Add sentiment analysis placeholder (would integrate with real sentiment analysis in production)
        if 'text' in df.columns:
            # Simple placeholder sentiment scoring based on text length
            # In a real implementation, this would use NLP libraries like TextBlob, VADER, or a ML model
            df['sentiment_score'] = df['text'].apply(lambda x: 
                                                   min(1.0, len(x) / 1000) if isinstance(x, str) else 0.5)
            
        return df
    
    except Exception as e:
        logger.error(f"Error processing JSON file {file_path}: {str(e)}")
        return None

def extract_text_from_pdf(file_path):
    """Extract text content from PDF file"""
    logger.info(f"Extracting text from PDF {file_path}")
    
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            
            return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
        return ""

def process_pdf_data(file_path):
    """Process financial report PDF data"""
    logger.info(f"Processing PDF data from {file_path}")
    
    try:
        # Extract text from PDF
        text = extract_text_from_pdf(file_path)
        
        # Extract financial data using regex patterns
        # These patterns are basic examples - real implementation would need more robust patterns
        revenue_pattern = r"revenue[\s:]*[$]?([0-9,.]+)"
        profit_pattern = r"(net income|profit)[\s:]*[$]?([0-9,.]+)"
        year_pattern = r"(fiscal year|year)[\s:]*([0-9]{4})"
        
        # Extract data with regex
        revenue_match = re.search(revenue_pattern, text, re.IGNORECASE)
        profit_match = re.search(profit_pattern, text, re.IGNORECASE)
        year_match = re.search(year_pattern, text, re.IGNORECASE)
        
        revenue = revenue_match.group(1).replace(',', '') if revenue_match else None
        profit = profit_match.group(2).replace(',', '') if profit_match else None
        year = year_match.group(2) if year_match else None
        
        # Create structured data
        data = {
            'filename': os.path.basename(file_path),
            'year': year,
            'revenue': revenue,
            'profit': profit,
            'processed_date': datetime.now().strftime('%Y-%m-%d'),
            'text_content': text
        }
        
        # Convert to DataFrame
        df = pd.DataFrame([data])
        return df
    
    except Exception as e:
        logger.error(f"Error processing PDF file {file_path}: {str(e)}")
        return None

def upload_dataframe_to_minio(df, file_name, file_format='csv'):
    """Upload a DataFrame to MinIO in the specified format"""
    logger.info(f"Uploading {file_name} to MinIO in {file_format} format")
    
    try:
        buffer = io.BytesIO()
        
        if file_format.lower() == 'csv':
            df.to_csv(buffer, index=False)
        elif file_format.lower() == 'json':
            df.to_json(buffer, orient='records')
        elif file_format.lower() == 'parquet':
            df.to_parquet(buffer, index=False)
        else:
            logger.error(f"Unsupported file format: {file_format}")
            return False
        
        buffer.seek(0)
        s3.upload_fileobj(buffer, bucket_name, file_name)
        logger.info(f"Successfully uploaded {file_name} to MinIO")
        return True
    
    except Exception as e:
        logger.error(f"Error uploading {file_name} to MinIO: {str(e)}")
        return False

def main():
    """Main function to process all data files"""
    data_dir = "data"
    
    # Process CSV files
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        
        if file.lower().endswith('.csv'):
            logger.info(f"Processing CSV file: {file}")
            try:
                # Read and clean CSV data
                df = pd.read_csv(file_path)
                cleaned_df = clean_csv_data(df)
                
                # Upload cleaned data to MinIO
                cleaned_file_name = f"cleaned_{file}"
                upload_dataframe_to_minio(cleaned_df, cleaned_file_name, 'csv')
                
                # Also save as parquet for analytics
                parquet_file_name = f"cleaned_{os.path.splitext(file)[0]}.parquet"
                upload_dataframe_to_minio(cleaned_df, parquet_file_name, 'parquet')
                
            except Exception as e:
                logger.error(f"Error processing CSV file {file}: {str(e)}")
        
        elif file.lower().endswith('.json'):
            logger.info(f"Processing JSON file: {file}")
            try:
                # Process JSON data
                df = process_json_data(file_path)
                if df is not None:
                    # Upload processed data to MinIO
                    processed_file_name = f"processed_{file}"
                    upload_dataframe_to_minio(df, processed_file_name, 'json')
                    
                    # Also save as parquet for analytics
                    parquet_file_name = f"processed_{os.path.splitext(file)[0]}.parquet"
                    upload_dataframe_to_minio(df, parquet_file_name, 'parquet')
            except Exception as e:
                logger.error(f"Error processing JSON file {file}: {str(e)}")
        
        elif file.lower().endswith('.pdf'):
            logger.info(f"Processing PDF file: {file}")
            try:
                # Process PDF data
                df = process_pdf_data(file_path)
                if df is not None:
                    # Upload processed data to MinIO
                    processed_file_name = f"processed_{os.path.splitext(file)[0]}.json"
                    upload_dataframe_to_minio(df, processed_file_name, 'json')
                    
                    # Also save CSV for database loading
                    csv_file_name = f"processed_{os.path.splitext(file)[0]}.csv"
                    upload_dataframe_to_minio(df, csv_file_name, 'csv')
            except Exception as e:
                logger.error(f"Error processing PDF file {file}: {str(e)}")
        
        else:
            logger.info(f"Skipping unsupported file format: {file}")

if __name__ == "__main__":
    main()