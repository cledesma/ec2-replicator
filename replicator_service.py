import boto.ec2
import os
import time
import datetime
import smtplib
import logging
from time import sleep

class ReplicatorService:

    def clone(self, email):
        conn = self.get_connection()
        reference_instance = self.get_reference_instance(conn)
        image_name = self.get_image_name()
        image_id = self.create_image(reference_instance, image_name)

        while True:
            image = conn.get_all_images(image_ids=image_id)[0]
            image_state = image.state
            logging.info("Is image " + image_id + " available? " + image_state)
            if (image_state == 'available'):
                logging.info("Image " + image_id + " is " + image_state)
                instance = self.clone_instance(
                	reference_instance, 
                	image_id, 
                	conn)
                break
            else:
                logging.info("Retrying after 30 seconds")
                sleep(30)

        while True:
            instance = self.get_instance(instance.id, conn)
            logging.info("Is instance " + instance.id + " runnning? " + instance.state)
            if (instance.state == 'running'):
                logging.info("Instance setup complete!")
                url = instance.public_dns_name
                logging.info("URL: " + url)
                self.send_mail(email, url)
                break
            else:
                logging.info("Retrying after 30 seconds")
                sleep(30)

    def get_instance(self, instance_id, conn):

        logging.info("get_instance: " + instance_id)
        try:
            instances = conn.get_only_instances();
            for instance in instances:
                if (instance.id == instance_id):
                    logging.info("Instance retrieved")
                    break;
        except Exception, e:
            logging.info("Exception: " + str(e))

        logging.info("Instance: " + instance.id)
        return instance

    def get_connection(self):

        logging.info("get_connection")
        try:
            aws_access_key_id = os.environ['aws_access_key_id']
            aws_secret_access_key = os.environ['aws_secret_access_key']
            aws_region = os.environ['aws_region']
        except Exception, e:
            logging.info("Required environment variables are missing" + str(e))

        try:
            conn = boto.ec2.connect_to_region(aws_region,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key)
        except Exception, e:
            logging.info("Failed to get connection" + str(e))
        return conn

    def get_reference_instance(self, conn):

        logging.info("get_reference_instance")
        try:
            instances = conn.get_only_instances()
        except Exception, e:
            logging.info("Failed to get instances" + str(e))

        aws_instance_name_tag = self.get_aws_instance_name_tag()

        for instance in instances:

            try:
                if (instance.tags['Name'] == aws_instance_name_tag):
                    reference_instance = instance
                    logging.info("reference_instance: " + reference_instance.id)
                    break
            except Exception, e:
                logging.info("Instance has no tag Name" + str(e))

        return reference_instance

    def get_aws_instance_name_tag(self):

        logging.info("get_aws_instance_name_tag")
        try:
            aws_instance_name_tag = os.environ['aws_instance_name_tag']
        except Exception, e:
            logging.info("Environment variable aws_instance_name_tag is undefined" + str(e))

        return aws_instance_name_tag

    def get_image_name(self):

        logging.info("get_image_name")
        t = time.time()
        timestamp = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d-%H-%M-%S')

        image_name = self.get_aws_instance_name_tag() + "-" + timestamp
        logging.info(image_name)

        return image_name

    def create_image(self, target_instance, image_name):

        logging.info("create_image")
        try:
            image_id = target_instance.create_image(
                image_name,
                description=None,
                no_reboot=True,
                dry_run=False)
            logging.info("New image ID: " + image_id)
        except Exception, e:
            logging.info("Problem with creating image" + str(e))

        return image_id

    def clone_instance(self, instance, image_id, conn):

        logging.info("create_instance")
        security_group_ids = []
        instance_type = instance.instance_type
        instance_key_name = instance.key_name
        instance_groups = instance.groups
        for group in instance_groups:
            security_group_ids.append(group.id)
        instance_placement = instance.placement

        logging.info("image id: " + image_id)
        logging.info("instance type: " + instance_type)
        logging.info("key name: " + instance_key_name)
        logging.info("group ids: ".join(security_group_ids))
        logging.info("placement: " + instance_placement)

        instances = conn.run_instances(image_id,
            instance_type=instance_type,
            key_name=instance_key_name,
            security_group_ids=security_group_ids,
            placement=instance_placement,
            monitoring_enabled=False);
        instance = instances.instances[0]

        return instance

    def send_mail(self, email, url):
            try:
                logging.info("begin send_mail")
                logging.info("email: " + email)
                logging.info("url: " + url)
                email_username = os.environ['GMAIL_USERNAME']
                email_password = os.environ['GMAIL_PASSWORD']
                to_list = []
                cc_list = []
                bcc_list = []
                bcc_list.append(email)
                header  = 'From: %s\n' % os.environ['GMAIL_USERNAME']
                header += 'To: %s\n' % ','.join(to_list)
                header += 'Cc: %s\n' % ','.join(cc_list)
                header += 'Subject: %s\n\n' % "New server: " + url
                message = header + "Use the URL to access the new server"
                smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
                smtp_server.starttls()
                smtp_server.login(email_username, email_password)
                smtp_server.sendmail(email_username, bcc_list, message)
                smtp_server.quit()
                logging.info("end send_mail")
            except Exception, e:
                logging.info("Exception: " + str(e))
