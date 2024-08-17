import boto3

def receive_message_from_sqs(queue_url):
    """
    Receive a message from the specified SQS queue and print the receipt handle.

    :param queue_url: The URL of the SQS queue.
    """
    # Initialize the SQS client
    sqs = boto3.client('sqs')

    # Receive a message from the SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=5
    )
    
    messages = response.get('Messages', [])
    
    if messages:
        for message in messages:
            receipt_handle = message['ReceiptHandle']
            message_body = message['Body']
            print(f"Message Body: {message_body}")
            print(f"Receipt Handle: {receipt_handle}")
    else:
        print("No messages available.")

if __name__ == "__main__":
    queue_url = 'https://sqs.us-east-2.amazonaws.com/637423377183/realtimedataprocessing-transactions-queue'
    receive_message_from_sqs(queue_url)
