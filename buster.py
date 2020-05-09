import boto3
import argparse
from regionget import get_region
# import sys
# from subnetget import get_subnets
# from amiget import get_amis
# from sg_get import get_sgs
# from add_block_device import add_block_device
# from userdata_get import get_userdata

# ADD ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--region', help="region of VPC")
parser.add_argument('-v', '--vpc', help="VPC to get vars")
parser.add_argument('-o','--os', help="operating system")
parser.add_argument('-t','--type', help="instance type (size)")
parser.add_argument('-z','--zone', help="availability zone")
parser.add_argument('--hostname', help='name of instance')
parser.add_argument('--keyname', help='name of keypair')
parser.add_argument('--role', help='instance iam role')
parser.add_argument('--profile', help="AWS CLI Profile")
parser.add_argument('--network', help="Public or Private subnet")
parser.add_argument('--timezone', help='Timezone of instance')
parser.add_argument('--user', help='default user on instance')
parser.add_argument('-d', '--disks', nargs='+', help='add data volumes')
args = parser.parse_args()

value_dict = {}

disks = args.disks

allowed_os = ['ubuntu16', 'ubuntu18', 'suse']

source_file = "stacks/000004.yml"
build_file = "stacks/000005.yml"

# vpc = "vpc-06db524c77128c292"
vpc = args.vpc
profile = "default"

if args.region:
    region = args.region
else:
    region = get_region(profile, vpc)
value_dict["VAR_REGION"] = region

print(region)
# VALIDATE ARGUMENTS


if args.type:
    value_dict["VAR_INSTANCE_TYPE"] = args.type

if args.hostname:
    value_dict["VAR_HOSTNAME"] = args.hostname

if args.keyname:
    value_dict["VAR_KEYNAME"] = args.keyname

if args.timezone:
    value_dict["# timedatectl"] = "timedatectl"
    value_dict["VAR_TIMEZONE"] = args.timezone

if args.user:
    value_dict["VAR_USER"] = args.user

if args.region:
    value_dict["VAR_REGION"] = args.region

# If OS is entered, use it. Else, create as parameter
if args.os in allowed_os:
    value_dict["VAR_OS"] = args.os
else:
    os_params = "OS:"
    os_params += "\n    Type: String"
    os_params += "\n    AllowedValues:"
    for os in allowed_os:
        os_params += "\n      - " + os

    value_dict["# VAR_PARAM_OS"] = os_params
    value_dict["VAR_OS"] = "!Ref OS"

print(value_dict)


with open(source_file, 'r') as f:
    build = f.read()
    for key, value in value_dict.items():
        build = build.replace(key, value)
    
with open(build_file, 'w') as f:
    f.write(build)
