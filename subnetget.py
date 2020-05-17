import boto3
import collections


# Initial structure and defaults
subnet_dict = collections.defaultdict(dict)
subnet_dict['Mappings'] = collections.defaultdict(dict)
subnet_dict['Mappings']['SubnetMap'] = collections.defaultdict(dict)

# regions = ['us-east-1', 'us-east-2', 'us-west-2']

# NU LOOP
def get_subnets(profile_nm, allowed_regions):
    for region_nm in allowed_regions:

        # Initial setup
        session = boto3.Session(profile_name=profile_nm, region_name=region_nm)

        # Initiate the session
        ec2 = session.client('ec2')

        # Get public subnets
        public_subnets = ec2.describe_subnets(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        '*ublic*'
                    ]
                }
            ]
        )





        # print("Public Subnets")
        for subnet in public_subnets['Subnets']:
            subnet_dict['Mappings']['SubnetMap'][subnet['AvailabilityZone']]["Public"] = subnet['SubnetId']

        # Get private subnets
        private_subnets = ec2.describe_subnets(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        '*rivate*'
                    ]
                }
            ]
        )

        # print("Private Subnets")
        for subnet in private_subnets['Subnets']:
            subnet_dict['Mappings']['SubnetMap'][subnet['AvailabilityZone']]["Private"] = subnet['SubnetId']



    # The final printer
    subnet_map = ""
    for key in subnet_dict:
        for key_two in subnet_dict[key]:
            subnet_map += ("  " + key_two + ":")
            for key_three in subnet_dict[key][key_two]:
                subnet_map += ("\n    " + key_three + ":")
                for key_four in subnet_dict[key][key_two][key_three]:
                    subnet_map += ("\n      " + key_four + ": " + subnet_dict[key][key_two][key_three][key_four])

    return subnet_map