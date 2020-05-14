###############
# CLOUDBUSTER #
###############


import boto3
import argparse
from regionget import get_region
from amiget import get_amimap
import sys
from subnetget import get_subnets
from sg_get import get_sgs
from vpcget import get_vpc
from vpc_sanitize import sanitize_vpc
# from add_block_device import add_block_device
# from userdata_get import get_userdata

# ADD ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--vpc', help="VPC to get vars")
parser.add_argument('-o','--os', help="operating system")
parser.add_argument('-t','--type', help="instance type (size)")
parser.add_argument('-z','--zone', help="availability zone")
parser.add_argument('--hostname', help='name of instance')
parser.add_argument('--keyname', help='name of keypair')
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

allowed_os = ['ubuntu16', 'ubuntu18', 'suse']
allowed_regions = ['us-east-1', 'us-east-2', 'us-west-2']

source_file = "stacks/000004.yml"
build_file = "stacks/000005.yml"

profile = "default"

# GET VPC and REGION - REQUIRED!
if args.region:
    region = args.region
    if args.vpc:
        vpc = sanitize_vpc(profile, args.vpc, [region])
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

if args.type:
    value_dict["VAR_INSTANCE_TYPE"] = args.type
else:
    skipped_req["type"] = "No default"

if args.user:
    value_dict["VAR_USER"] = args.user
else:
    skipped_req["user"] = "No Default"

if skipped_req:
    print("You forgot the following mandatory parameters:")
    for key, value in skipped_req.items():
        print(f"{key}: {value}")
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
    value_dict["VAR_HOSTNAME"] = args.hostname
else:
    value_dict["VAR_HOSTNAME"] = "Cloud Host 1"
    skipped_opts["hostname"] = value_dict["VAR_HOSTNAME"]

if args.keyname:
    value_dict["VAR_KEYNAME"] = args.keyname
#add in logic to look for default values
else:
    skipped_opts["keyname"] = "None"


if args.timezone:
    value_dict["# timedatectl"] = "timedatectl"
    value_dict["VAR_TIMEZONE"] = args.timezone
else:
    skipped_opts["timezone"] = "UTC"


# If network type is entered, use it. Else, create as parameter
if args.network and args.network.lower() == 'public':
    value_dict["VAR_NETWORK"] = "Public"
elif args.network:
    value_dict["VAR_NETWORK"] = "Private"
else:
    network_params = "SubnetType:"
    network_params += "\n    Type: String\n    AllowedValues:"
    network_params += "\n       - Private\n       - Public"
    network_params += "\n    Default: Private"

    value_dict["# VAR_PARAM_NETWORK"] = network_params
    value_dict["VAR_NETWORK"] = "!Ref SubnetType"
    skipped_opts["network"] = "Private"

# If role is entered, use it. Else, create as parameter
if args.role:
    value_dict["VAR_ROLE"] = args.role
else:
    role_params = "IamInstanceProfile:"
    role_params += "\n    Type: String"
    role_params += "\n    Default: EC2-S3-Access"

    value_dict["# VAR_PARAM_ROLE"] = role_params
    value_dict["VAR_ROLE"] = "!Ref IamInstanceProfile"
    skipped_opts["role"] = "EC2-S3-Access"

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
    skipped_opts["OS // Allowed Values:"] = allowed_os


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
    print("\n#-------------#\n")
    for key, value in skipped_opts.items():
        print(f"{key}: {value}")

# print(value_dict)


with open(source_file, 'r') as f:
    build = f.read()
    for key, value in value_dict.items():
        build = build.replace(key, value)
    
with open(build_file, 'w') as f:
    f.write(build)
