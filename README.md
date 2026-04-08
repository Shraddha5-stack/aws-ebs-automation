🚀 AWS EBS Automation Project — gp2 to gp3 Conversion


📌 Project Overview

This project automates the conversion of Amazon Elastic Block Store (EBS) volumes from gp2 to gp3 to optimize cost and improve performance using a fully serverless architecture.

The system uses AWS managed services to automatically detect gp2 volumes, convert them to gp3, log the activity, and send notifications — all without manual intervention.


This is a production-style DevOps automation project suitable for:

DevOps Engineers

Cloud Engineers

AWS Beginners

System Administrators

Portfolio / Resume Projects


🎯 Problem Statement

Many AWS environments still run on gp2 volumes, which:

Cost more than gp3

Have limited performance tuning

Require manual upgrades

Increase operational overhead


Manual conversion is:

Time-consuming

Error-prone

Not scalable


💡 Solution

This project provides a fully automated serverless workflow that:

Scans AWS for gp2 volumes

Filters volumes using tags

Converts gp2 volumes to gp3

Logs conversion details into DynamoDB

Sends email notifications using SNS

Runs automatically on a schedule


🏗 Architecture

EventBridge (Scheduler)
        │
        ▼
Step Functions
        │
 ┌────────────────────┐
 │ Filter Volumes     │
 └────────────────────┘
        │
        ▼
 ┌────────────────────┐
 │ Convert Volumes    │
 └────────────────────┘
        │
        ▼
 ┌────────────────────┐
 │ Log to DynamoDB    │
 └────────────────────┘
        │
        ▼
 ┌────────────────────┐
 │ Send SNS Alert     │
 └────────────────────┘
 

⚙️ AWS Services Used

Service

Purpose

AWS Lambda

Serverless compute

AWS Step Functions

Workflow orchestration

Amazon DynamoDB

Store logs

Amazon SNS

Send notifications

Amazon EventBridge

Schedule automation

Amazon EC2 / EBS

Volume management

Amazon CloudWatch

Monitoring and logs

IAM

Access control


🛠 Tech Stack

AWS Lambda

Python 3.x

Boto3

AWS Step Functions

DynamoDB

SNS

EventBridge

CloudWatch

IAM


📋 Prerequisites

Before starting, ensure you have:

AWS Account

IAM permissions

Python 3.x installed

AWS CLI configured


Basic understanding of:

AWS Lambda

Step Functions

DynamoDB

SNS


📂 Project Structure


aws-ebs-automation/
│
├── filter-volumes/
│   └── lambda_function.py
│
├── convert-volume/
│   └── lambda_function.py
│
├── log-to-dynamodb/
│   └── lambda_function.py
│
├── send-notification/
│   └── lambda_function.py
│
├── screenshots/
│   ├── step-functions.png
│   ├── dynamodb-logs.png
│   ├── sns-notification.png
│
└── README.md


🔧 Step-by-Step Implementation


Step 1 — Create DynamoDB Table

Table Name:

EBS-Logs

Primary Key:

VolumeId (String)


Purpose:

Store logs of converted volumes.

Step 2 — Create SNS Topic


Topic Name:

EBS-Conversion-Notifications

Create Subscription:

Protocol: Email

Purpose:

Send notification emails after conversion.


Step 3 — Create IAM Role for Lambda

Attach permissions:

AmazonEC2FullAccess
AmazonDynamoDBFullAccess
AmazonSNSFullAccess
CloudWatchLogsFullAccess

Recommended for Production:

Use least privilege policies.


Step 4 — Create Lambda Function — Filter gp2 Volumes

Function Name:

filter-volumes

Runtime:

Python 3.x

Code:

import boto3


ec2 = boto3.client('ec2')


def lambda_handler(event, context):

    volumes = ec2.describe_volumes(
        Filters=[
            {
                'Name': 'tag:AutoConvert',
                'Values': ['true']
            },
            {
                'Name': 'volume-type',
                'Values': ['gp2']
            }
        ]
    )

    volume_ids = [
        v['VolumeId']
        for v in volumes['Volumes']
    ]

    return volume_ids
    

Step 5 — Create Lambda Function — Convert Volumes

Function Name:

convert-volume

Code:

import boto3


ec2 = boto3.client('ec2')


def lambda_handler(event, context):


    volume_list = (
        event
        if isinstance(event, list)
        else event.get('Payload', [])
    )

    results = []

    for vol_id in volume_list:

        ec2.modify_volume(
            VolumeId=vol_id,
            VolumeType='gp3'
        )

        results.append(vol_id)

    return results
    

Step 6 — Create Lambda Function — Log to DynamoDB

Function Name:

log-to-dynamodb

Code:

import boto3
from datetime import datetime


dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('EBS-Logs')


def lambda_handler(event, context):


    volume_list = (
        event
        if isinstance(event, list)
        else event.get('Payload', [])
    )

    for vol in volume_list:

        table.put_item(
            Item={
                'VolumeId': vol,
                'Time': str(datetime.now())
            }
        )

    return volume_list
    

Step 7 — Create Lambda Function — Send Notification

Function Name:

send-notification

Code:

import boto3


sns = boto3.client('sns')


TOPIC_ARN = "YOUR_SNS_ARN"


def lambda_handler(event, context):


    volume_list = (
        event
        if isinstance(event, list)
        else event.get('Payload', [])
    )

    message = f"Converted volumes: {volume_list}"

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="EBS Converted",
        Message=message
    )

    return "Done"
    

Step 8 — Create Step Functions State Machine

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


Step 9 — Trigger Execution Using EventBridge

Create Rule:

EventBridge → Scheduler

Set Target:

Step Functions

Set Frequency:

Daily

Example:

Every day at 02:00 UTC

Step 10 — Testing the Project

Start execution manually:

Step Functions → Start Execution

Verify:

Step Functions execution status

CloudWatch logs

DynamoDB records

Email notifications

Step 11 — Verification Checklist

Step Functions execution successful

DynamoDB contains logs

Email notification received

Volume type changed to gp3

📸 Screenshots

Add screenshots here:

screenshots/

Examples:

Step Functions workflow

DynamoDB logs

SNS email notification

EventBridge schedule

Lambda execution logs

🚀 Key Features

Fully automated workflow

Serverless architecture

Event-driven scheduling

Cost optimization

Logging and monitoring

Notification system

Scalable design

Production-ready architecture

📉 Cost Optimization Benefit

Switching from:

gp2 → gp3

Provides:

Up to 20% lower cost

Better performance control

Independent IOPS configuration

Independent throughput configuration

🔐 Security Best Practices

Use least privilege IAM policies

Enable CloudWatch logging

Use encrypted EBS volumes

Store secrets in environment variables

Use IAM roles instead of access keys

📈 Future Improvements

You can extend this project with:

Terraform automation

CloudFormation template

Slack notifications

Retry mechanism

Dead Letter Queue (DLQ)

Monitoring dashboard

CI/CD pipeline

Multi-region support

🎯 Use Cases

Cost optimization automation

Infrastructure maintenance

Cloud governance

DevOps automation

Enterprise AWS environments

👨‍💻 Author

Satyam MauryaDevOps Engineer | Cloud Engineer | MERN Stack Developer

⭐ If you found this project useful

Give it a star on GitHub and share it with others in the DevOps community.
