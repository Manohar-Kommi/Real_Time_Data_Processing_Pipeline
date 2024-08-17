import boto3
from botocore.exceptions import ClientError

# Initialize AWS clients
dynamodb = boto3.client('dynamodb')

def modify_dynamodb_table(table_name):
    try:
        # Get current table details
        table_description = dynamodb.describe_table(TableName=table_name)
        print(f"Table '{table_name}' already exists.")
        
        # Example: Modify provisioned throughput (Increase read/write capacity units)
        response = dynamodb.update_table(
            TableName=table_name,
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,  
                'WriteCapacityUnits': 5
            }
        )
        print("DynamoDB Table Modified:", response)
    
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Table '{table_name}' does not exist. Creating new table.")
            create_dynamodb_table(table_name)
        else:
            raise

def create_dynamodb_table(table_name):
    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'transaction_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'transaction_id',
                'AttributeType': 'S'  # String type
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("DynamoDB Table Created:", response)
    return response['TableDescription']['TableArn']

if __name__ == "__main__":
    table_name = 'realtime-transactions-table'
    modify_dynamodb_table(table_name)
