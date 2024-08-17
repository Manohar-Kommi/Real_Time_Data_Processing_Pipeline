import boto3

def create_sqs_queue(queue_name):
    
    # Initialize the SQS client
    sqs = boto3.client('sqs')

    # Create the SQS queue
    response = sqs.create_queue(
        QueueName=queue_name,
        Attributes={
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '345600' 
        }
    )
    
    print("SQS Queue Created: ", response)
    return response['QueueUrl']

if __name__ == "__main__":
    queue_name = 'realtime-transactions-queue'
    queue_url = create_sqs_queue(queue_name)
    print(f"SQS Queue URL: {queue_url}")
