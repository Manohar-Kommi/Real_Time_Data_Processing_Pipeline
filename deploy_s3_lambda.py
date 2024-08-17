import boto3
import zipfile
import os
from botocore.exceptions import ClientError

# AWS configuration
LAMBDA_FUNCTION_NAME = 's3_bucket_lambda'
LAMBDA_ROLE_ARN = 'arn:aws:iam::211125559197:role/Project1Role'
ZIP_FILE_NAME = 'lambda_function_s3.zip'
LAMBDA_FILE_NAME = 'lambda_function_s3.py'
RUNTIME = 'python3.9'

def zip_lambda_code():
    """
    Zip the Lambda function code.
    """
    if not os.path.isfile(LAMBDA_FILE_NAME):
        raise FileNotFoundError(f"{LAMBDA_FILE_NAME} not found. Please check the file path.")

    with zipfile.ZipFile(ZIP_FILE_NAME, 'w') as zipf:
        # Ensure only the file name is used in the zip
        zipf.write(LAMBDA_FILE_NAME, arcname=os.path.basename(LAMBDA_FILE_NAME))
    print(f"Zipped {LAMBDA_FILE_NAME} into {ZIP_FILE_NAME}")

def deploy_lambda_function():
    """
    Deploy or update the Lambda function.
    """
    client = boto3.client('lambda')

    with open(ZIP_FILE_NAME, 'rb') as f:
        zipped_code = f.read()

    try:
        # Check if the function exists
        response = client.get_function(FunctionName=LAMBDA_FUNCTION_NAME)
        print(f"Lambda function '{LAMBDA_FUNCTION_NAME}' already exists. Updating function.")
        
        # Update function code
        response = client.update_function_code(
            FunctionName=LAMBDA_FUNCTION_NAME,
            ZipFile=zipped_code
        )
        print("Lambda function code updated.")

    except client.exceptions.ResourceNotFoundException:
        print(f"Lambda function '{LAMBDA_FUNCTION_NAME}' does not exist. Creating function.")
        try:
            response = client.create_function(
                FunctionName=LAMBDA_FUNCTION_NAME,
                Runtime=RUNTIME,
                Role=LAMBDA_ROLE_ARN,
                Handler='lambda_function_s3.lambda_handler',
                Code=dict(ZipFile=zipped_code),
                Timeout=300,  # 5 minutes
                MemorySize=128
            )
            print("Lambda function created.")
        except ClientError as e:
            print(f"Failed to create Lambda function: {e}")
            raise

    except ClientError as e:
        print(f"Failed to update Lambda function: {e}")
        raise

    print("Lambda function deployed/updated:")
    print(response)

def clean_up():
    """
    Clean up local files.
    """
    if os.path.exists(ZIP_FILE_NAME):
        os.remove(ZIP_FILE_NAME)
        print(f"Deleted local zip file: {ZIP_FILE_NAME}")

if __name__ == "__main__":
    try:
        zip_lambda_code()
        deploy_lambda_function()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        clean_up()
