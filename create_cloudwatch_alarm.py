import boto3

cloudwatch = boto3.client('cloudwatch')

def create_lambda_error_alarm(function_name, sns_topic_arn):
    response = cloudwatch.put_metric_alarm(
        AlarmName=f'{function_name}-Error-Alarm',
        AlarmDescription='Alarm when Lambda function errors exceed 1',
        ActionsEnabled=True,
        AlarmActions=[sns_topic_arn],
        MetricName='Errors',
        Namespace='AWS/Lambda',
        Statistic='Sum',
        Dimensions=[
            {'Name': 'FunctionName', 'Value': function_name}
        ],
        Period=60,
        EvaluationPeriods=1,
        Threshold=1,
        ComparisonOperator='GreaterThanThreshold'
    )
    print("Lambda Error Alarm Created:", response)

def create_lambda_duration_alarm(function_name, sns_topic_arn):
    response = cloudwatch.put_metric_alarm(
        AlarmName=f'{function_name}-Duration-Alarm',
        AlarmDescription='Alarm when Lambda function duration exceeds 1000ms',
        ActionsEnabled=True,
        AlarmActions=[sns_topic_arn],
        MetricName='Duration',
        Namespace='AWS/Lambda',
        Statistic='Average',
        Dimensions=[
            {'Name': 'FunctionName', 'Value': function_name}
        ],
        Period=60,
        EvaluationPeriods=1,
        Threshold=1000,
        ComparisonOperator='GreaterThanThreshold'
    )
    print("Lambda Duration Alarm Created:", response)

def create_dynamodb_throttle_alarm(table_name, sns_topic_arn):
    response = cloudwatch.put_metric_alarm(
        AlarmName=f'{table_name}-Throttle-Alarm',
        AlarmDescription='Alarm when DynamoDB table throttling occurs',
        ActionsEnabled=True,
        AlarmActions=[sns_topic_arn],
        MetricName='WriteThrottleEvents',
        Namespace='AWS/DynamoDB',
        Statistic='Sum',
        Dimensions=[
            {'Name': 'TableName', 'Value': table_name}
        ],
        Period=300,
        EvaluationPeriods=1,
        Threshold=0,
        ComparisonOperator='GreaterThanThreshold'
    )
    print("DynamoDB Throttle Alarm Created:", response)

if __name__ == "__main__":
    lambda_function_name = 'RealTimeDataHandler'
    dynamodb_table_name = 'realtime-transactions-table'
    sns_topic_arn = 'arn:aws:sns:us-east-1:211125559197:realtime-transactions-topic'
    
    create_lambda_error_alarm(lambda_function_name, sns_topic_arn)
    create_lambda_duration_alarm(lambda_function_name, sns_topic_arn)
    create_dynamodb_throttle_alarm(dynamodb_table_name, sns_topic_arn)
