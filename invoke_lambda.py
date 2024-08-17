import json
import boto3
from botocore.exceptions import ClientError

# Initialize AWS Lambda client
lambda_client = boto3.client('lambda', region_name='us-east-1')

# Configuration
lambda_function_name = 's3_bucket_lambda'  # Lambda function name

def invoke_lambda_function(function_name, payload):
    """
    Invoke the specified Lambda function with the given payload.
    
    :param function_name: The name of the Lambda function.
    :param payload: The payload to pass to the Lambda function.
    :return: The response from the Lambda function invocation.
    """
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',  # Synchronous invocation
            Payload=json.dumps(payload)
        )
        
        # Check if the status code is 200 (OK)
        status_code = response.get('StatusCode', 500)
        if status_code == 200:
            response_payload = json.loads(response['Payload'].read().decode('utf-8'))
            return response_payload
        else:
            print(f"Lambda function returned status code: {status_code}")
            print(f"Full response: {response}")
            return {"error": "Lambda function invocation failed"}
        
    except ClientError as e:
        print(f"Failed to invoke Lambda function: {e}")
        raise

def main():
    # List of S3 file names to process
    file_names = [
        "fitness_transactions.json",
        "electronics_transactions.json",
    ]
    
    # Create payload with file names
    payload = {
        "file_names": file_names
    }
    
    # Invoke the Lambda function
    try:
        response = invoke_lambda_function(lambda_function_name, payload)
        print("Lambda function response:")
        print(json.dumps(response, indent=4))
    except Exception as e:
        print(f"Error invoking Lambda function: {e}")

if __name__ == "__main__":
    main()
