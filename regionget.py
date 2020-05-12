import boto3

# regions = ['us-east-1', 'us-east-2', 'us-west-2']

def get_region(profile, vpc_nm, regions):
    for region in regions:
        session = boto3.Session(profile_name=profile, region_name=region)
        ec2 = session.client('ec2')
        vpcs = ec2.describe_vpcs(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_nm,
                    ]
                },
            ]
        )
        for vpc in vpcs['Vpcs']:
            if vpc_nm in vpc['VpcId']:
                return region
