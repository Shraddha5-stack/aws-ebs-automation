AWS EBS Automation Project

📝 Introduction

This project automates the conversion of AWS EBS volumes from gp2 → gp3 to optimize cost and performance.
It uses serverless architecture with AWS Lambda, Step Functions, DynamoDB, SNS, and EventBridge for fully automated workflows.


🔧 Prerequisites

Before starting, ensure you have:

AWS account with necessary permissions
IAM roles for Lambda functions
Python 3.x knowledge
Basic understanding of AWS Lambda, Step Functions, DynamoDB, and SNS


🛠 Tools & AWS Services Used
AWS Lambda – Serverless compute for code execution
AWS Step Functions – Orchestrates workflow
Amazon DynamoDB – Stores logs of converted volumes
Amazon SNS – Sends email notifications
Amazon EventBridge – Triggers automation on schedule


📂 Step-by-Step Implementation

Step 1: Create DynamoDB Table
Table name: EBS-Logs
Primary key: VolumeId (String)

Step 2: Create SNS Topic
Topic name: EBS-Conversion-Notifications
Create an email subscription to receive notifications

Step 3: Create IAM Role for Lambda
Assign permissions: EC2 modify, DynamoDB write, SNS publish

Step 4: Create Lambda Function – Scan gp2 Volumes
Function name: filter-volumes
Runtime: Python 3.x
Code:
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    volumes = ec2.describe_volumes(
        Filters=[{'Name': 'tag:AutoConvert', 'Values': ['true']},
                 {'Name': 'volume-type', 'Values': ['gp2']}]
    )
    volume_ids = [v['VolumeId'] for v in volumes['Volumes']]
    return volume_ids
    
Step 5: Create Lambda Function – Convert Volumes
Function name: convert-volume
Runtime: Python 3.x
Code:
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    volume_list = event if isinstance(event, list) else event.get('Payload', [])
    results = []
    for vol_id in volume_list:
        ec2.modify_volume(VolumeId=vol_id, VolumeType='gp3')
        results.append(vol_id)
    return results
    
    
Step 6: Create Lambda Function – Log to DynamoDB
Function name: log-to-dynamodb
Code:
import boto3

from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EBS-Logs')

def lambda_handler(event, context):
    volume_list = event if isinstance(event, list) else event.get('Payload', [])
    for vol in volume_list:
        table.put_item(Item={'VolumeId': vol, 'Time': str(datetime.now())})
    return volume_list

    
Step 7: Create Lambda Function – Send Notification via SNS
Function name: send-notification
Code:
import boto3

sns = boto3.client('sns')
TOPIC_ARN = "YOUR_SNS_ARN"  # Replace with your actual ARN

def lambda_handler(event, context):
    volume_list = event if isinstance(event, list) else event.get('Payload', [])
    message = f"Converted volumes: {volume_list}"
    sns.publish(TopicArn=TOPIC_ARN, Subject="EBS Converted", Message=message)
    return "Done"

    
Step 8: Create Step Functions State Machine
Create workflow in Step Functions:
{
  "Comment": "EBS Automation Workflow",
  "StartAt": "FilterVolumes",
  "States": {
    "FilterVolumes": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:filter-volumes",
      "Next": "ConvertVolumes"
    },
    "ConvertVolumes": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:convert-volume",
      "Next": "LogVolumes"
    },
    "LogVolumes": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:log-to-dynamodb",
      "Next": "Notify"
    },
    "Notify": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:send-notification",
      "End": true
    }
  }
}


Step 9: Trigger Execution
Use EventBridge Scheduler → Create a rule → Target → Step Functions
Set frequency (e.g., daily)


Step 10: Test the Project
Start execution manually in Step Functions
Check CloudWatch logs for Lambda functions
Verify DynamoDB table for logged volumes
Confirm email notifications


Step 11: Verify Project Flow
Step Functions execution history shows workflow success
DynamoDB has all converted volume logs
Email notifications confirm conversions

📂 Repository Structure

aws-ebs-automation/
├─ filter-volumes/
│  └─ lambda_function.py
├─ convert-volume/
│  └─ lambda_function.py
├─ log-to-dynamodb/
│  └─ lambda_function.py
├─ send-notification/
│  └─ lambda_function.py
├─ screenshot/
│  ├─ Screenshot from 2026-04-08 00-03-44.png
│  ├─ Screenshot from 2026-04-08 00-07-27.png
│  └─ ... other screenshots
└─ README.md

📌 Summary

This project provides a fully automated serverless workflow to convert EBS volumes from gp2 → gp3, reducing cost, improving performance, and maintaining logs and notifications. It’s beginner-friendly and a great portfolio project for freshers.



