# lambda_assignment_HeroVired
Lambda Projects using Boto3

# 1. AWS Lambda EC2 Auto Start/Stop Using Tags

## Overview

This project demonstrates how to automate EC2 instance management using AWS Lambda and Boto3. The Lambda function identifies EC2 instances based on specific tags and automatically starts or stops them.

### Objective

* Stop EC2 instances tagged with `Action=Auto-Stop`
* Start EC2 instances tagged with `Action=Auto-Start`
* Use AWS Lambda and Boto3 for automation
* Log all actions to Amazon CloudWatch

## Step 1: Create EC2 Instances

Launch two EC2 instances, each with key as Action and value as Auto-Start and Auto-Stop.

---

## Step 2: Create IAM Role for Lambda

Navigate to:

```text
IAM → Roles → Create Role
```

### Trusted Entity

```text
AWS Service → Lambda
```

### Attach Policies

```text
AmazonEC2FullAccess
AWSLambdaBasicExecutionRole
```

### Example Role Name

```text
Lambda-EC2-Management-Role
```

---

## Step 3: Create Lambda Function

Navigate to:

```text
AWS Lambda → Create Function
```

### Configuration

| Setting        | Value                      |
| -------------- | -------------------------- |
| Function Name  | EC2-Auto-Manager           |
| Runtime        | Python 3.x                 |
| Execution Role | Lambda-EC2-Management-Role |

---

## Step 4: Lambda Function Code

```python
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    # Find running instances tagged Auto-Stop
    stop_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Stop']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )

    stop_instances = []

    for reservation in stop_response['Reservations']:
        for instance in reservation['Instances']:
            stop_instances.append(instance['InstanceId'])

    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)
        print(f"Stopped Instances: {stop_instances}")

    # Find stopped instances tagged Auto-Start
    start_response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Start']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['stopped']
            }
        ]
    )

    start_instances = []

    for reservation in start_response['Reservations']:
        for instance in reservation['Instances']:
            start_instances.append(instance['InstanceId'])

    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        print(f"Started Instances: {start_instances}")

    return {
        'statusCode': 200,
        'body': 'EC2 instance management completed'
    }
```

---

## Step 5: Deploy the Function

Click:

```text
Deploy
```

After deployment, verify that the function is successfully updated.

---

## Step 6: Test the Function

Create a test eventn and click:

```text
Test
```

---

## Step 7: Verify Results

### EC2 Console

Check the state of your instances:

| Tag        | Expected Result       |
| ---------- | --------------------- |
| Auto-Stop  | Instance should stop  |
| Auto-Start | Instance should start |

### CloudWatch Logs

Example output:

```text
Stopped Instances: ['i-0123456789abcdef0']
Started Instances: ['i-0fedcba9876543210']
```

---



