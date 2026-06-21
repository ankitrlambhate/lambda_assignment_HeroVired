import boto3
from datetime import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    try:
        instance_id = event['detail']['instance-id']

        launch_date = datetime.utcnow().strftime('%Y-%m-%d')

        ec2.create_tags(
            Resources=[instance_id],
            Tags=[
                {
                    'Key': 'LaunchDate',
                    'Value': launch_date
                },
                {
                    'Key': 'Environment',
                    'Value': 'DEVELOPMENT'
                }
            ]
        )

        print(f"Successfully tagged instance {instance_id}")

        return {
            'statusCode': 200,
            'body': f'Tagged {instance_id}'
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise e