# CLOUDBUSTER
### An interactive tool for creating Cloudformation Templates

## Prerequisites
- Python 3.7 needs to be installed (it does not need to be your default Python install)
    - If you are using Windows, WSL (Windows Subsystem on Linux) is highly recommended. You still may need to install 3.7 alongside the system defaults, but 3.7 is available in the main repos of most Linux distributions. 
    - If you are using a Mac, there are many methods for installing Python 3, but many people like using homebrew. The incomparable Yousef Eledra has writen a Medium article on it.
    - If you are using Linux and the system default for Python 3 is not 3.7, use your system's native package manager to find and install ```python37```
- AWS CLI needs to be installed and configured.
    - Either version (1 or 2) should be fine
    - Profiles need to be set up in ~/.aws/config
- Pipenv (or your preferred method of isolation) is required for Cloudbuster v 0.1.0

## Installing Cloudbuster
First, download or clone this project. Navigate to the main folder.
Create a virtualenv for this project by running the following command in the main folder:
    
    $ pipenv install -e .

After the virtualenv is created, activate it by running:
    
    $ pipenv shell

As long as this virtualenv is active, you can safely use the ```cloudbuster``` command.

## Usage
Cloudbuster is versitile. You will need to provide a CLI profile and either a VPC or Region, but after that it is very flexible. The more information you give it upfront, the less it will prompt you.

### Example

    $ cloudbuster --profile moon-company --os ubuntu18 --vpc moon-east-vpc --hostname moonlander-server-1 --user moon-admin --timezone America/Chicago

### Environment Variable
When using the AWS CLI, a common way to set the preferred account profile is by temporarily setting it as an environment variable. This is compatible with Cloudbuster as well. To set a profile (profile must already exist in ~/.aws/config):

    $ export AWS_PROFILE=myprofile

### Parameter Files
If you have access to a customer_data file, you can pre-populate some values that are helpful while building Linux instances

    $ cloudbuster --populate /path/to/data/file.sls

You may want to consider cloning some gitlab projects and setting up an easily-accessible directory.

There are future plans for support for more types of files.

### CLI Parameters
The most common way of entering parameters is by adding command line flags.
Cloudbuster supports a large selection of parameters:
- ```-v, --vpc``` Either VPC or Region is required
- ```-r, --region``` See above
- ```--profile``` Must be entered either as flag or as environment variable
- ```-o, --os``` Operating System
- ```-t, --type``` Instance type (size)
- ```-k, --key``` Keypair for instance
- ```-r, --role``` IAM instance role
- ```--sgs``` Security Groups. Can be between 1 and 5 arguments


OPTIONAL
- ```-z, --zone``` Availability Zone. If not provided, one will be selected for you
- ```-d, --disks``` Additional EBS (data) volumes. A root block device is always included and does not need to be specified
- ```--root``` Default root volume size is 64 GB. Specify a value for --root-vol to override this
- ```--network``` If not provided, the network will default to Private
- ```--timezone``` If not provided, the timezone will default to UTC

### One-Touch Execute
Cloudbuster now offers the option to immediately execute your new template. After generating the template, simply run "./execute.sh" to create the stack. This file will be overwritten every time you run Cloudbuster. The first time you run Cloudbuster, you will need to make the execute.sh file executable with ```chmod +x execute.sh```.

### Prompts
If a parameter is not entered through any of the methods above, you may be prompted for it. While Cloudbuster attempts to be comprehensive, some missing values may not generate prompts, so try and front-load Cloudbuster with whatever values you do have available. As a last resort, some values may finally be either set as defaults, or become Parameters in the resulting CloudForamtion template. Due to dependencies, if you do not enter a value for *os*, you will only be able to create Windows instances through the template.
