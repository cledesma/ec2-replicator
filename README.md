# ec2-replicator

*Set environment variables: *
export aws_access_key_id=test
export aws_secret_access_key=test
export aws_region=test
export aws_instance_name_tag=test
export GMAIL_USERNAME=test
export GMAIL_PASSWORD='test'

*How to run: *
nohup python replicator.py &

*View logs* in replicator.log

*Access in browser.* Make sure to indicate your email address.
http://0.0.0.0:5000/clone?email=cledesma@ewise.com
