from flask import Flask
import boto.ec2
import os
import time
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


def get_connection():

    print "get_connection"
    try:
        aws_access_key_id = os.environ['aws_access_key_id']
        aws_secret_access_key = os.environ['aws_secret_access_key']
        aws_region = os.environ['aws_region']
    except Exception, e:
        print "Required environment variables are missing"

    try: 
        conn = boto.ec2.connect_to_region(aws_region, 
            aws_access_key_id=aws_access_key_id, 
            aws_secret_access_key=aws_secret_access_key)
    except Exception, e:
        print "Failed to get connection"
    return conn

def get_reference_instance(conn):

    print "get_reference_instance"
    try:
        instances = conn.get_only_instances()
    except Exception, e:
        print "Failed to get instances"

    aws_instance_name_tag = get_aws_instance_name_tag()

    for instance in instances:

        try:
            if (instance.tags['Name'] == aws_instance_name_tag):
                reference_instance = instance
                print "reference_instance: " + reference_instance.id
                break
        except Exception, e:
            print "Instance has no tag Name"

    return reference_instance

def get_aws_instance_name_tag():

    print "get_aws_instance_name_tag"
    try:
        aws_instance_name_tag = os.environ['aws_instance_name_tag']
    except Exception, e:
        print "Environment variable aws_instance_name_tag is undefined"

    return aws_instance_name_tag

def get_image_name():
    
    print "get_image_name"
    t = time.time()
    timestamp = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d-%H-%M-%S')
    
    image_name = get_aws_instance_name_tag() + "-" + timestamp 
    print image_name

    return image_name

def create_image(target_instance, image_name):

    print "create_image"
    try:
        # image_id = target_instance.create_image(
        #     image_name, 
        #     description=None, 
        #     no_reboot=True, 
        #     dry_run=False)
        image_id = 'ami-63838053' # TODO Remove
        print "New image ID: " + image_id
    except Exception, e:
        print "Problem with creating image"

    return image_id

def clone_instance(instance, image_id):

    print "create_instance"
    security_group_ids = []
    instance_type = instance.instance_type
    instance_key_name = instance.key_name
    instance_groups = instance.groups
    for group in instance_groups:
        security_group_ids.append(group.id)
    instance_placement = instance.placement 

    print "image id: " + image_id
    print "instance type: " + instance_type
    print "key name: " + instance_key_name
    print "group ids: ".join(security_group_ids)
    print "placement: " + instance_placement

    instances = conn.run_instances(image_id, 
        instance_type=instance_type, 
        key_name=instance_key_name, 
        security_group_ids=security_group_ids, 
        placement=instance_placement, 
        monitoring_enabled=False);
    instance = instances.instances[0]

    return instance

if __name__ == '__main__':
    #app.run()

    conn = get_connection()
    reference_instance = get_reference_instance(conn)
    image_name = get_image_name()
    image_id = create_image(reference_instance, image_name)




    image = conn.get_all_images(image_ids=image_id)[0]
    image_state = image.state
    print "Is image " + image_id + " available? " + image_state
    if (image_state == 'available'):
        print "Image " + image_id + " is " + image_state
        instance = clone_instance(reference_instance, image_id)



    if (instance.state == 'running'):
        print "Instance setup complete!"
        print "Public URL: " + instance.public_dns_name
        #TODO Send email of public dns name


