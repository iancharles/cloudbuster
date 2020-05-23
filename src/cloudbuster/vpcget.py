import boto3
import sys

def get_vpc(profile, region):
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.client('ec2')
    vpcs = ec2.describe_vpcs()
    available_vpcs = {}
    
    for vpc in vpcs['Vpcs']:
        vpc_tags = ec2.describe_tags(
            Filters=[
                {
                    'Name': 'resource-id',
                    'Values': [
                        vpc['VpcId'],
                    ]
                },
                {
                    'Name': 'key',
                    'Values': [
                        'Name',
                    ]
                }
            ]    
        )
        

        for tag in vpc_tags["Tags"]:
            # print(tag["Value"])
            available_vpcs[vpc['VpcId']] = tag["Value"]

    print("\nVPC")
    print("===")
    print("VPC is REQUIRED to proceed. Please choose from one below,")
    print("or hit Q to exit Cloudbuster\n")


    counter = 0
    displayed_vpcs = []
    for key, value in available_vpcs.items():
        print (f"{counter} - {key} : {value}")
        displayed_vpcs.append(key)
        counter += 1

    try:
        choice = int(input("\nEnter the number of the VPC to select: "))
        if choice in range(0,counter):
            return displayed_vpcs[int(choice)]
        else:
            print("Invalid choice\nExiting now...")
            sys.exit(1)
    except ValueError:
        print("Please enter a valid number.\nExiting now...")
        sys.exit(1)
    except IndexError:
        print("That number is out of range")
        sys.exit(1)


    
