from datetime import datetime
from uuid import UUID

from pony.orm import Database, Optional, PrimaryKey, Required, Set, sql_debug


db = Database()
db.bind('sqlite',
        'whoisconnected',
        create_db=True)


class Device(db.Entity):
    mac_addr = PrimaryKey(str)
    name = Optional(str)
    eth_vendor = Optional(str)
    cur_status = Optional(str)
    connect_times = Set('ConnectTime')
    ip_leases = Set('IPLease')


class ConnectTime(db.Entity):
    id = PrimaryKey(UUID, auto=True)
    lease_time = Optional(int)
    time = Required(datetime)
    transition = Optional(int)
    device = Required(Device)


class IPLease(db.Entity):
    id = PrimaryKey(UUID, auto=True)
    ipv4 = Optional(str, nullable=True)
    ipv6 = Optional(str, nullable=True)
    current = Optional(bool)
    device = Required(Device)


db.generate_mapping(create_tables=True)
