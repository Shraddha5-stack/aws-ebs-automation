# AWS EBS Automation Project

## 📝 Introduction
This project automates the process of converting AWS EBS volumes from **gp2 to gp3**.  

Even if you are a fresher, this project is easy to understand and implement because it uses **serverless AWS services**.  
The workflow ensures:  
- Only the correct volumes are selected using tags  
- Volumes are converted automatically without manual intervention  
- Logs are stored for auditing  
- Notifications are sent when the conversion is complete  

This project helps reduce **AWS costs** while improving performance.

---

## 🖼 Architecture Diagram
> You can replace this placeholder with an actual diagram image showing the workflow.
[EventBridge Scheduler] --> [Step Functions] --> [Lambda: Filter Volumes] --> [Lambda: Convert Volumes] --> [Lambda: Log to DynamoDB] --> [Lambda: Notify via SNS]


---

## 🛠 Tools & AWS Services Used
**Tools:**
- VS Code / any code editor
- GitHub (for version control)
- Browser (for AWS console)

**AWS Services:**
- AWS Lambda  
- AWS Step Functions  
- Amazon DynamoDB  
- Amazon SNS  
- Amazon EventBridge Scheduler  
- AWS IAM (roles & permissions)  

---

## 📌 Prerequisites
Before starting, ensure you have:  
1. AWS account with required permissions  
2. IAM user/role with access to EC2, Lambda, DynamoDB, SNS, Step Functions  
3. GitHub account to save project files (optional)  
4. Basic knowledge of Python  

---

## 🏗 Steps to Execute the Project

### Step 1: Create DynamoDB Table
1. Go to DynamoDB console → Create table  
2. Table name: `EBS-Logs`  
3. Partition key: `VolumeId` (String)  
4. Save the table  

---

### Step 2: Create SNS Topic and Email Subscription
1. Go to SNS console → Create topic  
2. Topic name: `EBS-Conversion-Notifications`  
3. Create subscription → choose **Email** → enter your email  
4. Confirm subscription via email  

---

### Step 3: Create IAM Role for Lambda
1. Go to IAM → Roles → Create role  
2. Select **Lambda** service → Attach policies:  
   - AmazonEC2FullAccess  
   - AmazonDynamoDBFullAccess  
   - AmazonSNSFullAccess  
3. Save role → Note the **Role ARN**  

---

### Step 4: Create Lambda Function – Scan GP2 Volumes
1. Go to Lambda console → Create function → Author from scratch  
2. Function name: `filter-volumes`  
3. Runtime: Python 3.x  
4. Assign IAM role created earlier  

**Lambda code for scanning volumes:**
```python
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
Create Lambda function: convert-volume
Assign IAM role → Python 3.x

Lambda code to convert gp2 → gp3:
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

Lambda code:
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

Lambda code:
import boto3

sns = boto3.client('sns')
TOPIC_ARN = "YOUR_SNS_ARN"

def lambda_handler(event, context):
    volume_list = event if isinstance(event, list) else event.get('Payload', [])
    message = f"Converted volumes: {volume_list}"
    sns.publish(TopicArn=TOPIC_ARN, Subject="EBS Converted", Message=message)
    return "Done"

Step 8: Create Step Functions State Machine
1. Go to Step Functions → Create state machine
2. Define workflow:
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
Use EventBridge Scheduler → Create rule → Target → Step Functions → Choose your state machine
Set to run daily or as needed


Step 10: Test the Project
Trigger execution manually from Step Functions → Start execution
Check logs in CloudWatch for Lambda functions
Verify DynamoDB table EBS-Logs for entries
Confirm email notification received from SNS

Step 11: Verify Project Flow
Step Functions Execution History shows workflow success
DynamoDB has logged all converted volumes
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
│  ├─ Screenshot from 2026-04-08 00-12-01.png
│  ├─ Screenshot from 2026-04-08 00-12-13.png
│  ├─ Screenshot from 2026-04-08 00-58-55.png
│  ├─ Screenshot from 2026-04-08 01-18-15.png
│  └─ Screenshot from 2026-04-08 01-20-15.png
└─ README.md

📌 Summary

This project provides a fully automated serverless workflow to convert EBS volumes from gp2 to gp3.

Reduces cost and improves performance
Stores logs in DynamoDB for auditing
Sends notifications via SNS
Runs daily without manual intervention
