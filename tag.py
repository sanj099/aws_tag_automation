import boto3

def get_untagged_ec2_instances(region):
    untagged_instances = []

    # Create a Boto3 EC2 client using IAM user credentials
    session = boto3.Session(aws_access_key_id='AKIAXLZQCJGM2KOFQBLI',
                            aws_secret_access_key='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',
                            region_name=region)
    ec2_client = session.client('ec2')

    # Describe all EC2 instances in the specified region
    response = ec2_client.describe_instances()

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            tags = instance.get('Tags', [])
            team_tag = next((tag['Value'] for tag in tags if tag['Key'] == 'team'), None)
            cost_center_tag = next((tag['Value'] for tag in tags if tag['Key'] == 'costcenter'), None)

            if not team_tag or not cost_center_tag:
                untagged_instances.append(instance_id)

    return untagged_instances

if __name__ == "__main__":
    region = "us-west-1"
    untagged_instances = get_untagged_ec2_instances(region)
    
    if untagged_instances:
        print("Untagged EC2 instances found:")
        for instance_id in untagged_instances:
            print(f"- {instance_id}")
    else:
        print("No untagged EC2 instances found in the specified region.")
