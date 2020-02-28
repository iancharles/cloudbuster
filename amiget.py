import boto3
import collections
# from datetime import datetime
import datetime
from dateutil import parser


# Temp variables, replace with logic
profile_nm = "default"
# region_nm = "us-east-2"

# Initial structure and defaults
subnet_dict = collections.defaultdict(dict)
subnet_dict['Mappings'] = collections.defaultdict(dict)

regions = ['us-east-1', 'us-east-2', 'us-west-2']

# NU LOOP
for region_nm in regions:

    # Initial setup
    session = boto3.Session(profile_name=profile_nm, region_name=region_nm)

    # Initiate the session
    ec2 = session.client('ec2')

    # Get all AMIs
    all_amis = ec2.describe_images(
        Owners=[
            'self',
        ]
    )

 
    count = 0
    for image in all_amis['Images']:
        print(image['CreationDate'])
        count += 1

    print(count)

