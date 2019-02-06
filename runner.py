""" Main script to run WhoIsConnected
"""
import datetime
from ipaddress import IPv4Address, IPv6Address
from time import sleep
from uuid import uuid4

from pony.orm import db_session

from core.models import ConnectTime, Device
from utils import dhcp, email, network, config_reader


@db_session
def populate__device_info():
    """
    Populate Devices DB with devices information

    :return: All devices changed or added to the DB (dict)
    {
        'new_devices': list(),
        'changed_devices': list()
    }
    """
    dev = {
        'new_devices': list(),
        'changed_devices': list()
    }
    devices_in_lease = dhcp.parse_dhcp_lease_file()
    for mac_addr in devices_in_lease.keys():
        if Device.exists(mac_addr=mac_addr):
            device = Device.get(mac_addr=mac_addr)
            if device.ip_addr_v4 is not None:
                cur_device_status = network.check_device_status(
                    IPv4Address(device.ip_addr_v4))
            elif device.ip_addr_v6 is not None:
                cur_device_status = network.check_device_status(
                    IPv6Address(device.ip_addr_v6)
                )
            else:
                continue

            if cur_device_status != device.cur_status:
                if device.cur_status == 'Offline':
                    transaction = 1
                else:
                    transaction = 0
                ConnectTime(
                    id=uuid4(),
                    lease_time=devices_in_lease[mac_addr]['lease_time'],
                    time=datetime.datetime.now(),
                    transition=transaction,
                    device=device
                )
                dev['changed_devices'].append(device)
        else:
            if devices_in_lease[mac_addr].get('ipv4'):
                ip4 = devices_in_lease[mac_addr]['ipv4']
            else:
                ip4 = None
            if devices_in_lease[mac_addr].get('ipv6'):
                ip6 = devices_in_lease[mac_addr]['ipv6']
            else:
                ip6 = None

            new_device = Device(mac_addr=mac_addr,
                                name=devices_in_lease[mac_addr]['hostname'],
                                cur_status=network.check_device_status(ip4),
                                ip_addr_v4=str(ip4),
                                ip_addr_v6=str(ip6))
            new_device.eth_vendor = network.get_mac_vendor(mac_addr)

            ConnectTime(id=uuid4(),
                        lease_time=devices_in_lease[mac_addr]['lease_time'],
                        device=new_device,
                        time=datetime.datetime.now())
            dev['new_devices'].append(new_device)

    return dev


def mail_to_user(devices_data):
    """
    Routine that sends email to the user when something is detected
    :param devices_data: (dict) A dict returned
    :return:
    """
    possible_status = ['changed_devices', 'new_devices']

    if sorted(possible_status) == sorted(devices_data.keys()):
        if len(devices_data['changed_devices']) > 0 or \
                len(devices_data['new_devices']) > 0:
            mail_to_send = email.Gmail(devices_data)
            mail_to_send.send_message()
        else:
            return None
    else:
        mail_to_send = email.Gmail(devices_data)
        message = "Wrong Status Detected, please check: "
        message += ','.join(devices_data.keys())
        mail_to_send.send_message(message=message)

    return None


def main():
    conf = config_reader.ConfigData()
    daemon_conf = conf.get_daemon_info()

    while True:
        devices = populate__device_info()
        mail_to_user(devices)

        sleep(int(daemon_conf['daemon']['probe_min'])*60)


if __name__ == '__main__':
    main()
