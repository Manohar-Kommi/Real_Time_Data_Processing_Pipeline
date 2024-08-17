import boto3

def create_sns_topic(topic_name):
    """
    Create an SNS topic with the specified name.

    :param topic_name: The name of the SNS topic.
    :return: The ARN of the created SNS topic.
    """
    # Initialize the SNS client
    sns = boto3.client('sns')

    # Create the SNS topic
    response = sns.create_topic(Name=topic_name)
    topic_arn = response['TopicArn']
    
    print("SNS Topic Created: ", response)
    return topic_arn

def subscribe_to_sns_topic(topic_arn, protocol, endpoint):
    """
    Subscribe to an SNS topic.

    :param topic_arn: The ARN of the SNS topic.
    :param protocol: The protocol to use (e.g., 'email').
    :param endpoint: The endpoint to receive notifications (e.g., email address).
    :return: The subscription ARN.
    """
    # Initialize the SNS client
    sns = boto3.client('sns')

    # Subscribe to the SNS topic
    response = sns.subscribe(
        TopicArn=topic_arn,
        Protocol=protocol,
        Endpoint=endpoint
    )
    
    print("SNS Subscription: ", response)
    return response['SubscriptionArn']


if __name__ == "__main__":
    topic_name = 'realtime-transactions-topic'
    topic_arn = create_sns_topic(topic_name)
    print(f"SNS Topic ARN: {topic_arn}")
    protocol = 'email'  
    endpoint = 'manoharkommi.24@gmail.com'  
    subscription_arn = subscribe_to_sns_topic(topic_arn, protocol, endpoint)
    print(f"SNS Subscription ARN: {subscription_arn}")
