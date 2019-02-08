""" Main script to run WhoIsConnected
"""
import datetime
from enum import Enum
from time import sleep
from uuid import uuid4

import daemon
from pony.orm import db_session, select

from core.models import ConnectTime, Device, IPLease
from utils import config_reader, dhcp, email, network


class Transition(Enum):
    Off_to_On = 0
    On_to_Off = 1
    Unknown = 2


@db_session
def add_new_device(mac_addr, device_data):
    """
    Adds a new device to the Data Base if not exists
    :param device_data:
    :return: The Device object
    """
    ip4 = device_data['ipv4'] if device_data.get('ipv4') else None
    ip6 = device_data['ipv6'] if device_data.get('ipv6') else None

    ip4_status = network.check_device_status(ip4)
    ip6_status = network.check_device_status(ip6)

    if ip4_status == 'Online' or ip6_status == 'Online':
        cur_status = 'Online'
    else:
        cur_status = 'Offline'

    new_device = Device(
        mac_addr=mac_addr,
        name=device_data['hostname'],
        eth_vendor=network.get_mac_vendor(mac_addr),
        cur_status=cur_status
    )
    ConnectTime(
        id=uuid4(),
        lease_time=device_data['lease_time'],
        time=datetime.datetime.now(),
        transition=Transition.Unknown.value,
        device=new_device
    )
    IPLease(
        id=uuid4(),
        ipv4=str(ip4) if ip4 is not None else None,
        ipv6=str(ip6) if ip6 is not None else None,
        current=True,
        device=new_device
    )
    return new_device


@db_session
def updated_device_data(device, data_dict):
    """
    If a device already exists in database this routine will check if something
    has changed. If so, perform the proper updates.
    :param device: A device ORM to check possible updated
    :param data_dict: A dict with some data from dhcp_lease file to check
    :return: The object if this was updated or None
    """
    updated = False
    ip_lease_query = select(il for il in IPLease if il.device == device and
                      il.current)

    # Updates IPLease data if necessary
    if ip_lease_query.count() > 0:
        ip_lease = ip_lease_query.first()
        if str(data_dict['ipv4']) != ip_lease.ipv4 or \
            str(data_dict['ipv6']) != ip_lease.ipv6:
            ip_lease.current = False
            IPLease(
                id=uuid4(),
                ipv4=str(data_dict['ipv4']),
                ipv6=str(data_dict['ipv6']),
                current=True,
                device=device
            )
            updated = True

    # Updates Connection Infor if necessary
    device_status_v4 = network.check_device_status(data_dict['ipv4'])
    device_status_v6 = network.check_device_status(data_dict['ipv6'])
    device_status = 'Online' if device_status_v4 == 'Online' or \
                                device_status_v6 == 'Online' else 'Offline'
    if device_status != device.cur_status:
        ConnectTime(
            id=uuid4(),
            lease_time=data_dict['lease_time'],
            time=datetime.datetime.now(),
            transition=Transition.Off_to_On.value if device_status == 'Online'
            else Transition.On_to_Off.value,
            device=device
        )
        device.cur_status = device_status
        updated = True

    if updated:
        return device
    else:
        return None


@db_session
def device_check():
    """
    Check if a device exists or not in database and call proper routines
    :return: A dict with devices changed and/or added
    """
    dev = {
        'new_devices': list(),
        'changed_devices': list()
    }
    devices_in_lease = dhcp.parse_dhcp_lease_file()
    for mac_addr in devices_in_lease.keys():
        if Device.exists(mac_addr=mac_addr):
            cur_device = Device.get(mac_addr=mac_addr)
            device_data = {
                'lease_time': devices_in_lease[mac_addr]['lease_time'],
                'ipv4': devices_in_lease[mac_addr]['ipv4'] if
                devices_in_lease[mac_addr].get('ipv4') else None,
                'ipv6': devices_in_lease[mac_addr]['ipv6'] if
                devices_in_lease[mac_addr].get('ipv6') else None
            }
            update_device = updated_device_data(cur_device, device_data)
            if update_device is not None:
                dev['changed_devices'].append(update_device)

        else:
            device_added = add_new_device(mac_addr, devices_in_lease[mac_addr])
            if device_added is not None:
                dev['new_devices'].append(device_added)

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
    with daemon.DaemonContext():
        while True:
            devices = device_check()
            mail_to_user(devices)
            sleep(int(daemon_conf['daemon']['probe_min'])*60)


if __name__ == '__main__':
    main()
