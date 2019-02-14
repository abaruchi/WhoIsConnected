from pony.orm import db_session, select


@db_session
def last_ip_lease(device, db):
    """
    Retrieve last IPLease of a given device
    :param device:
    :param db: database connection
    :return:
    """
    ip_query = select(il for il in db.IPLease if
                      il.device == device and il.current)
    if ip_query.count() > 0:
        return ip_query.first()
    return None
