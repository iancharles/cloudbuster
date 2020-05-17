###############
# CLOUDBUSTER #
###############

import boto3
import argparse
import sys
import datetime
import os


from amiget import get_amimap
from iam_role_get import get_iam_role
from keypairget import get_key_pairs
from regionget import get_region
from size_get import get_sizes
from subnetget import get_subnets
from sg_get import get_sgs
from userdata import add_user_data
from vpcget import get_vpc
from vpc_sanitize import sanitize_vpc


# ADD ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--vpc', help="VPC (VPC-id or friendly name)")
parser.add_argument('-o','--os', help="operating system")
parser.add_argument('-t','--type', help="instance type (size)")
parser.add_argument('-z','--zone', help="availability zone")
parser.add_argument('--hostname', help='name of instance')
parser.add_argument('-k', '--key', help='name of keypair')
parser.add_argument('--role', help='instance iam role')
parser.add_argument('--region', help='region of build')
parser.add_argument('--profile', help="AWS CLI Profile")
parser.add_argument('--network', help="Public or Private subnet")
parser.add_argument('--timezone', help='Timezone of instance')
parser.add_argument('--user', help='default user on instance')
parser.add_argument('-d', '--disks', nargs='+', help='add data volumes', default=None)
parser.add_argument('--sgs', nargs='+', help='add security groups', default=None)
args = parser.parse_args()

value_dict = {}
skipped_opts = {}
skipped_req = {}

allowed_os = [
    'ubuntu16', 'ubuntu18', 'amazonlinux2', 'rhel7', 'centos7'
    ]
linux_os = [
    'ubuntu16', 'ubuntu18', 'amazonlinux2', 'rhel7', 'centos7'
    ]
allowed_regions = ['us-east-1', 'us-east-2', 'us-west-2']

source_file = "ec2.yml"
build_file = '{:%Y-%m-%d-%H:%M}'.format(datetime.datetime.now()) + ".yml"

if args.profile:
    profile = args.profile
elif 'AWS_PROFILE' in os.environ:
    profile = os.environ['AWS_PROFILE']
else:
    print("\nProfile is required")
    print("\nTo set profile in BASH environment variable")
    print("(Profile must already be configured in ~/.aws/config):")
    print("$ export AWS_PROFILE=myprofile")
    print("\nTo set profile using flag in cloudbuster:")
    print("Add  '--profile myprofile' to your cloudbuster command\n")
    sys.exit(1)

# GET VPC and REGION - REQUIRED!
if args.region:
    region = args.region
    if args.vpc:
        vpc = sanitize_vpc(profile, args.vpc, [region])
    else:
        vpc = get_vpc(profile, region)
else:
    if args.vpc:
        vpc = sanitize_vpc(profile, args.vpc, allowed_regions)
        region = get_region(profile, args.vpc, allowed_regions)
    else:
        print("VPC or Region is required for all builds.")
        print("Exiting...")
        sys.exit(1)

value_dict["VAR_REGION"] = region


# USER GEN - REQUIRED

# Instance type
if args.type:
    value_dict["VAR_INSTANCE_TYPE"] = args.type
else:
    print("\nInstance type is required.")
    # TO DO: Add instance type generator
    # print("You can choose to see a list of types before entering a value.")
    # size_choices = get_sizes(profile, region)
    # if input("See available types first? [y/N] ").lower() == "y":
        # print(size_choices)
    selection = input("\nEnter instance type (size): ")
    value_dict["VAR_INSTANCE_TYPE"] = selection
    # if selection in size_choices:
    #     value_dict["VAR_INSTANCE_TYPE"] = selection
    # else:
    #     print("That was not a valid choice. Exiting...")
    #     sys.exit(1)

    

# Default system user - maybe only necessary for linux
if args.user:
    value_dict["VAR_USER"] = args.user
elif not args.os or args.os and args.os not in linux_os:
    pass
else:
    skipped_req["user"] = "No Default"

# key pair
if args.key:
    value_dict["VAR_KEYNAME"] = args.key
else:
    key = get_key_pairs(profile, region)
    if key:
        value_dict["VAR_KEYNAME"] = key
    else:
        value_dict["VAR_KEYNAME"] = ""
        skipped_req["keypair"] = "None"

# Output missing required values to user
if skipped_req:
    print("\nYou forgot the following mandatory parameters:\n")
    print(skipped_req)
    sys.exit(1)


# GET AUTOMATIC VALUES

value_dict["# VAR_AMI_MAP"] = get_amimap(profile, region)

value_dict["# VAR_SUBNET_MAP"] = get_subnets(profile, allowed_regions)



# USER GEN OR PROMPTED
if args.sgs:
    sgs_fmt = ""
    for group in args.sgs:
        sgs_fmt += "\n        - " + group
    value_dict["VAR_SECURITY_GROUPS"] = sgs_fmt
else:
    value_dict["VAR_SECURITY_GROUPS"] = get_sgs(vpc, region, profile)


# USER GEN - OPTIONAL

if args.hostname:
    hn = args.hostname
else:
    hn = "Cloudbuster Host 1"
    skipped_opts["hostname"] = hn

value_dict["VAR_HOSTNAME"] = hn


if args.timezone:
    # value_dict["# timedatectl"] = "timedatectl"
    tz = args.timezone
else:
    tz = "UTC"
    skipped_opts["timezone"] = tz

value_dict["VAR_TIMEZONE"] = tz

# If network type is entered, use it. Else, create as parameter
if args.network and args.network.lower() == 'public':
    value_dict["VAR_NETWORK"] = "Public"
else:
    value_dict["VAR_NETWORK"] = "Private"

# If role is entered, use it. Else, create as parameter
if args.role:
    value_dict["VAR_ROLE"] = args.role
else:
    value_dict["VAR_ROLE"] = get_iam_role(profile, region)
if not value_dict["VAR_ROLE"]:
    role_params = "IamInstanceProfile:"
    role_params += "\n    Type: String"
    role_params += "\n    Default: EC2-S3-Access"

    value_dict["# VAR_PARAM_ROLE"] = role_params
    value_dict["VAR_ROLE"] = "!Ref IamInstanceProfile"
    # skipped_opts["role"] = "EC2-S3-Access"

# If OS is entered, use it. Else, create as parameter
if args.os in allowed_os:
    value_dict["VAR_OS"] = args.os
else:
    print("\nSkipping the os parameter prevents you from entering user data")
    print("This means you will be limited to using Windows instances with")
    print("any template created.")
    os_params = "OS:"
    os_params += "\n    Type: String"
    os_params += "\n    AllowedValues:"
    for os in allowed_os:
        if os not in linux_os:
            os_params += "\n      - " + os

    value_dict["# VAR_PARAM_OS"] = os_params
    value_dict["VAR_OS"] = "!Ref OS"

# Write user_data
if args.os and args.os in linux_os:
    value_dict["# VAR_UD"] = add_user_data(
        args.os, hn, tz, args.user)

# If disks are entered, add them. Else, ignore
if args.disks:
    disks = args.disks
    block_device_pool = ['/dev/xvdb', '/dev/xvdc', '/dev/xvdd', \
        '/dev/xvde', '/dev/xvdf', '/dev/xvdg', '/dev/xvdh' ]
    counter = 0
    disk_params = ""

    for disk in disks:
        disk_params += "        - DeviceName: " + block_device_pool[counter] + "\n"
        disk_params += "          Ebs:" + "\n"
        disk_params += "            VolumeSize: " + disk + "\n"
        disk_params += "            Encrypted: true"
        counter += 1
        if counter < len(disks):
            disk_params += "\n"
            
    value_dict["# VAR_PARAM_DISKS"] = disk_params
else:
    skipped_opts["Disks"] = "None"




## CHECK VALUES


if skipped_opts:
    print("You skipped the following optional parameters.")
    print("They are not required, but please confirm you did not \
omit them by accident")
    print("Default values shown when available")
    print("\n")
    for key, value in skipped_opts.items():
        print(f"{key}: {value}")
    print("\n#-------------#\n")



# print(value_dict)


with open(source_file, 'r') as f:
    build = f.read()
    for key, value in value_dict.items():
        build = build.replace(key, value)
    
with open(build_file, 'w') as f:
    f.write(build)

print(f"Your Cloudbuster CFT File is now available at {build_file}\n")