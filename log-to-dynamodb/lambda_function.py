import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EBS-Logs')

def lambda_handler(event, context):
    if isinstance(event, list):
        volume_list = event
    else:
        volume_list = event.get('Payload', [])

    for vol in volume_list:
        table.put_item(Item={
            'VolumeId': vol,
            'Time': str(datetime.now())
        })

    return volume_list
