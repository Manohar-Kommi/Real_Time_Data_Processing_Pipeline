import boto3

# Initialize AWS DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Configuration
table_name = 'realtimedataprocessing-transactions-table'

def check_table_content(table_name):
    table = dynamodb.Table(table_name)
    
    # Scan table to get all items
    response = table.scan()
    data = response.get('Items', [])
    
    # Print the content of the table
    if data:
        print("Table content:")
        for item in data:
            print(item)
    else:
        print("The table is empty.")

    # Handle pagination if there are more items
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data = response.get('Items', [])
        for item in data:
            print(item)

if __name__ == "__main__":
    check_table_content(table_name)
