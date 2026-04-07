import boto3

sns = boto3.client('sns')

TOPIC_ARN = "YOUR_SNS_ARN"

def lambda_handler(event, context):
    if isinstance(event, list):
        volume_list = event
    else:
        volume_list = event.get('Payload', [])

    message = f"Converted volumes: {volume_list}"

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="EBS Converted",
        Message=message
    )

    return "Done"
