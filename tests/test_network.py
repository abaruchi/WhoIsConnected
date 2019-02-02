import unittest
from ipaddress import IPv4Address, IPv6Address
from unittest import mock
from unittest.mock import patch
import requests_mock

from command import Command, run

from utils.network import check_device_status, get_mac_vendor


class TestNetwork(unittest.TestCase):

    def setUp(self):
        self.ipv4_addr = IPv4Address('192.168.1.10')
        self.ipv6_addr = IPv6Address('4bde:cb47:348e:9add:9258:d728:cedb:96f2')
        self.valid_mac_addr = 'a4:5e:60:ea:ff:c7'
        self.wrong_mac_vendor = 'a5:5e:60:ea:ff:aa'
        self.invalid_mac_addr = 'abc:12:123:a'

    def test_valid_mac_addr(self):
        valid_json = {"result":
                          {"company":"Apple, Inc.",
                           "mac_prefix":"A4:5E:60",
                           "address":"1 Infinite Loop,Cupertino  CA  95014,US",
                           "start_hex":"A45E60000000",
                           "end_hex":"A45E60FFFFFF",
                           "country":"US",
                           "type":"MA-L"}
                      }
        with requests_mock.Mocker() as m:
            m.get('http://macvendors.co/api/' + self.valid_mac_addr,
                  json=valid_json)
            vendor = get_mac_vendor(self.valid_mac_addr)
        self.assertEqual(vendor, "Apple, Inc.")

    def test_invalid_mac_addr(self):
        vendor = get_mac_vendor(self.invalid_mac_addr)
        self.assertEqual(vendor, "None")

    def test_unknown_vendor(self):
        unknown_vendor = {"result":
                              {"error": "no result"}
                          }
        with requests_mock.Mocker() as m:
            m.get('http://macvendors.co/api/' + self.wrong_mac_vendor,
                  json=unknown_vendor)
            vendor = get_mac_vendor(self.wrong_mac_vendor)
        self.assertEqual(vendor, "None")

    def test_host_ipv4_is_up(self):
        pass

    def test_host_ipv4_is_down(self):
        pass

    def test_host_ipv6_is_up(self):
        pass

    def test_host_ipv6_is_down(self):
        pass

