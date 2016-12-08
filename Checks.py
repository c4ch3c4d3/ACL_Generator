# pylint: disable=C0301
# may need to implement character check for names, as they can only have a
# maximum character count of 32
import re
from ipaddress import IPv4Network


def key_word_check(word, kind):
    """Provided a kind of keyword, check against a library of acceptable key words.
    Kinds accepted:
    'protocols' to check for a valid protocol
    'actions' to check for forwarding or dropping
    'yes_or_no' to check for y or n
    'device' to check for device type

    Returns true if a keyword is found
    """
    protocols = ["*", "any", "ip", "tcp", "udp", "icmp", "gre", "esp"]
    actions = ["forward", "drop", "accept", "reject", "permit", "deny"]
    yes_or_no = ["y", "n", "Y", "N", "yes", "no"]
    device = ["a", "c", "j", "alcatel", "juniper", "cisco"]

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

def ip_check(ip_addr):
    """
    Provided an array, ensure all its elements are valid network addresses
    Ex. 192.168.1.1/32 or 192.168.1.0/24

    Returns true if a correctly formatted IP is found
    """
    if type(ip_addr) is str:
        try:
            if ip_addr == "any":
                return True
            else:
                #IPv4Network, provided a string in the format "###.###.###.###/##" will return a network object.
                #We only use it to ensure that a string is a valid network object, otherwise an error will occur and be excepted
                IPv4Network(ip_addr)
                return True
        except ValueError:
            return False
                
    elif type(ip_addr) is list:
        for i in ip_addr:
            try:
                if i == "any":
                    return True
                else:
                    IPv4Network(i)
                    return True
            except ValueError:
                return False


def service_check(service):
    """
    Provided a string, determine if it is a digit. If it is, ensure it is between 0 & 65535
    Returns true if an int within range is found
    """
    #Used when passed a string
    if type(service) is str:
        if service.isdigit() is True:
            if (int(service) <= 65535) and (int(service) > 0):
                pass
        elif service == "any":
            return True
        else:
            return False

    #Used when passed a list
    elif type(service) is list:
        for port in service:
            if port.isdigit() is True:
                if (int(port) <= 65535) and (int(port) > 0):
                    pass
            elif service[0] == "any" or service == "any":
                return True
            else:
                return False
        return True


def space_check(name):
    """Checks for spaces."""

    # regex search for a space
    valid_name = re.compile(' ')
    return bool(valid_name.search(name) is None)


def length_check(name):
    "Checks input ensure it is less than 30 characters"
    if len(name) <= 20 and len(name) > 0:
        return True
    else:
        return False
