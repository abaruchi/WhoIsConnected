from datetime import datetime
from uuid import UUID

from pony.orm import Database, Optional, PrimaryKey, Required, Set, sql_debug

db = Database()
db.bind('sqlite',
        'whoisconnected',
        create_db=True)

db = Database()


class Device(db.Entity):
    mac_addr = PrimaryKey(str)
    name = Optional(str)
    eth_vendor = Optional(str)
    cur_status = Optional(str)
    connect_times = Set('ConnectTime')
    ip_leases = Set('IPLease')


class ConnectTime(db.Entity):
    id = PrimaryKey(UUID, auto=True)
    lease_time = Optional(str)
    time = Required(datetime)
    transition = Optional(str)  # 0 - Offline to Online, 1 - Online to Offline
    device = Required(Device)


class IPLease(db.Entity):
    id = PrimaryKey(UUID, auto=True)
    IPv4Addr = Optional(str, nullable=True)
    IPv6Addr = Optional(str, nullable=True)
    Current = Optional(bool)  # Indicates if this IPLease is the current assigned IP Addr
    device = Required(Device)


db.generate_mapping(create_tables=True)
