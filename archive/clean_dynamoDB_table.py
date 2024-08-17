import boto3

# Initialize AWS DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Configuration
table_name = 'realtimedataprocessing-transactions-table'

def delete_all_items_from_table(table_name):
    table = dynamodb.Table(table_name)
    
    # Scan table to get all items
    response = table.scan()
    data = response['Items']
    
    # Delete each item
    for item in data:
        # Assuming the primary key is 'transaction_id'
        table.delete_item(
            Key={
                'transaction_id': item['transaction_id']
            }
        )
        print(f"Deleted item: {item}")

    # Handle pagination if there are more items
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data = response['Items']
        for item in data:
            table.delete_item(
                Key={
                    'transaction_id': item['transaction_id']
                }
            )
            print(f"Deleted item: {item}")

if __name__ == "__main__":
    delete_all_items_from_table(table_name)
