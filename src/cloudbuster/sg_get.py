import boto3
import collections
from json import dumps

def get_sgs(vpc, region_nm, profile_nm):

    session = boto3.Session(profile_name=profile_nm, region_name=region_nm)
    ec2 = session.client('ec2')

    available_sgs = ec2.describe_security_groups(
        Filters=[
            {
                'Name': 'vpc-id',
                'Values': [
                    vpc
                ]
            }
        ]
    )


    # # Initial structure and defaults
    subnet_dict = collections.defaultdict(dict)
    subnet_dict['SecurityGroups'] = collections.defaultdict(dict)
    
    selected_security_groups = []
    counter = 0
    print("\nSECURITY GROUPS")
    print("===============")
    print("You must choose at least 1 security group. You can choose up to 5.")
    display = input("\nWould you like to see the available security groups first? [y/N] ").lower()
    if display == 'y':
        print(f"\nAvailable Security Groups for {vpc}:\n")
        for item in available_sgs['SecurityGroups']:
            print(f"{item['GroupName']} - {item['Description']}")
        print("\n#-------------#\n")
    print("Choose from Available Security Groups:\n")
    for item in available_sgs['SecurityGroups']:
        if input(f"{item['GroupName']} - {item['Description']} [y/N]: ").lower() == 'y':
            selected_security_groups.append(item["GroupId"])
    
    print("\n#-------------#\n")
    # security_groups = dumps(selected_security_groups)

    sg_output = ""

    for group in selected_security_groups:
        sg_output += "\n        - " + group

    return sg_output