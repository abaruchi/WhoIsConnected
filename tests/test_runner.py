import unittest
from ipaddress import IPv4Address, IPv6Address
from unittest.mock import patch

import requests_mock

from utils.network import check_device_status, get_mac_vendor


class TestRunner(unittest.TestCase):

    def setUp(self):
        pass

    def test_add_new_device(self):
        """
        Test cases:
        1. Device already exists in database
        2. Device does not exist in database
        """
        pass


    def test_updated_device_data(self):
        """
        Test cases:
        1. Device IP has changed
        2. Device Status has changed
        3. No changed detected
        """
        pass

    def test_device_check(self):
        """
        Test cases:
        1. Device already exists in database
        2. Device does not exist in database
        """
        pass