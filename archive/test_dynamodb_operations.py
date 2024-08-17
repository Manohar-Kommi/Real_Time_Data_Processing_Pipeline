import boto3
from datetime import datetime, timezone

def put_item_to_dynamodb(table_name, transaction_id, amount, item):
    """
    Put an item into the DynamoDB table.

    :param table_name: The name of the DynamoDB table.
    :param transaction_id: The transaction ID.
    :param amount: The amount of the transaction.
    :param item: The item description.
    """
    # Initialize the DynamoDB resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Put the item into the table
    response = table.put_item(
        Item={
            'transaction_id': transaction_id,
            'amount': amount,
            'item': item,
            'timestamp': datetime.now(timezone.utc).isoformat()  # Adding a timestamp
        }
    )
    
    print("Item Put: ", response)

def get_item_from_dynamodb(table_name, transaction_id):
    """
    Get an item from the DynamoDB table.

    :param table_name: The name of the DynamoDB table.
    :param transaction_id: The transaction ID.
    """
    # Initialize the DynamoDB resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Get the item from the table
    response = table.get_item(
        Key={
            'transaction_id': transaction_id
        }
    )
    
    print("Item Retrieved: ", response.get('Item'))

if __name__ == "__main__":
    table_name = 'realtimedataprocessing-transactions-table'
    
    # Put an item into the DynamoDB table
    put_item_to_dynamodb(table_name, '1234', 100, 'Book')
    
    # Retrieve the item from the DynamoDB table
    get_item_from_dynamodb(table_name, '1234')
