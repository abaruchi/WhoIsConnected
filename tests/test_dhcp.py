import unittest
from ipaddress import IPv4Address, IPv6Address

from utils.dhcp import parse_dhcp_lease_file


class TestDHCP(unittest.TestCase):
    def setUp(self):
        dhcp_lease_file = './dhcp_leases_test'
        self.dhcp_data = parse_dhcp_lease_file(dhcp_lease_file)

    def test_data_parsing(self):
        self.assertEqual(3, len(self.dhcp_data.keys()))

    def test_ipv4_parsing(self):
        ipv4_count = 0
        for v in self.dhcp_data.values():
            if v.get('ipv4'):
                if isinstance(v['ipv4'], IPv4Address):
                    ipv4_count += 1

        self.assertEqual(3, ipv4_count)

    def test_ipv6_parsing(self):
        ipv6_count = 0
        for v in self.dhcp_data.values():
            if v.get('ipv6'):
                if isinstance(v['ipv6'], IPv6Address):
                    ipv6_count += 1

        self.assertEqual(1, ipv6_count)
