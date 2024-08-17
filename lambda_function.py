import json
import boto3
import logging
import time

# Initialize AWS clients
sqs = boto3.client('sqs')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# DynamoDB table name
DYNAMODB_TABLE = 'realtime-transactions-table'
# SNS topic ARN
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:211125559197:realtime-transactions-topic'

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function handler to process SQS messages, validate data, store in DynamoDB, and send notifications.
    """
    table = dynamodb.Table(DYNAMODB_TABLE)
    
    logger.info(f"Received event: {json.dumps(event)}")
    
    # Check for test inputs to trigger alarms
    if 'test' in event:
        if event['test'] == 'error':
            raise Exception("Intentional error to trigger CloudWatch alarm")
        elif event['test'] == 'duration':
            time.sleep(10)  # Sleep for 10 seconds to exceed the duration threshold
            return {'statusCode': 200, 'body': json.dumps('Duration test completed')}
    
    record_count = len(event.get('Records', []))
    logger.info(f"Number of records in event: {record_count}")
    
    for record in event.get('Records', []):
        try:
            # Get the message body
            logger.info(f"Processing record: {json.dumps(record)}")
            message_body = json.loads(record['body'])
            logger.info(f"Message body: {json.dumps(message_body)}")
            amount = message_body.get('amount', 0)
            
            # Example validation: Check if amount is greater than 0
            if amount > 0:
                # Store valid transaction in DynamoDB
                response = table.put_item(Item=message_body)
                logger.info(f"Stored item in DynamoDB: {json.dumps(message_body)}")
                logger.info(f"DynamoDB put_item response: {json.dumps(response)}")
                
                # Send notification via SNS only if amount > 50000
                if amount > 100:
                    sns_response = sns.publish(
                        TopicArn=SNS_TOPIC_ARN,
                        Message=json.dumps({'default': f"Large order detected: {message_body}"}),
                        MessageStructure='json'
                    )
                    logger.info(f"Notification sent via SNS: {json.dumps(message_body)}")
                    logger.info(f"SNS publish response: {json.dumps(sns_response)}")
                else:
                    logger.info(f"No notification sent (amount <= 100): {json.dumps(message_body)}")
            else:
                logger.info(f"Transaction not stored (amount = 0): {json.dumps(message_body)}")
        
        except Exception as e:
            logger.error(f"Error processing record {record}: {str(e)}")
    
    logger.info(f"Processed {record_count} records")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Transactions processed')
    }
