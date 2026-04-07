import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    if isinstance(event, list):
        volume_list = event
    else:
        volume_list = event.get('Payload', [])

    results = []

    for volume_id in volume_list:
        ec2.modify_volume(
            VolumeId=volume_id,
            VolumeType='gp3'
        )
        results.append(volume_id)

    return results
