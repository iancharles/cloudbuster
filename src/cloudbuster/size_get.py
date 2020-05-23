import boto3

def get_sizes(profile, region):
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.client('ec2')
    # paginator = ec2.get_paginator('describe_instance_types')
    instance_types = ec2.describe_instance_types(
        Filters=[
            {
                'Name': 'ebs-info.encryption-support',
                'Values': [
                    'supported',
                ]
            },
        ],
    )
    # response_iterator = paginator.paginate(
    #     Filters=[
    #         {
    #             'Name': 'ebs-info.encryption-support',
    #             'Values': [
    #                 'supported',
    #             ]
    #         },
    #     ],
    #     PaginationConfig={
    #         'MaxItems': 123,
    #         'PageSize': 123,
    #         'StartingToken': 'string'
    #     }
    # )
    

    sizes = []
    avail_types =  instance_types['InstanceTypes']
    for type in avail_types:
        sizes.append(type['InstanceType'])

    # return(sorted(sizes))
    print(len(sorted(sizes)))

# get_sizes('default', 'us-east-2')