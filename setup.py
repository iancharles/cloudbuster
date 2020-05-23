from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='cloudbuster',
    version='0.1.0',
    description='A CLI tool to generate CFT',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Ian M',
    author_email='ian@telem.us',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['boto3'],
    entry_points={
        'console_scripts': [
            'cloudbuster=cloudbuster.ec2:main',
        ],
    }
)
