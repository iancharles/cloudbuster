import boto3

def get_key_pairs(profile, region):
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.client('ec2')
    keypairs = ec2.describe_key_pairs()
    counter = 1
    print("\nKEY PAIR")
    print("========")
    print("Key pair is required for all instances")
    print("\nAvailable Key Pairs:")
    for key in keypairs['KeyPairs']:
        print(f"{counter} - {key['KeyName']}")
        counter += 1

    try:
        index = int(input("\nChoose a keypair: ")) -1
        if -1 < index < counter:
            return keypairs['KeyPairs'][index]['KeyName']
            # print(keypairs['KeyPairs'][index]['KeyName'])
    except:
        return None

