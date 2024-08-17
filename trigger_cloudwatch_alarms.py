import boto3
import time

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')

def trigger_lambda_error():
    """
    Function to trigger a Lambda error
    """
    response = lambda_client.invoke(
        FunctionName='RealTimeDataHandler',
        InvocationType='Event',
        Payload=b'{"test": "error"}'
    )
    print(f"Lambda error triggered: {response}")

def trigger_lambda_duration():
    """
    Function to trigger a Lambda duration exceedance
    """
    # Invoke the Lambda function with a delay to exceed the duration threshold
    response = lambda_client.invoke(
        FunctionName='RealTimeDataHandler',
        InvocationType='RequestResponse',
        Payload=b'{"test": "duration"}'
    )
    print(f"Lambda duration triggered: {response}")

def trigger_dynamodb_throttle():
    """
    Function to trigger DynamoDB throttle
    """
    table = dynamodb.Table('realtime-transactions-table')
    item = {'transaction_id': 'test', 'amount': 100, 'item': 'TestItem'}

    # Making multiple put_item calls to simulate throttling
    for _ in range(100):
        try:
            table.put_item(Item=item)
        except Exception as e:
            print(f"Expected throttling error: {e}")

if __name__ == "__main__":
    try:
        trigger_lambda_error()
    except Exception as e:
        print(f"Expected error: {e}")

    try:
        trigger_lambda_duration()
    except Exception as e:
        print(f"Expected duration error: {e}")

    try:
        trigger_dynamodb_throttle()
    except Exception as e:
        print(f"Expected throttling error: {e}")

    print("Alarm conditions triggered")
