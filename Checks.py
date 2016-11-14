#pylint: disable=C0301
#may need to implement character check for names, as they can only have a maximum character count of 32
import re
class network_checks:

    def key_word_check(self, word, kind):
        """Provided a kind of keyword, check against a library of acceptable key words.
        Kinds accepted:
        'protocols' to check for a valid protocol
        'actions' to check for forwarding or dropping
        'yes_or_no' to check for y or n
        'device' to check for device type

        Returns true if a keyword is found
        """
        protocols = ["*", "any", "tcp", "udp", "icmp", "gre", "esp"]
        actions = ["forward", "drop", "accept", "reject"]
        yes_or_no = ["y", "n", "Y", "N", "yes", "no"]
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
        """Provided a string, ensure its formated as an ip address
        Ex. 192.168.1.1/32

        Returns true if a correctly formatted IP is found
        """
        self.ip_addr = ip_addr

        #regex checking for an ip address in the EXACT format: ###.###.###.###/##  Anything else will be rejected
        valid_ip = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(?:3[0-2]|2[0-9]|1[0-9]|[0-9]?)$")
        try:
            if valid_ip.search(ip_addr) is not None or ip_addr == "any":
                return True
            else:
                return False
        except:
            for ip in ip_addr:
                if valid_ip.search(ip) is not None or ip == "any":
                    pass
                else:
                    return False
            return True

    def service_check(self, service):
        """
        Provided a string, determine if it is a digit. If it is, ensure it is between 0 & 65535
        Returns true if an int within range is found
        """
        self.service = service
        for port in service:
            if port.isdigit() is True:
                if (int(port) <= 65535) and (int(port) > 0):
                    pass
            elif service[0] == "any" or service == "any":
                return True
            else:
                return False
        return True

    def space_check(self, name):
        """Checks for spaces."""
        self.name = name

        #regex search for a space
        valid_name = re.compile(' ')
        return bool(valid_name.search(name) is None)

    def length_check(self, name):
        "Checks input ensure it is less than 30 characters"
        self.name = name
        if len(name) <= 20:
            return True
        else:
            return False
