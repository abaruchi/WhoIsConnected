""" Main script to run WhoIsConnected
"""
import datetime
from enum import Enum
from time import sleep
from uuid import uuid4

import daemon
from pony.orm import db_session, select

from core.models import define_db
from core.views import last_ip_lease
from utils import config_reader, dhcp, email, network


class Transition(Enum):
    Off_to_On = 0
    On_to_Off = 1
    Unknown = 2


@db_session
def add_new_device(mac_addr, device_data, db):
    """
    Adds a new device to the Data Base if not exists
    :param device_data:
    :param db: database connection
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

    new_device = db.Device(
        mac_addr=mac_addr,
        name=device_data['hostname'],
        eth_vendor=network.get_mac_vendor(mac_addr),
        cur_status=cur_status
    )
    db.ConnectTime(
        id=uuid4(),
        lease_time=device_data['lease_time'],
        time=datetime.datetime.now(),
        transition=Transition.Unknown.value,
        device=new_device
    )
    db.IPLease(
        id=uuid4(),
        ipv4=str(ip4) if ip4 is not None else None,
        ipv6=str(ip6) if ip6 is not None else None,
        current=True,
        device=new_device
    )
    return new_device


@db_session
def updated_device_data(device, data_dict, db):
    """
    If a device already exists in database this routine will check if something
    has changed. If so, perform the proper updates.
    :param device: A device ORM to check possible updated
    :param data_dict: A dict with some data from dhcp_lease file to check
    :param db: database connection
    :return: The object if this was updated or None
    """
    updated = False
    last_il = last_ip_lease(device, db)

    # Updates IPLease data if necessary
    if last_il is not None:
        if str(data_dict['ipv4']) != last_il.ipv4 or \
                str(data_dict['ipv6']) != last_il.ipv6:
            last_il.current = False
            db.IPLease(
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
        db.ConnectTime(
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
def device_check(db):
    """
    Check if a device exists or not in database and call proper routines
    :param db: database connection
    :return: A dict with devices changed and/or added
    """
    dev = {
        'new_devices': list(),
        'changed_devices': list()
    }
    devices_in_lease = dhcp.parse_dhcp_lease_file()
    for mac_addr in devices_in_lease.keys():
        if db.Device.exists(mac_addr=mac_addr):
            cur_device = db.Device.get(mac_addr=mac_addr)
            device_data = {
                'lease_time': devices_in_lease[mac_addr]['lease_time'],
                'ipv4': devices_in_lease[mac_addr]['ipv4'] if
                devices_in_lease[mac_addr].get('ipv4') else None,
                'ipv6': devices_in_lease[mac_addr]['ipv6'] if
                devices_in_lease[mac_addr].get('ipv6') else None
            }
            update_device = updated_device_data(cur_device,
                                                device_data,
                                                db)
            if update_device is not None:
                dev['changed_devices'].append(update_device)

        else:
            device_added = add_new_device(mac_addr,
                                          devices_in_lease[mac_addr],
                                          db)
            if device_added is not None:
                dev['new_devices'].append(device_added)

    return dev


def mail_to_user(devices_data, db):
    """
    Routine that sends email to the user when something is detected
    :param devices_data: (dict) A dict returned
    :param db: database connection
    :return:
    """
    possible_status = ['changed_devices', 'new_devices']

    if sorted(possible_status) == sorted(devices_data.keys()):
        if len(devices_data['changed_devices']) > 0 or \
                len(devices_data['new_devices']) > 0:
            mail_to_send = email.Gmail(devices_data, db)
            mail_to_send.send_message()
        else:
            return None
    else:
        mail_to_send = email.Gmail(devices_data, db)
        message = "Wrong Status Detected, please check: "
        message += ','.join(devices_data.keys())
        mail_to_send.send_message(message=message)

    return None


def main():
    db = define_db(
        provider='sqlite',
        filename='whoisconnected',
        create_db=True)

    conf = config_reader.ConfigData()
    daemon_conf = conf.get_daemon_info()
    with daemon.DaemonContext():
        while True:
            devices = device_check(db)
            mail_to_user(devices, db)
            sleep(int(daemon_conf['daemon']['probe_min'])*60)


if __name__ == '__main__':
    main()
