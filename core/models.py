from datetime import datetime
from uuid import UUID

from pony.orm import Database, Optional, PrimaryKey, Required, Set, sql_debug


db = Database()
db.bind('sqlite',
        'whoisconnected',
        create_db=True)


class Device(db.Entity):
    """
    Class to keep tracking of status changing over time
    """
    mac_addr = PrimaryKey(str)
    name = Required(str)
    eth_vendor = Optional(str)
    cur_status = Required(str)
    connect_times = Set('ConnectTime')


class ConnectTime(db.Entity):
    """
    Class to handle Devices running
    """
    id = PrimaryKey(UUID)
    lease_time = Required(str)
    time = Required(datetime)
    transition = Optional(int, default=0)
    device = Required(Device)


db.generate_mapping(create_tables=True)
