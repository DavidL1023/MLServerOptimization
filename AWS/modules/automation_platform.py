""" Provides functions to modify EC2 server states """

import resource_util as resource_util

import config.aws_config as aws_config
from datetime import datetime, timedelta, timezone

# Grab EC2 and CloudWatch clients
ec2 = aws_config.ec2
cloudwatch = aws_config.cloudwatch


def check_instance_status(instance_id):
    """
    Checks the status of a specified EC2 instance.

    Args:
        instance_id (str): The identifier of the EC2 instance.

    Returns:
        str: The current status of the instance ('running', 'stopped', etc.).
    """
    response = ec2.describe_instance_status(InstanceIds=[instance_id])
    instance_statuses = response.get('InstanceStatuses', [])

    if not instance_statuses:
        return "No information available"

    instance_status = instance_statuses[0]
    return instance_status.get('InstanceState', {}).get('Name', 'Unknown')


def start_instance(instance_id):
    """
    Starts a specified EC2 instance.

    Args:
        instance_id (str): The identifier of the EC2 instance to start.

    Returns:
        str: The response from the start instance request.
    """
    try:
        response = ec2.start_instances(InstanceIds=[instance_id])
        return response
    except Exception as e:
        return f"Error starting instance: {str(e)}"


def stop_instance(instance_id):
    """
    Stops a specified EC2 instance.

    Args:
        instance_id (str): The identifier of the EC2 instance to stop.

    Returns:
        str: The response from the stop instance request.
    """
    try:
        response = ec2.stop_instances(InstanceIds=[instance_id])
        return response
    except Exception as e:
        return f"Error stopping instance: {str(e)}"


