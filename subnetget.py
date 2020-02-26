import boto3

# Temp variables, replace with logic
profile_nm = "default"
region_nm = "us-east-2"

# Initial setup
session = boto3.Session(profile_name=profile_nm, region_name=region_nm)

# Initiate the session
ec2.session.client('ec2')

# Get public subnets
public_subnets = ec2.describe_subnets(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                '*public*'
            ]
        }
    ]
)

print("Public Subnets")
for subnet in public_subnets['Subnets']:
    print(f"{subnet['AvailabilityZone']}: {subnet['SubnetId']} - {subnet['VpdId']}")

# Get private subnets
private_subnets = ec2.describe_subnets(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                '*private*'
            ]
        }
    ]
)

print("Private Subnets")
for subnet in private_subnets['Subnets']:
    print(f"{subnet['AvailabilityZone']}: {subnet['SubnetId']} - {subnet['VpdId']}")