import boto3



def sanitize_vpc(profile, vpc_nm, regions):
    for region in regions:
        session = boto3.Session(profile_name=profile, region_name=region)
        ec2 = session.client('ec2')
        return_region = ""
        vpcs = ec2.describe_vpcs(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_nm,
                    ]
                },
            ]
        )
        
        for vpc in vpcs['Vpcs']:
            if vpc_nm in vpc['VpcId']:
                return_region = True
                return vpc_nm

        if not return_region:
            tags = ec2.describe_tags(
                Filters=[
                    {
                        'Name': 'resource-type',
                        'Values': [
                            'vpc',
                        ]
                    },
                    {
                        'Name': 'tag:Name',
                        'Values': [
                            vpc_nm,
                        ]
                    }
                ]
            )

            for tag in tags['Tags']:
                if vpc_nm in tag['Value']:
                    return tag['ResourceId']