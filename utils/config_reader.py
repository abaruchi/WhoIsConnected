from configparser import RawConfigParser
import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG_FILE_PATH = os.path.join(CURRENT_DIR, "../config.ini")


class ConfigData(object):

    def __init__(self, config_file=CONFIG_FILE_PATH):
        self.config_file = config_file
        self.config = RawConfigParser()
        self.config.read(self.config_file)

    def get_dhcp_info(self):
        config_data = {
            'dhcp': dict()
        }
        config_data['dhcp']['lease_file'] = self.config.get(
                                                        'dhcp',
                                                        'LEASE_FILE')
        config_data['dhcp']['know_devices'] = self.config.get(
                                                        'dhcp',
                                                        'KNOW_DEVICES')
        return config_data

    def get_gmail_info(self):
        config_data = {
            'gmail': dict()
        }

        config_data['gmail']['user'] = self.config.get(
                                                'gmail',
                                                'USER')
        config_data['gmail']['dest'] = self.config.get(
                                                'gmail',
                                                'DEST')
        config_data['gmail']['pass'] = self.config.get(
                                                'gmail',
                                                'PASS')
        config_data['gmail']['subject'] = self.config.get(
                                                'gmail',
                                                'SUBJECT')
        return config_data

    def get_network_info(self):
        config_data = {
            'network': dict()
        }
        config_data['network']['mac_url'] = self.config.get(
                                                'network',
                                                'MAC_URL')
        return config_data
