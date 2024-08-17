import json
import boto3
import logging

# Initialize AWS clients
sqs = boto3.client('sqs')

# Invalid SQS Queue URL
INVALID_SQS_QUEUE_URL = 'https://sqs.us-east-2.amazonaws.com/123456789012/invalid-queue'

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function handler to simulate a resource not found error.
    """
    try:
        # Attempt to send a message to an invalid SQS queue
        sqs.send_message(
            QueueUrl=INVALID_SQS_QUEUE_URL,
            MessageBody=json.dumps({'message': 'This will fail'})
        )
    except sqs.exceptions.QueueDoesNotExist as e:
        logger.error(f"SQS Queue does not exist: {str(e)}")
        raise  # Re-raise the exception to trigger the CloudWatch alarm
    
    return {
        'statusCode': 200,
        'body': json.dumps('Function completed successfully')
    }
