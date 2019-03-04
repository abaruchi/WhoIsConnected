""" Routines and Classes to inform the user about new Device on Network
"""
import boto3
from pony.orm import db_session

from core.views import last_ip_lease

from .config_reader import ConfigData


@db_session
class SendMAIL(object):
    def __init__(self, devices_data, db):
        config = ConfigData()
        self.config_email = config.get_email_info()
        self.devices_data = devices_data
        self.db = db

        user = self.config_email['email']['access_key']
        password = self.config_email['email']['secret_key']

        self.client = boto3.client(
            service_name='ses',
            region_name='eu-west-1',
            aws_access_key_id=user,
            aws_secret_access_key=password
        )

    @db_session
    def send_message(self, message=None):
        destination = {
            'ToAddresses': self.config_email['email']['dest'].
                replace(' ', '').split(',')
        }
        source = self.config_email['email']['sender']

        if message is None:
            body = ''
            for device_stat in self.devices_data.keys():
                if device_stat == "changed_devices":
                    body += "<p><b>Devices Changed Status:</b><br/>"
                    body += "<ul>"
                    for i, device in enumerate(self.devices_data[device_stat]):
                        ip_lease = last_ip_lease(device, self.db)
                        body += "<li> Device {}: {} / {} / {}".format(
                            i, device.name,
                            ip_lease.ipv4, device.cur_status)
                    body += "</ul>"
                    body += "</p>"

                if device_stat == "new_devices":
                    body += "<p><b>New Devices:</b><br />"
                    body += "<ul>"
                    for i, device in enumerate(self.devices_data[device_stat]):
                        ip_lease = last_ip_lease(device, self.db)
                        body += "<li> Device {}: {} / {} / {}".format(
                            i, device.name,
                            ip_lease.ipv4, device.cur_status)
                    body += "</ul>"
                    body += "</p>"

        else:
            body = message

        message_dict = {
            'Subject': {'Data': self.config_email['email']['subject']},
            'Body': {'Html': {'Data': body}}
        }
        self.client.send_email(
            Source=source,
            Destination=destination,
            Message=message_dict
        )
