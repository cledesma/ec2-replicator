from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

# Read access keys from environment variables
# Get EC2 Connection
# Get reference to master machine
# Get security group of master machine
# Get keypair of master machine
# Get vpc of master machine
# Create AMI name
# Create an AMI from master machine
# Create an instance from AMI
# Get public IP of new AMI
# Deregister AMI
