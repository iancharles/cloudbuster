import boto3
import collections
# from datetime import datetime
import datetime
from dateutil import parser


# Temp variables, replace with logic
# profile_nm = "default"
# region_nm = "us-east-2"

def get_amimap(profile_nm, region_nm):

    # Initial structure and defaults
    subnet_dict = collections.defaultdict(dict)
    subnet_dict['Mappings'] = collections.defaultdict(dict)
    subnet_dict['Mappings']['AMIMap'] = collections.defaultdict(dict)

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

    # Format dates and order main dict by date
    for image in all_amis['Images']:
        image['CreationDate'] = image['CreationDate'][:19]
        # image['CreationDate'] = datetime.datetime.strptime(image['CreationDate'], "%Y-%m-%dT%H:%M:%S")

    all_amis['Images'].sort(key= lambda image: datetime.datetime.strptime(image['CreationDate'], "%Y-%m-%dT%H:%M:%S"))

    count = 0

    # Create empty OS dicts
    ubuntu16_amis = [""]
    ubuntu18_amis = [""]
    amazonlinux2_amis = [""]

    # Sort images into dicts by OS
    for image in all_amis['Images']:
        if 'ubuntu' in image['Name'].lower() and '16' in image['Name'].lower():
            ubuntu16_amis.append(image)
        elif 'ubuntu' in image['Name'].lower() and '18' in image['Name'].lower():
            ubuntu18_amis.append(image)
        elif 'amazon' in image['Name'].lower() and '-2-' in image['Name'].lower():
            amazonlinux2_amis.append(image)    

    ubuntu16 = ubuntu16_amis[-1]
    ubuntu18 = ubuntu18_amis[-1]
    amazonlinux2 = amazonlinux2_amis[-1]

    # print(ubuntu16_amis)
    # print(ubuntu18_amis)
    # print(amazonlinux2_amis)

    try:
        # print(f"{ubuntu16['Name']} - {ubuntu16['ImageId']} - {ubuntu16['CreationDate']}")
        subnet_dict['Mappings']['AMIMap'][region_nm]['ubuntu16'] = ubuntu16['ImageId']
    except:
        pass

    try:
        # print(f"{ubuntu18['Name']} - {ubuntu18['ImageId']} - {ubuntu18['CreationDate']}")
        subnet_dict['Mappings']['AMIMap'][region_nm]['ubuntu18'] = ubuntu18['ImageId']
    except:
        pass
    try:
        # print(f"{amazonlinux2['Name']} - {amazonlinux2['ImageId']} - {amazonlinux2['CreationDate']}")
        subnet_dict['Mappings']['AMIMap'][region_nm]['amazonlinux2'] = amazonlinux2['ImageId']
    except:
        pass


    ami_map = ""
    for key in subnet_dict:
        # ami_map += (key + ":")
        for key_two in subnet_dict[key]:
            ami_map += ("  " + key_two + ":")
            for key_three in subnet_dict[key][key_two]:
                ami_map += ("\n    " + key_three + ":")
                for key_four in subnet_dict[key][key_two][key_three]:
                    ami_map += ("\n      " + key_four + ": " + subnet_dict[key][key_two][key_three][key_four])

    return ami_map
