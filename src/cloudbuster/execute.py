def execute(profile, region, build_file, stack_name):
    with open('execute.sh', 'w') as f:
        f.write("#!/bin/bash")
        f.write(f"\nexport AWS_PROFILE={profile}")
        f.write(f"\naws cloudformation create-stack ")
        f.write(f"--region {region} ")
        f.write(f"--template-body file://{build_file} ")
        f.write(f"--stack-name {stack_name}")
