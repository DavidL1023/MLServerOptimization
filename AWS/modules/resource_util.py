""" Checks resource utilization of AWS EC2 instances using Python and AWS Cloudwatch """

import sys
from pathlib import Path

# Add the parent directory to sys.path
parent_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(parent_dir)

import config.aws_config as aws_config
from datetime import datetime, timedelta, timezone

# Grab EC2 and CloudWatch clients
ec2 = aws_config.ec2
cloudwatch = aws_config.cloudwatch


def _get_ec2_cpu_datapoints(instance_id, start_time, end_time, period, statistics):
    """
    Retrieves CPU utilization metrics for a specified EC2 instance from AWS CloudWatch.

    This function queries AWS CloudWatch for the CPUUtilization metric of a given EC2 instance
    over a specified time range. The metrics are retrieved based on the defined period and
    statistics type.

    Args:
        instance_id (str): The identifier of the EC2 instance.
        start_time (datetime): The starting point of the time range for the metrics query.
        end_time (datetime): The end point of the time range for the metrics query.
        period (int): The granularity, in seconds, of the returned data points. This defines
                      the length of time represented by each data point.
        statistics (list[str]): A list of statistical values to retrieve. 
                                Typical values include 'Average', 'Minimum', 'Maximum', 'Sum', 'SampleCount'.

    Returns:
        list: A list of dictionaries, where each dictionary contains data points for the CPU utilization.
              Each data point includes the time of the data point and the metric value.

    Example of returned data point:
        {
            'Timestamp': datetime.datetime(2023, 1, 1, 12, 0),
            'SampleCount': 1.0,
            'Average': 25.0,
            'Unit': 'Percent'
        }
    """
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[
            {
                'Name': 'InstanceId',
                'Value': instance_id
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=statistics
    )
    return response['Datapoints']


def _calculate_average_cpu_usage(datapoints):
    """
    Calculates the average CPU usage from a list of CPU utilization data points.

    Args:
        datapoints (list of dict): A list of dictionaries, each containing data points for CPU utilization.
                                   Each data point should have a key 'Average' which holds the CPU utilization value.

    Returns:
        float: The calculated average CPU utilization over the given data points. Returns None if no data points are provided.

    Raises:
        ValueError: If any data point does not contain the 'Average' key.
    """
    if not datapoints:
        return None

    total = 0
    for point in datapoints:
        if 'Average' not in point:
            raise ValueError("Each data point must contain an 'Average' key")
        total += point['Average']

    return total / len(datapoints)


def get_cpu_datapoints_5_minutes(instance_id, period=aws_config.PERIOD, statistics=aws_config.STATISTICS):
    """
    Fetches the average CPU usage for a specified EC2 instance over the past 5 minutes.

    Args:
        instance_id (str): The identifier for the EC2 instance.
        period (int): The granularity, in seconds, of the returned data points.
        statistics (str): The metric statistics, e.g., 'Average', 'Sum'.

    Returns:
        float: The average CPU utilization for the specified instance in the past 5 minutes.
    """

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=5)
    return _get_ec2_cpu_datapoints(instance_id, start_time, end_time, period, statistics)


def get_cpu_datapoints_1_day(instance_id, period=aws_config.PERIOD, statistics=aws_config.STATISTICS):
    """
    Fetches the average CPU usage for a specified EC2 instance over the past day.

    Args:
        instance_id (str): The identifier for the EC2 instance.
        period (int): The granularity, in seconds, of the returned data points.
        statistics (str): The metric statistics, e.g., 'Average', 'Sum'.

    Returns:
        float: The average CPU utilization for the specified instance in the past day.
    """

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=1)
    return _get_ec2_cpu_datapoints(instance_id, start_time, end_time, period, statistics)


def get_most_used_server_5_minutes():
    """
    Identifies the EC2 instance with the highest average CPU usage over the past 5 minutes.

    Returns:
        tuple: A tuple containing the instance ID with the highest CPU usage and the average CPU usage value.
    """
    max_usage = 0
    max_instance = None
    for instance_id in aws_config.INSTANCE_IDS:
        datapoints = get_cpu_datapoints_5_minutes(instance_id)
        average_usage = _calculate_average_cpu_usage(datapoints)
        if average_usage > max_usage:
            max_usage = average_usage
            max_instance = instance_id
    return max_instance, max_usage


def get_least_used_server_5_minutes():
    """
    Identifies the EC2 instance with the lowest average CPU usage over the past 5 minutes.

    Returns:
        tuple: A tuple containing the instance ID with the lowest CPU usage and the average CPU usage value.
    """
    min_usage = float('inf')
    min_instance = None
    for instance_id in aws_config.INSTANCE_IDS:
        datapoints = get_cpu_datapoints_5_minutes(instance_id)
        average_usage = _calculate_average_cpu_usage(datapoints)
        if average_usage < min_usage:
            min_usage = average_usage
            min_instance = instance_id
    return min_instance, min_usage


def get_most_used_server_1_day():
    """
    Identifies the EC2 instance with the highest average CPU usage over the past day.

    Returns:
        tuple: A tuple containing the instance ID with the highest CPU usage and the average CPU usage value.
    """
    max_usage = 0
    max_instance = None
    for instance_id in aws_config.INSTANCE_IDS:
        datapoints = get_cpu_datapoints_1_day(instance_id)
        average_usage = _calculate_average_cpu_usage(datapoints)
        if average_usage > max_usage:
            max_usage = average_usage
            max_instance = instance_id
    return max_instance, max_usage


def get_least_used_server_1_day():
    """
    Identifies the EC2 instance with the lowest average CPU usage over the past day.

    Returns:
        tuple: A tuple containing the instance ID with the lowest CPU usage and the average CPU usage value.
    """
    min_usage = float('inf')
    min_instance = None
    for instance_id in aws_config.INSTANCE_IDS:
        datapoints = get_cpu_datapoints_1_day(instance_id)
        average_usage = _calculate_average_cpu_usage(datapoints)
        if average_usage < min_usage:
            min_usage = average_usage
            min_instance = instance_id
    return min_instance, min_usage

