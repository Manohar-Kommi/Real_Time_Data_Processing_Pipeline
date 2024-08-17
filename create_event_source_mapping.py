import boto3

# Initialize Boto3 clients for Lambda and SQS
lambda_client = boto3.client('lambda', region_name='us-east-1')
sqs_client = boto3.client('sqs', region_name='us-east-1')

# Define the Lambda function name and SQS queue ARN
function_name = 'RealTimeDataHandler'  # Ensure this Lambda function exists
queue_arn = 'arn:aws:sqs:us-east-1:211125559197:realtime-transactions-queue'

# Get the URL of the SQS queue
response = sqs_client.get_queue_url(QueueName='realtime-transactions-queue')
queue_url = response['QueueUrl']

# Create the event source mapping
response = lambda_client.create_event_source_mapping(
    EventSourceArn=queue_arn,
    FunctionName=function_name,
    BatchSize=10,  # Number of messages to retrieve in one batch
    Enabled=True
)

# Print the response
print("Event Source Mapping Created: ", response)
