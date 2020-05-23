import boto3
import sys

def get_iam_role(profile, region):
    session = boto3.Session(profile_name=profile, region_name=region)
    iam = session.client('iam')

    available_instance_profiles = []
    all_instance_profiles = iam.list_instance_profiles()
    for instance_profile in all_instance_profiles['InstanceProfiles']:
        available_instance_profiles.append(instance_profile['InstanceProfileName'])
        default_profile_name = "CloudBuster-InstanceProfile"
        if instance_profile['InstanceProfileName'] == default_profile_name:
            print(f"\nDefault instance profile found. \nWould you like to use {default_profile_name}?\n")
            if input("Hit Y to see other profiles, or any key to use default: ").lower() != 'y':
                # print(default_profile_name)
                return default_profile_name


    counter = 1
    print("\nIAM INSTANCE ROLE")
    print("=================")
    print("Also called Instance Profiles")
    print("\nAvailable Instance Roles:\n")
    for role in available_instance_profiles:
        print(f"{counter} - {role}")
        counter += 1
    
    try:
        index = int(input("\nChoose an Instance Profile (IAM Instance Role): ")) -1
        if -1 < index < counter:
            # print(available_instance_profiles[index])
            return available_instance_profiles[index]
            
    except:
        print("\n##########\nWARNING!!!\n##########")
        print("That is not a valid profile/role")
        print("You will be required to enter a profile as a parameter in CF\n")
            
        
        

        
    # available_iam_roles = []
    # all_iam_roles = iam.list_roles()
    # for role in all_iam_roles['Roles']:
    #     # print(role['RoleName'])
    #     for statement in role['AssumeRolePolicyDocument']['Statement']:
    #         # print(statement['Principal'])
    #         # print(statement['Principal']['Service'])
    #         for service in statement['Principal']:
    #             # print(statement['Principal']['Service'])
    #             if 'ec2' in statement['Principal']['Service']:
    #                 available_iam_roles.append(role['RoleName'])
    #                 available_iam_roles.append(role['RoleName'])

    # print(available_iam_roles)
    


# get_iam_role('default', 'us-west-2')