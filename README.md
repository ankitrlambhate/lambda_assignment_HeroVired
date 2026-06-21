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

# 2. AWS Lambda EBS Snapshot Automation

## Objective

Automate the creation of EBS snapshots and delete snapshots older than 30 days using AWS Lambda, Boto3, and Amazon EventBridge.

---

## Step 1: Identify EBS Volume

1. Navigate to **EC2 Console** → **Volumes**.
2. Select the EBS volume to back up.
3. Copy the Volume ID.

Example:

```text
vol-0123456789abcdef0
```

---

## Step 2: Create IAM Role

1. Open **IAM Console**.
2. Create a new role for **Lambda**.
3. Attach the policy:

```text
AmazonEC2FullAccess
```

4. Save the role.

---

## Step 3: Create Lambda Function

1. Open **AWS Lambda**.
2. Click **Create Function**.
3. Choose **Author from Scratch**.
4. Runtime: **Python 3.x**
5. Assign the IAM role created earlier.

---

## Step 4: Add Lambda Code

The Lambda function performs the following actions:

* Creates a snapshot of the specified EBS volume.
* Tags the snapshot.
* Identifies snapshots older than 30 days.
* Deletes outdated snapshots.
* Logs created and deleted snapshot IDs.

# Note: Update the code with your EBS Volume ID before deployment.

Deploy the function after saving the code.

---

## Step 5: Test the Function

1. Create a test event.
2. Use the following event payload:

```json
{}
```

3. Execute the test.
4. Verify successful execution in Lambda logs.

---

## Step 6: Verify Snapshot Creation

1. Navigate to **EC2 Console** → **Snapshots**.
2. Confirm that a new snapshot has been created.
3. Verify the snapshot contains the expected tags.

---

## Step 7: Monitor Execution

1. Open the Lambda function.
2. Navigate to **Monitor**.
3. View **CloudWatch Logs**.
4. Confirm snapshot creation and cleanup activities.

Example log output:

```text
Created Snapshot: snap-xxxxxxxx
Deleted Snapshot: snap-yyyyyyyy
```

---

# 3. Auto-Tagging EC2 Instances on Launch Using AWS Lambda and Boto3

## Objective

Automatically tag newly launched EC2 instances with:

* LaunchDate (current date)
* Environment = DEVELOPMENT

---

## Step 1: Create IAM Role

1. Open the IAM Console.
2. Create a new role for Lambda.
3. Attach the following policies:

   * AmazonEC2FullAccess
   * AWSLambdaBasicExecutionRole
4. Name the role:

   ```
   LambdaEC2AutoTagRole
   ```

---

## Step 2: Create Lambda Function

1. Open the Lambda Console.
2. Click **Create Function**.
3. Select **Author from Scratch**.
4. Enter:

   * Function Name: `EC2AutoTagger`
   * Runtime: Python 3.x
5. Select the IAM role created earlier.
6. Paste the provided Python code.
7. Deploy the function.

---

## Step 3: Create EventBridge Rule

1. Open the EventBridge Console.

2. Click **Create Rule**.

3. Configure:

   * Rule Name: `EC2LaunchTrigger`
   * Event Bus: `default`
   * Rule Type: `Rule with an event pattern`

4. Use the following event pattern:

```json
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Instance State-change Notification"],
  "detail": {
    "state": ["running"]
  }
}
```

5. Select the Lambda function `EC2AutoTagger` as the target.
6. Create the rule.

---

## Step 4: Test the Solution

1. Launch a new EC2 instance.
2. Wait for the instance to reach the **Running** state.
3. EventBridge will trigger the Lambda function.
4. Lambda will automatically add the tags.

---

## Step 5: Verify Tags

1. Open the EC2 Console.
2. Select the newly launched instance.
3. Open the **Tags** tab.
4. Verify the following tags exist:

| Key         | Value        |
| ----------- | ------------ |
| LaunchDate  | Current Date |
| Environment | DEVELOPMENT  |

---

## Monitoring

To verify execution:

1. Open CloudWatch Logs.
2. Navigate to the Lambda log group.
3. Confirm the message:

```
Successfully tagged instance <instance-id>
```

---







