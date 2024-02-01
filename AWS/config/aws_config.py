import boto3
import json

# Load configuration from config.json
with open('config\config.json', 'r') as config_file:
    config = json.load(config_file)

AWS_CONFIG = config['aws']
EC2_CONFIG = config['ec2']
MONITORING_CONFIG = config['monitoring']

INSTANCE_IDS = EC2_CONFIG['instance_ids']
PERIOD = MONITORING_CONFIG['period']
STATISTICS = MONITORING_CONFIG['statistics']

# Initialize a session using Boto3 with values from the config file
session = boto3.Session(
    aws_access_key_id=AWS_CONFIG['access_key_id'],
    aws_secret_access_key=AWS_CONFIG['secret_access_key'],
    region_name=AWS_CONFIG['region_name']
)

# Create EC2 and CloudWatch clients
ec2 = session.client('ec2')
cloudwatch = session.client('cloudwatch')
