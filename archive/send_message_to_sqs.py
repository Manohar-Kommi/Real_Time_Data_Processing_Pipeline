import boto3

def send_message_to_sqs(queue_url, message_body):
    """
    Send a message to the specified SQS queue.

    :param queue_url: The URL of the SQS queue.
    :param message_body: The body of the message to send.
    """
    # Initialize the SQS client
    sqs = boto3.client('sqs')

    # Send the message to the SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    
    print("Message Sent: ", response)

if __name__ == "__main__":
    queue_url = 'https://sqs.us-east-2.amazonaws.com/637423377183/realtimedataprocessing-transactions-queue'
    message_body = '{"transaction_id": "4055", "amount": 500000, "item": "MacBook"}'
    send_message_to_sqs(queue_url, message_body)
