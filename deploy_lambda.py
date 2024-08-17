import boto3
import zipfile
import os

# AWS configuration
LAMBDA_FUNCTION_NAME = 'RealTimeDataHandler'
LAMBDA_ROLE_ARN = 'arn:aws:iam::211125559197:role/Project1Role'  # Replace with your IAM role ARN
AWS_REGION = 'us-east-1'  # Replace with your AWS region

def zip_lambda_code():
    """
    Zip the Lambda function code.
    """
    with zipfile.ZipFile('lambda_function.zip', 'w') as zipf:
        zipf.write('lambda_function.py', arcname='lambda_function.py')

def deploy_lambda_function():
    """
    Deploy or update the Lambda function.
    """
    client = boto3.client('lambda', region_name=AWS_REGION)
    
    with open('lambda_function.zip', 'rb') as f:
        zipped_code = f.read()
    
    try:
        # Check if the function exists
        response = client.get_function(FunctionName=LAMBDA_FUNCTION_NAME)
        function_exists = True
    except client.exceptions.ResourceNotFoundException:
        function_exists = False
    
    if function_exists:
        # Update existing Lambda function
        response = client.update_function_code(
            FunctionName=LAMBDA_FUNCTION_NAME,
            ZipFile=zipped_code
        )
    else:
        # Create new Lambda function
        response = client.create_function(
            FunctionName=LAMBDA_FUNCTION_NAME,
            Runtime='python3.9',
            Role=LAMBDA_ROLE_ARN,
            Handler='lambda_function.lambda_handler',
            Code=dict(ZipFile=zipped_code),
            Timeout=60,
            MemorySize=128
        )
    
    print("Lambda function deployed/updated:")
    print(response)

def clean_up():
    """
    Clean up local files.
    """
    if os.path.exists('lambda_function.zip'):
        os.remove('lambda_function.zip')

if __name__ == "__main__":
    try:
        zip_lambda_code()
        deploy_lambda_function()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        clean_up()
