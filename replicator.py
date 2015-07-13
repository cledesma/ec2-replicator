from flask import Flask
import boto.ec2
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    #app.run()

    # Read access keys from environment variables
    aws_access_key_id = os.environ['aws_access_key_id']
    aws_secret_access_key = os.environ['aws_secret_access_key']
    aws_region = os.environ['aws_region']
    aws_instance_name_tag = os.environ['aws_instance_name_tag']

    # Get EC2 Connection
    conn = boto.ec2.connect_to_region(aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    # Get reference to master machine
    instances = conn.get_only_instances()
    security_group_ids = []
    for instance in instances:
        if (instance.tags['Name'] == aws_instance_name_tag):
            instance_image_id = instance.image_id
            instance_type = instance.instance_type
            instance_key_name = instance.key_name
            instance_groups = instance.groups
            for group in instance_groups:
                security_group_ids.append(group.id)
            instance_placement = instance.placement 

    print instance_image_id
    print instance_type
    print instance_key_name
    print security_group_ids
    print instance_placement
    # Get security group of master machine
    # Get keypair of master machine
    # Get vpc of master machine
    # Create AMI name
    # Create an AMI from master machine
    # Create an instance from AMI
    #image_id=image_id
    #instance_type=instance_type
    #key_name=key_name
    #security_group_ids=security_group_ids
    #placement=aws_region
    #monitoring_enabled=true
    # Get public IP of new AMI
    # Deregister AMI