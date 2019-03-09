""" Routines and Classes to inform the user about new Device on Network
"""
import os

import boto3
from jinja2 import Environment, FileSystemLoader
from pony.orm import db_session

from core.views import last_ip_lease

from .config_reader import ConfigData


def email_body_generator(device_dict):
    """

    :param devices_dict:
    :return:
    """
    this_dir = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(this_dir + '/templates/'))

    return j2_env.get_template('email_template.html').render(items=device_dict)


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
    def __build_dict_to_render(self):
        """
        Creates a dict used by Jinja2 template to render the email that will be
        used to send to the user.

        :return: A dict to Jinja2 templates render
        """
        dict_to_render = {
            'changed_devices': dict(),
            'new_devices': dict()
        }

        for device_stat in self.devices_data.keys():
            if device_stat == 'changed_devices':
                for device in self.devices_data[device_stat]:
                    ip_lease = last_ip_lease(device, self.db)
                    dict_to_render[device_stat][device.mac_addr] = {
                        'ip': ip_lease.ipv4,
                        'name': device.name,
                        'status': device.cur_status
                    }
            if device_stat == 'new_devices':
                for device in self.devices_data[device_stat]:
                    ip_lease = last_ip_lease(device, self.db)
                    dict_to_render[device_stat][device.mac_addr] = {
                        'ip': ip_lease.ipv4,
                        'name': device.name,
                        'status': device.cur_status
                    }
        return dict_to_render

    def send_message(self, message=None):
        destination = {
            'ToAddresses': self.config_email['email']['dest'].
                replace(' ', '').split(',')
        }
        source = self.config_email['email']['sender']
        dict_to_render = self.__build_dict_to_render()
        if message is None:
            body = email_body_generator(dict_to_render)
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
