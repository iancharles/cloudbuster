import os
import sys

def get_profile():
    try:
        home = os.environ["HOME"]

        options = []
        with open(f"{home}/.aws/config", 'r') as f:
            profile_items = f.readlines()
            for item in profile_items:
                # print(item)
                if item[0] == '[':
                    item = item.replace("[", "")
                    item = item.replace("]", "")
                    item = item.replace("\n", "")
                    item = item.replace("profile ", "")
                    options.append(item)

        counter = 1
        print("\nCLI PROFILE")
        print("===========")
        print("CLI profile is required.")
        print("This is configured in '~/.aws/config'")
        print('and is not to be confused with the instance IAM profile')
        print("\nAvailable Profiles:")
        for profile in options:
            print(f"{counter} - {profile}")
            counter += 1

        try:
            index = int(input("\nChoose a profile: ")) -1
            if -1 < index < counter:
                return options[index]
        except:
            print("\nProfile is required")
            print("\nTo set profile in BASH environment variable")
            print("(Profile must already be configured in ~/.aws/config):")
            print("$ export AWS_PROFILE=myprofile")
            print("\nTo set profile using flag in cloudbuster:")
            print("Add  '--profile myprofile' to your cloudbuster command\n")
            sys.exit(1)
    except:
        print("\nProfile is required")
        print("\nTo set profile in BASH environment variable")
        print("(Profile must already be configured in ~/.aws/config):")
        print("$ export AWS_PROFILE=myprofile")
        print("\nTo set profile using flag in cloudbuster:")
        print("Add  '--profile myprofile' to your cloudbuster command\n")
        sys.exit(1)