from pony.orm import db_session, select

from core.models import IPLease


@db_session
def last_ip_lease(device):
    """
    Retrieve last IPLease of a given device
    :param device:
    :return:
    """
    ip_query = select(il for il in IPLease if il.device==device and il.current)
    if ip_query.count() > 0:
        return ip_query.first()
    return None
