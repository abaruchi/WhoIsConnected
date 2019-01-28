"""
This file contains regex used by the system. Any regex should be added to
this file
"""


class MySystemRegex(object):

    def ipv4_regex(self):
        return r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'

    def ipv6_regex(self):
        return (r"(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:"
                 r"[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|"
                 r"2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|"
                 r"1[0-9]{2}|2[0-4][0-9]|25[0-5]))|::(?:[0-9A-Fa-f]{1,4}:"
                 r"){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:"
                 r"[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}("
                 r"?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
                 r")|(?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}("
                 r"?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:"
                 r"[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}("
                 r"?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
                 r")|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?"
                 r":[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:"
                 r"[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1"
                 r"[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:"
                 r"[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:"
                 r"(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::("
                 r"?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:"
                 r"[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1"
                 r"[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?"
                 r":[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:"
                 r"(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?:"
                 r":[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:"
                 r"[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|"
                 r"2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1"
                 r"[0-9]{2}|2[0-4][0-9]|25[0-5]))|(?:(?:"
                 r"[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:"
                 r"[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:"
                 r"(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|"
                 r"25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|"
                 r"2[0-4][0-9]|25[0-5]))|(?:(?:[0-9A-Fa-f]{1,4}:"
                 r"){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:"
                 r"[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)")
