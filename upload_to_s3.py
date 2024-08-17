import boto3
import os
from botocore.exceptions import ClientError

# Initialize AWS S3 client
s3 = boto3.client('s3')

# Configuration
local_directory = 'data'  # Local directory containing files
s3_bucket_name = 'real-time-ecommerce-processing'
s3_prefix = 'uploaded/'  # S3 folder or prefix where files will be uploaded

def upload_file_to_s3(file_path, bucket_name, s3_file_key):
    """
    Upload a file to S3.
    """
    try:
        with open(file_path, 'rb') as file:
            s3.put_object(Bucket=bucket_name, Key=s3_file_key, Body=file)
        print(f"Uploaded {file_path} to S3 bucket {bucket_name} as {s3_file_key}")
    except ClientError as e:
        print(f"Failed to upload to S3: {e}")
        raise

def upload_all_files(directory, bucket_name, prefix):
    """
    Upload all files in the specified directory to S3.
    """
    try:
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            
            # Skip directories
            if os.path.isfile(file_path):
                s3_file_key = f"{prefix}{file_name}"  # Define the S3 key
                upload_file_to_s3(file_path, bucket_name, s3_file_key)
    except Exception as e:
        print(f"Error uploading files: {e}")

if __name__ == "__main__":
    upload_all_files(local_directory, s3_bucket_name, s3_prefix)
