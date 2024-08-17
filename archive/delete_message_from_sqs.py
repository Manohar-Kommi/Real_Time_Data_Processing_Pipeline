import boto3

def delete_message_from_sqs(queue_url, receipt_handle):
    """
    Delete a message from the specified SQS queue.

    :param queue_url: The URL of the SQS queue.
    :param receipt_handle: The receipt handle of the message to delete.
    """
    # Initialize the SQS client
    sqs = boto3.client('sqs')

    # Delete the message from the SQS queue
    response = sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    
    print("Message Deleted: ", response)

if __name__ == "__main__":
    queue_url = 'https://sqs.us-east-2.amazonaws.com/637423377183/realtimedataprocessing-transactions-queue'
    receipt_handle = 'AQEBHArMI93hEo2WLFW7GrIQgOhWFz4RyuRF5j+3Mwrl96NGVZZLGqBYf1NwTozWvUw04hlLdp42u3Qv0XCA55IbgKJzEmoovbGWGlwZ2okgJ29vxMkJAHXHWm+TLzYpTWt1wtGqDPRWElqQC/97iqSN0PQHAO1AxiZqShHUBHUUhiaDm5Df3dIs7288KchlHeRflBTTBV1Z2Bm13skfVSuXV9wqbR0E66BwqnAhQV25NyhfGhLdwYIBGxynEhv0qsksvLIz03z5FvcdTPkQmhB2hBRd3fybY119PQyqokiZv9ogF8zxyYbfNrPuuDJAHXjn+U78SWikCCGAPLyI7AyPQJY2nyNR03DmgSLw+u6xzJQJJOyGRI0sdX//yrvcnGbSSsx6D0JXmGxyU6XbqmJk6cEe/eoZo5rmpsHMJO5kA1+vuMOfYhmjRUkJEnDGMHbA'
    delete_message_from_sqs(queue_url, receipt_handle)
