import boto3
import os

# MinIO configuration
endpoint = "http://localhost:9000"
access_key = "minioadmin"
secret_key = "minioadmin"
bucket_name = "dta_bucket"

# Initialize MinIO client
s3 = boto3.client('s3', endpoint_url=endpoint, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# Upload files to MinIO
for file in os.listdir("data"):
    file_path = os.path.join("data", file)
    s3.upload_file(file_path, bucket_name, file)