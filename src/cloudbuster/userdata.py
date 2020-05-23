import boto3


def add_user_data(os, hostname, timezone, user):
    value_dict = {
        "VAR_HOSTNAME": hostname,
        "VAR_TIMEZONE": timezone,
        "VAR_USER": user
    }
    
    userdata = """      UserData: !Base64 |
        #!/bin/bash -ex
        hostnamectl set-hostname "VAR_HOSTNAME" 
        # timedatectl set-timezone VAR_TIMEZONE
        adduser "VAR_USER"
        cp -R /home/VAR_DEFAULT/.ssh /home/VAR_USER/.ssh
        chown -R VAR_USER: /home/VAR_USER/
        echo "VAR_USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/VAR_USER
        chage -I -1 -m 0 -M 99999 -E -1 VAR_USER
        echo "VAR_HOSTNAME" > /home/VAR_USER/hostname.txt
        echo "VAR_TIMEZONE" > /home/VAR_USER/timezone.txt
        echo "VAR_USER" > /home/VAR_USER/user.txt
        reboot now
        """
    
    user_dict = {
        "amazonlinux2": "ec2-user",
        "centos7": "centos",
        "rhel7": "ec2-user",
        "ubuntu16": "ubuntu",
        "ubuntu18": "ubuntu"
    }

    userdata = userdata.replace("VAR_DEFAULT", user_dict[os])

    if timezone != "UTC":
        userdata = userdata.replace("# timedatectl", "timedatectl")

    for key, value in value_dict.items():
        userdata = userdata.replace(key, value)
    # print(userdata)
    return userdata

# add_user_data("ubuntu18", "cb-instance-1", "America/Los_Angeles", "nv-admin")