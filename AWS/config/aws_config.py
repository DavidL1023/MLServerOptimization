import boto3
import json
import os
from dotenv import load_dotenv

# Be sure to have a .env file with
"""
access_key_id=your_key
secret_access_key=your_secret
"""
load_dotenv()

# Load configuration from config.json
dir_path = os.path.dirname(os.path.realpath(__file__))

# Path to config.json
config_path = os.path.join(dir_path, 'config.json')

# Load configuration from config.json
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

AWS_CONFIG = config['aws']
EC2_CONFIG = config['ec2']
MONITORING_CONFIG = config['monitoring']

INSTANCE_IDS = EC2_CONFIG['instance_ids']
PERIOD = MONITORING_CONFIG['period']
STATISTICS = MONITORING_CONFIG['statistics']

# Initialize a session using Boto3 with values from the config file
session = boto3.Session(
    aws_access_key_id=os.getenv('access_key_id'),
    aws_secret_access_key=os.getenv('secret_access_key'),
    region_name=AWS_CONFIG['region_name']
)

# Create EC2 and CloudWatch clients
ec2 = session.client('ec2')
cloudwatch = session.client('cloudwatch')
