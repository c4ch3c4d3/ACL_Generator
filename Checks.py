#pylint: disable=C0301
import re
class network_checks:

    def key_word_check(self, word, kind):
        protocols = ["*", "any", "tcp", "udp", "icmp", "gre", "esp"]
        actions = ["forward", "drop", "accept", "reject"]
        yes_or_no = ["y", "n"]
        device = ["a,", "c", "j", "alcatel", "juniper", "cisco"]

        if kind == "protocol":
            if word in protocols:
                return True
            else:
                return False
        elif kind == "action":
            if word in actions:
                return True
            else:
                return False
        elif kind == "y_or_n":
            if word in yes_or_no:
                return True
            else:
                return False
        elif kind == "device":
            if word in device:
                return True
            else:
                return False


    def ip_check(self, ip_addr):
    #Provided a string of text, ensure it is a valid IP/CIDR for our Alcatel device.
        self.ip_addr = ip_addr

        #regex checking for an ip address in the EXACT format: ###.###.###.###/##  Anything else will be rejected  NOTE: messes up on 1.1.1.1/33 due to a match of everything before the last 3.
        valid_ip = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(?:3[0-2]|2[0-9]|1[0-9]|[0-9]?)$")

        for ip in ip_addr:
            if valid_ip.search(ip) is not None:
                pass
            elif ip == "any":
                pass
            else:
                return False
        return True

    def service_check(self, service):
    #Provided a string, determine if it is a valid port, or "any".  Return result as a string
        self.service = service
        #check if the input is a digit. If it is, ensure its within our valid port range (0-65535)
        #import pdb; pdb.set_trace()
        for port in service:
            if port.isdigit() is True:
                if (int(port) <= 65535) and (int(port) > 0):
                    pass
            elif service[0] == "any":
                return True
            else:
                return False
        return True

    def space_check(self, name):
        self.name = name

        valid_name = re.compile(' ')
        if valid_name.search(name) is None:
            return True
        else:
            return False
