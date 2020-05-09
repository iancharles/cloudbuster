import boto3
import collections
# import argparse


# Temp variables, replace with logic
profile_nm = "default"
region_nm = "us-east-2"

# temp variable, replace with argarse later
vpc = "vpc-06db524c77128c292"

session = boto3.Session(profile_name=profile_nm, region_name=region_nm)
ec2 = session.client('ec2')

zones_raw = ec2.describe_availability_zones()

print(zones_raw)



# # Initial structure and defaults
# subnet_dict = collections.defaultdict(dict)
# subnet_dict['Mappings'] = collections.defaultdict(dict)
# subnet_dict['Mappings']['SubnetMap'] = collections.defaultdict(dict)

# regions = ['us-east-1', 'us-east-2', 'us-west-2']

# # NU LOOP
# for region_nm in regions:

#     # Initial setup
#     session = boto3.Session(profile_name=profile_nm, region_name=region_nm)

#     # Initiate the session
#     ec2 = session.client('ec2')

#     # Get public subnets
#     public_subnets = ec2.describe_subnets(
#         Filters=[
#             {
#                 'Name': 'tag:Name',
#                 'Values': [
#                     '*ublic*'
#                 ]
#             }
#         ]
#     )





#     # # print("Public Subnets")
#     # for subnet in public_subnets['Subnets']:
#     #     subnet_dict['Mappings']['SubnetMap'][subnet['AvailabilityZone']]["Public"] = subnet['SubnetId']

#     # Get private subnets
#     private_subnets = ec2.describe_subnets(
#         Filters=[
#             {
#                 'Name': 'tag:Name',
#                 'Values': [
#                     '*rivate*'
#                 ]
#             }
#         ]
#     )

#     # # print("Private Subnets")
#     # for subnet in private_subnets['Subnets']:
#     #     subnet_dict['Mappings']['SubnetMap'][subnet['AvailabilityZone']]["Private"] = subnet['SubnetId']



# # The final printer
# for key in subnet_dict:
#     print(f"{key}:")
#     for key_two in subnet_dict[key]:
#         print(f"  {key_two}:")
#         for key_three in subnet_dict[key][key_two]:
#             print(f"    {key_three}:")
#             for key_four in subnet_dict[key][key_two][key_three]:
#                 print(f"      {key_four}: {subnet_dict[key][key_two][key_three][key_four]}")