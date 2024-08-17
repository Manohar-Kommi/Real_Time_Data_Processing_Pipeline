import boto3
import json

def create_iam_role(role_name, trust_policy):
    """
    Create an IAM role with the specified trust policy.

    :param role_name: The name of the IAM role.
    :param trust_policy: The trust policy JSON document.
    :return: The ARN of the created IAM role.
    """
    # Initialize the IAM client
    iam = boto3.client('iam')

    # Create the IAM role
    response = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=trust_policy
    )
    
    print("IAM Role Created: ", response)
    return response['Role']['Arn']

def attach_policy_to_role(role_name, policy_arn):
    """
    Attach an IAM policy to a role.

    :param role_name: The name of the IAM role.
    :param policy_arn: The ARN of the IAM policy to attach.
    """
    # Initialize the IAM client
    iam = boto3.client('iam')

    # Attach the policy to the role
    response = iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )
    
    print("Policy Attached: ", response)

if __name__ == "__main__":
    # Define the trust policy for Lambda execution role
    trust_policy = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    })

    # Create the IAM role
    role_name = 'Project1Role'
    role_arn = create_iam_role(role_name, trust_policy)
    
    # Policy ARNs
    #For Learning and Project Purpose I have given complete access for all the policies
    policies = [
        'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole', 
        'arn:aws:iam::aws:policy/AmazonSQSFullAccess',
        'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess',
        'arn:aws:iam::aws:policy/AmazonSNSFullAccess',
        'arn:aws:iam::aws:policy/CloudWatchEventsFullAccess',
        'arn:aws:iam::aws:policy/AmazonS3FullAccess'
    ]
    
    # Attach policies to the role
    for policy_arn in policies:
        attach_policy_to_role(role_name, policy_arn)
    
    print(f"IAM Role ARN: {role_arn}")
