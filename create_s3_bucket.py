import boto3
from botocore.exceptions import ClientError

# Initialize AWS client
s3 = boto3.client('s3')

def create_bucket_if_not_exists(bucket_name, region):
   
    try:
        # Check if the bucket exists
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            # Bucket does not exist, create it
            if region == 'us-east-1':
                s3.create_bucket(Bucket=bucket_name)
            else:
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            print(f"Bucket '{bucket_name}' created.")
        else:
            # Handle other possible exceptions
            raise

if __name__ == "__main__":
    bucket_name = 'real-time-ecommerce-processing'
    region = 'us-east-1' 
    create_bucket_if_not_exists(bucket_name, region)
