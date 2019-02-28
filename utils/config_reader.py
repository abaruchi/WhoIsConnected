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
        current_key = 'dhcp'
        config_data = {
            current_key: dict()
        }
        config_data[current_key]['lease_file'] = self.config.get(
                                                        current_key,
                                                        'LEASE_FILE')
        config_data[current_key]['ignore_hosts'] = self.config.get(
                                                        current_key,
                                                        'IGNORE_HOSTS').\
            lower().replace(' ', '').split(',')

        return config_data

    def get_email_info(self):
        current_key = 'email'
        config_data = {
            current_key: dict()
        }

        config_data[current_key]['access_key'] = self.config.get(
                                                current_key,
                                                'ACCESS_KEY')
        config_data[current_key]['dest'] = self.config.get(
                                                current_key,
                                                'DEST')
        config_data[current_key]['secret_key'] = self.config.get(
                                                current_key,
                                                'SECRET_KEY')
        config_data[current_key]['subject'] = self.config.get(
                                                current_key,
                                                'SUBJECT')
        return config_data

    def get_network_info(self):
        current_key = 'network'
        config_data = {
            current_key: dict()
        }
        config_data[current_key]['mac_url'] = self.config.get(
                                                current_key,
                                                'MAC_URL')
        return config_data

    def get_daemon_info(self):
        current_key = 'daemon'
        config_data = {
            current_key: dict()
        }
        config_data[current_key]['probe_min'] = self.config.get(
                                                 current_key,
                                                 'PROBING_MIN')
        return config_data
