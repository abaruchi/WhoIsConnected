""" Routines and Classes to inform the user about new Device on Network
"""
import smtplib

from pony.orm import db_session

from core.views import last_ip_lease

from .config_reader import ConfigData


@db_session
class Gmail(object):
    def __init__(self, devices_data, db):
        config = ConfigData()
        self.config_email = config.get_gmail_info()
        self.devices_data = devices_data
        self.db = db

        self.server = 'smtp.gmail.com'
        self.port = 587
        session = smtplib.SMTP(
            self.server, self.port
        )
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.config_email['gmail']['user'],
                      self.config_email['gmail']['pass'])
        self.session = session

    @db_session
    def send_message(self, message=None):

        body = ""
        if message is None:
            for device_stat in self.devices_data.keys():
                if device_stat == "changed_devices":
                    body += "<p><b>Devices Changed Status:</b><br />"
                    body += "<ul>"
                    for i, device in enumerate(self.devices_data[device_stat]):
                        ip_lease = last_ip_lease(device, self.db)
                        body += "<li> Device {}: {} / {} / {}".format(
                            i, device.name,
                            ip_lease.ipv4, device.cur_status)
                    body += "</ul>"
                    body += "</p>"

                if device_stat == "new_devices":
                    body += "<p><b>New Devices:</b><br />"
                    body += "<ul>"
                    for i, device in enumerate(self.devices_data[device_stat]):
                        ip_lease = last_ip_lease(device, self.db)
                        body += "<li> Device {}: {} / {} / {}".format(
                            i, device.name,
                            ip_lease.ipv4, device.cur_status)
                    body += "</ul>"
                    body += "</p>"
        else:
            body = message

        headers = [
            "From: " + self.config_email['gmail']['user'],
            "Subject: " + self.config_email['gmail']['subject'],
            "To: " + self.config_email['gmail']['dest'],
            "Content-Type: text/html"
        ]
        headers = "\r\n".join(headers)
        self.session.sendmail(
            self.config_email['gmail']['user'],
            self.config_email['gmail']['user'],
            headers + "\r\n\r\n" + body
        )
