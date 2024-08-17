import json
import boto3
from botocore.exceptions import ClientError

# Initialize AWS clients
s3 = boto3.client('s3')
sqs = boto3.client('sqs')

# Configuration
s3_bucket_name = 'real-time-ecommerce-processing'
queue_url = 'https://sqs.us-east-1.amazonaws.com/211125559197/realtime-transactions-queue'

def upload_file_to_s3(file_name, bucket_name, s3_file_key):
    """
    Upload a file to S3.
    """
    try:
        with open(file_name, 'rb') as file:
            s3.put_object(Bucket=bucket_name, Key=s3_file_key, Body=file)
        print(f"Uploaded {file_name} to S3 bucket {bucket_name} as {s3_file_key}")
    except ClientError as e:
        print(f"Failed to upload to S3: {e}")
        raise

def read_json_from_s3(bucket_name, file_key):
    """
    Read a JSON file directly from S3.
    """
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = obj['Body'].read().decode('utf-8')
        data = json.loads(file_content)
        return data
    except ClientError as e:
        print(f"Failed to read from S3: {e}")
        raise

def send_message_to_sqs(queue_url, message_body):
    """
    Send a message to the specified SQS queue.
    """
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )
        print("Message Sent: ", response)
    except ClientError as e:
        print(f"Failed to send message to SQS: {e}")
        raise

def process_and_send_messages(json_data, queue_url):
    """
    Process JSON data and send each item to SQS.
    """
    for item in json_data:
        message_body = json.dumps(item)
        send_message_to_sqs(queue_url, message_body)

def process_files(file_names, bucket_name, queue_url):
    """
    Process multiple files from S3 and send messages to SQS.
    """
    for file_name in file_names:
        s3_file_key = f"uploaded/{file_name}"  # S3 key where file is stored
        
        # Read JSON file from S3
        data = read_json_from_s3(bucket_name, s3_file_key)
        print(f"Processing file: {file_name}, Data: {data}")  # Debugging line
        
        # Process JSON data and send messages to SQS
        process_and_send_messages(data, queue_url)

def lambda_handler(event, context):
    """
    Lambda function handler to process multiple files.
    """
    # Extract file names from event
    file_names = event.get('file_names', [])
    print(f"Received file names: {file_names}")  # Debugging line

    if not file_names:
        raise ValueError("No file names found in the event.")

    # Process each file and send messages to SQS
    process_files(file_names, s3_bucket_name, queue_url)

    return {
        'statusCode': 200,
        'body': json.dumps('Files processed and messages sent to SQS successfully.')
    }
