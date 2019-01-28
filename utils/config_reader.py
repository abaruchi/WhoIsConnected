from configparser import RawConfigParser
import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE_PATH = os.path.join(CURRENT_DIR, "../config.ini")


class ConfigData(object):

    def __init__(self, config_file=CONFIG_FILE_PATH):
        self.config_file = config_file
        self.config = RawConfigParser()
        self.config.read(self.config_file)
        self.config_data = dict()

    def get_dhcp_info(self):
        self.config_data = {
            'dhcp': dict()
        }
        self.config_data['dhcp']['lease_file'] = self.config.get(
                                                        'dhcp',
                                                        'LEASE_FILE')
        self.config_data['dhcp']['know_devices'] = self.config.get(
                                                        'dhcp',
                                                        'KNOW_DEVICES')
        return self.config_data

    def get_gmail_info(self):
        self.config_data = {
            'gmail': dict()
        }

        self.config_data['gmail']['user'] = self.config.get(
                                                'gmail',
                                                'USER')
        self.config_data['gmail']['pass'] = self.config.get(
                                                'gmail',
                                                'PASS')
        self.config_data['gmail']['subject'] = self.config.get(
                                                'gmail',
                                                'SUBJECT')

    def get_network_info(self):
        self.config_data = {
            'network': dict()
        }

        self.config_data['network']['mac_url'] = self.config.get(
                                                'network',
                                                'MAC_URL')
