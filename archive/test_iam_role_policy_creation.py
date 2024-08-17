import boto3
from botocore.exceptions import ClientError

# Initialize IAM client
iam_client = boto3.client('iam')

def check_iam_role(role_name):
    try:
        # Get the IAM role
        response = iam_client.get_role(RoleName=role_name)
        print(f"Role '{role_name}' exists.")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            print(f"Role '{role_name}' does not exist.")
        else:
            print(f"Error occurred: {e}")
        return None

def check_policy_attached(role_name, policy_arn):
    try:
        # List the attached policies for the IAM role
        response = iam_client.list_attached_role_policies(RoleName=role_name)
        for policy in response['AttachedPolicies']:
            if policy['PolicyArn'] == policy_arn:
                print(f"Policy '{policy_arn}' is attached to the role '{role_name}'.")
                return True
        print(f"Policy '{policy_arn}' is NOT attached to the role '{role_name}'.")
        return False
    except ClientError as e:
        print(f"Error occurred: {e}")
        return False

def test_iam_role_and_policies(role_name, policies):
    # Check if the IAM role exists
    role = check_iam_role(role_name)
    if role:
        # Check if each policy is attached
        for policy_arn in policies:
            check_policy_attached(role_name, policy_arn)

if __name__ == "__main__":
    # Define the IAM role name
    role_name = 'LambdaExecutionRole'
    
    # Define the policy ARNs to be tested
    policies = [
        'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole', 
        'arn:aws:iam::aws:policy/AmazonSQSFullAccess',
        'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess',
        'arn:aws:iam::aws:policy/AmazonSNSFullAccess',
        'arn:aws:iam::aws:policy/CloudWatchEventsFullAccess',
        'arn:aws:iam::aws:policy/AmazonS3FullAccess'
    ]

    # Test the IAM role and attached policies
    test_iam_role_and_policies(role_name, policies)
