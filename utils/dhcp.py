""" Routines and Classes to get information about DHCP server
"""

import re
from ipaddress import IPv4Address, IPv6Address

from .config_reader import ConfigData
from .regex import MySystemRegex


def parse_dhcp_lease_file(dhcp_file=None):
    """
    Open and parse DHCP Lease file
    :param dhcp_file: Path of the DHCP Lease file (config.ini)
    :return: Dict with fields parsed
    { mac_addr:
        {
            lease_time: <int>
            ipv4: <ip>
            ipv6: <ip>
            hostname: <str>
        }
    }
    """
    config = ConfigData()
    ip_regex = MySystemRegex()
    dhcp_config = config.get_dhcp_info()
    dhcp_data = dict()

    if dhcp_file is None:
        dhcp_file = dhcp_config['dhcp']['lease_file']
    with open(dhcp_file, 'r') as f:
        dhcp_lease_entries = [line.strip().split() for line in f]

    for entry in dhcp_lease_entries:
        if entry[0] != 'duid':
            ipv4_validation = re.compile(ip_regex.ipv4_regex())
            ipv6_validation = re.compile(ip_regex.ipv6_regex())
            if dhcp_data.get(entry[1]):
                # If the entry exists, we just add the IP Addr
                if ipv4_validation.match(entry[2]):
                    dhcp_data[entry[1]]['ipv4'] = IPv4Address(entry[2])
                if ipv6_validation.match(entry[2]):
                    dhcp_data[entry[1]]['ipv6'] = IPv6Address(entry[2])
            else:
                dhcp_data[entry[1]] = {
                    'lease_time': entry[0],
                    'hostname': entry[3].capitalize()
                }
                if ipv4_validation.match(entry[2]):
                    dhcp_data[entry[1]]['ipv4'] = IPv4Address(entry[2])
                if ipv6_validation.match(entry[2]):
                    dhcp_data[entry[1]]['ipv6'] = IPv6Address(entry[2])

    return dhcp_data
