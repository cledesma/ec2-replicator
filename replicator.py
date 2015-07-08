from flask import Flask
import boto.ec2
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    #app.run()

    print "Hello"
    # Read access keys from environment variables
    aws_access_key_id = os.environ['aws_access_key_id']
    aws_secret_access_key = os.environ['aws_secret_access_key']
    aws_region = os.environ['aws_region']

    key_name = os.environ['key_name']
    instance_type = os.environ['instance_type']
    security_group_ids = os.environ['security_group_ids']

    # Get EC2 Connection
    conn = boto.ec2.connect_to_region(aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    print conn
    # Get reference to master machine
    instances = conn.get_all_instances()
    print instances
    # Get security group of master machine
    # Get keypair of master machine
    # Get vpc of master machine
    # Create AMI name
    # Create an AMI from master machine
    # Create an instance from AMI
    image_id=image_id
    instance_type=instance_type
    key_name=key_name
    security_group_ids=security_group_ids
    placement=aws_region
    monitoring_enabled=true
    # Get public IP of new AMI
    # Deregister AMI
