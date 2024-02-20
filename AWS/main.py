""" Flask REST API to be used by frontend to gather server information and inflict changes """

from flask import Flask, jsonify, request
from modules import automation_platform, resource_util

app = Flask(__name__)

@app.route('/instance/status/<instance_id>', methods=['GET'])
def instance_status(instance_id):
    """Endpoint to check the status of an EC2 instance."""
    status = automation_platform.check_instance_status(instance_id)
    return jsonify({'instance_id': instance_id, 'status': status})

@app.route('/instance/start', methods=['POST'])
def start_instance():
    """Endpoint to start an EC2 instance."""
    data = request.json
    instance_id = data.get('instance_id')
    response = automation_platform.start_instance(instance_id)
    return jsonify(response)

@app.route('/instance/stop', methods=['POST'])
def stop_instance():
    """Endpoint to stop an EC2 instance."""
    data = request.json
    instance_id = data.get('instance_id')
    response = automation_platform.stop_instance(instance_id)
    return jsonify(response)

@app.route('/cpu/usage/5minutes/<instance_id>', methods=['GET'])
def cpu_usage_5minutes(instance_id):
    """Endpoint to get the CPU usage of an EC2 instance over the past 5 minutes."""
    usage = resource_util.get_cpu_datapoints_5_minutes(instance_id)
    return jsonify({'instance_id': instance_id, 'cpu_usage_last_5_minutes': usage})

@app.route('/cpu/usage/1day/<instance_id>', methods=['GET'])
def cpu_usage_1day(instance_id):
    """Endpoint to get the CPU usage of an EC2 instance over the past day."""
    usage = resource_util.get_cpu_datapoints_1_day(instance_id)
    return jsonify({'instance_id': instance_id, 'cpu_usage_last_1_day': usage})

if __name__ == '__main__':
    app.run(debug=True)