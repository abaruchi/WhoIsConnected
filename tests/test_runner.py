import datetime
import unittest
from ipaddress import IPv4Address, IPv6Address
from unittest.mock import patch
from uuid import uuid4

from pony.orm import db_session

from core.models import define_db
from runner import (
    Transition, add_new_device, device_check, updated_device_data)


class TestRunner(unittest.TestCase):

    def setUp(self):
        self.db_test = define_db(
            provider='sqlite',
            filename='../tests/testdb',
            create_db=True
        )

        self.parse_dhcp_return = {
            '03-2C-07-6F-A6-46':
                {
                    'lease_time': 1548724194,
                    'ipv4': IPv4Address('10.10.5.10'),
                    'ipv6': None,
                    'hostname': 'device01'
                },
            '17-C6-C1-E0-FE-EF':
                {
                    'lease_time': 1548724200,
                    'ipv4': IPv4Address('10.10.5.70'),
                    'ipv6': None,
                    'hostname': 'device04'
                }
        }

    def tearDown(self):
        self.db_test.drop_all_tables(with_all_data=True)

    @db_session
    def __create_test_data(self):

        self.device_01 = self.db_test.Device(
            mac_addr='03-2C-07-6F-A6-46',
            name='device01',
            eth_vendor='Capsule Corp',
            cur_status='Online'
        )
        self.db_test.ConnectTime(
            id=uuid4(),
            lease_time=1548724194,
            time=datetime.datetime.now(),
            transition=Transition.Off_to_On.value,
            device=self.device_01
        )
        self.db_test.IPLease(
            id=uuid4(),
            ipv4='10.10.5.10',
            ipv6=None,
            current=True,
            device=self.device_01
        )

        self.device_02 = self.db_test.Device(
            mac_addr='2C-DF-58-84-49-BE',
            name='device02',
            eth_vendor='Acme LTDA',
            cur_status='Offline'
        )
        self.db_test.ConnectTime(
            id=uuid4(),
            lease_time=1548724194,
            time=datetime.datetime.now(),
            transition=Transition.On_to_Off.value,
            device=self.device_02
        )
        self.db_test.IPLease(
            id=uuid4(),
            ipv4='10.10.5.15',
            ipv6='641:2234:e141:21d0:8541:b716:6fc7:3821',
            current=True,
            device=self.device_02
        )

    def test_add_new_device(self):
        self.__create_test_data()
        dhcp_dict = {
            '65-DD-65-82-B8-19': {
                'lease_time': 1548725311,
                'ipv4': IPv4Address('10.10.5.35'),
                'ipv6': IPv6Address('1627:d27f:350:11a7:dec6:7385:bc1b:e0d'),
                'hostname': 'device03'
            }
        }

        add_device03 = add_new_device(
            mac_addr='65-DD-65-82-B8-19',
            device_data=dhcp_dict['65-DD-65-82-B8-19'],
            db=self.db_test
        )
        self.assertEqual(
            dhcp_dict['65-DD-65-82-B8-19']['hostname'],
            add_device03.name
        )

    @db_session
    def test_ip_updated_device(self):
        self.__create_test_data()
        device02 = self.db_test.Device.get(mac_addr='2C-DF-58-84-49-BE')

        changed_ip = {
            '2C-DF-58-84-49-BE': {
                'lease_time': 1548725422,
                'ipv4': IPv4Address('10.10.5.60'),
                'ipv6': IPv6Address('652:2235:e141:21d0:8541:b800:6fc7:4021'),
                'hostname': 'device02'
            }
        }
        changed_device02 = updated_device_data(
            device=device02,
            data_dict=changed_ip['2C-DF-58-84-49-BE'],
            db=self.db_test
        )
        self.assertEqual(
            changed_ip['2C-DF-58-84-49-BE']['hostname'],
            changed_device02.name
        )

    @db_session
    @patch('utils.network.check_device_status', return_value='Online')
    def test_status_updated_device(self, mock_magic):
        self.__create_test_data()
        device02 = self.db_test.Device.get(mac_addr='2C-DF-58-84-49-BE')

        changed_status = {
            '2C-DF-58-84-49-BE': {
                'lease_time': 1548725422,
                'ipv4': IPv4Address('10.10.5.15'),
                'ipv6': IPv6Address('641:2234:e141:21d0:8541:b716:6fc7:3821'),
                'hostname': 'device02'
            }
        }
        changed_device02 = updated_device_data(
            device=device02,
            data_dict=changed_status['2C-DF-58-84-49-BE'],
            db=self.db_test
        )
        self.assertEqual(
            changed_status['2C-DF-58-84-49-BE']['hostname'],
            changed_device02.name
        )

    @db_session
    def test_device_with_no_updates(self):
        self.__create_test_data()
        device02 = self.db_test.Device.get(mac_addr='2C-DF-58-84-49-BE')

        changed_status = {
            '2C-DF-58-84-49-BE': {
                'lease_time': 2045725422,
                'ipv4': IPv4Address('10.10.5.15'),
                'ipv6': IPv6Address('641:2234:e141:21d0:8541:b716:6fc7:3821'),
                'hostname': 'device02'
            }
        }
        changed_device02 = updated_device_data(
            device=device02,
            data_dict=changed_status['2C-DF-58-84-49-BE'],
            db=self.db_test
        )
        self.assertEqual(
            None,
            changed_device02
        )

    @db_session
    @patch('utils.dhcp.parse_dhcp_lease_file',
           return_value={
            '03-2C-07-6F-A6-46':
                {
                    'lease_time': 1548724194,
                    'ipv4': IPv4Address('10.10.5.10'),
                    'hostname': 'device01'
                },
            '17-C6-C1-E0-FE-EF':
                {
                    'lease_time': 1548724200,
                    'ipv4': IPv4Address('10.10.5.70'),
                    'ipv6': None,
                    'hostname': 'device04'
                }
        })
    def test_device_check(self, mock_magic01):
        self.__create_test_data()
        devices = device_check(self.db_test)

        self.assertEqual(
            devices['new_devices'][0].name,
            'device04'
        )

        self.assertEqual(
            devices['changed_devices'][0].name,
            'device01'
        )
