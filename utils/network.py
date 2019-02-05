""" Routines and Classes to get information about devices in network
"""

import os
import re
from ipaddress import IPv4Address, IPv6Address

import requests

from .config_reader import ConfigData
from .regex import MySystemRegex


def get_mac_vendor(mac_addr):
    """
    Routine to identify the vendor of a given mac address
    Ref.: https://macvendors.co/api/python

    :param mac_addr: The mac address to check (str)
    :return: Mac Address vendor (str)
    """
    mac_regex = MySystemRegex()
    mac_validation = re.compile(mac_regex.mac_addr())

    if not mac_validation.match(mac_addr):
        return "None"

    config = ConfigData()
    network_config = config.get_network_info()
    mac_addr_url = network_config['network']['mac_url']

    r = requests.get(mac_addr_url % mac_addr)
    try:
        response = r.json()['result']['company']
    except KeyError:
        return "None"
    return response


def check_device_status(ip_addr):
    """
    Returns if a given device - ip addr - is online of not
    :param ip_addr: An IP Addr (IPv4 or IPv6 Object)
    :return: Online or Offline (str)
    """

    if isinstance(ip_addr, IPv4Address):
        ip_to_ping = str(ip_addr)
        r = os.system("ping -c 1 " + ip_to_ping + " > /dev/null")
        if r == 0:
            return "Online"
        return "Offline"

    elif isinstance(ip_addr, IPv6Address):
        ip_to_ping = str(ip_addr)
        r = os.system("ping6 -c 1" + ip_to_ping + " > /dev/null")
        if r == 0:
            return "Online"
        return "Offline"
