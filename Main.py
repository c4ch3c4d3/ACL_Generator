# pylint: disable=C0301, W0201
# Generate an entry in an Alcatel ACL from command line arguments in the following form:
# Entry, Source IP, Destination IP, Protocol, Port, Fragment Status, Action
from Generators import alcatel_filter_generator
from Checks import key_word_check, ip_check, service_check, space_check, length_check


valid_input = False
# Variables of strings used modularity in the below questions.
# May need to be changed to dicts as we work on multiple types of routers
POLITE_STRING = "Please specify a "
INVALID_STRING = " is invalid. Specify a valid "
DEVICE_STRINGS = {
    'general': 'platform, aclatel (a), cisco (c), or juniper (j): ',
    'invalid': 'platform using a, c, or j: '
}
NAME_STRINGS = {
    'descriptor': ' (use _ for spaces): ',
    'entry': 'description for this entry, using underscores (_) for spaces and less than 20 characters: ',
    'filter': 'description for this filter, using underscores (_) for spaces and less than 20 characters: ',
    'number': 'number for this filter: '
}

PROTOCOL_STRINGS = {
    'general': 'protocol or [any]: ',
    'invalid': 'protocol (tcp, udp, icmp, gre, esp) or [any]: '
}
IP_STRINGS = [
    " IP/CIDR or [any].  You can also provide multiple IP/CIDRs, separated by a comma: ",
    " IP/CIDR in the form of #.#.#.#/# or [any].  Multiple IP/CIDRs must ALL be correctly formatted, or they will be rejected: "
]
PORT_STRINGS = [
    " port or [any]: ",
    " port between 1-65535 or [any]: "
]
ACTION_STRINGS = {
    'general': 'action, forward/[drop]: ',
    'alcatel': 'drop',
    'juniper': "reject"
}
NEW_TERM_STRINGS = {
    'general': 'Do you need another term? y/[n]: ',
    'invalid': 'input, y/[n]: '
}


def main():
    # Declaration of variables used below
    new_term = True
    acl_vars = []
    entry_number = 10

    # One time questions for the user to answer
    # device_type = q_device()

    filter_number = q_name("number")
    filter_name = q_name("filter") or "acl"
    print("")

    # user interaction, obtain the necessary components for an ACL
    while new_term is True:

        entry_description = q_name("entry")

        protocol = q_protocol()

        source_ip = q_ip("source")
        source_service = q_port("source")

        destination_ip = q_ip("destination")
        destination_service = q_port("destination")

        action = q_action("alcatel")

        acl_vars.append(
            [entry_number, entry_description, protocol, source_ip, source_service, destination_ip, destination_service,
             action])

        need_term = q_new_term()
        if need_term == "y":
            entry_number += 10
            print("")
        else:
            print("")
            new_term = False
            alcatel_filter_generator(filter_number, filter_name, acl_vars, entry_number)


# Functions for each type of information we need to query. There is almost certainly a way to combine all of these
# into one function that requires more inputs, but this is easier for now. Each method follows the same general logic:
# Ask for input, call the appropriate checking function in Checks, and ask the user again if the check returns false
def q_name(kind):
    """
    Ask for various types of names. Types accepted:
    'filter', 'entry', 'number'
    """
    name = input(POLITE_STRING + NAME_STRINGS[kind])

    is_true = space_check(name)
    length = length_check(name)
    valid_input = False

    while valid_input is False:
        if is_true is True and length is True:
            return name
        else:
            name = input(str(name) + INVALID_STRING + NAME_STRINGS[kind])
            if NAME_STRINGS[kind] == "number":
                is_true = service_check(name)
            else:
                is_true = space_check(name)
                length = length_check(name)


def q_ip(kind):
    """
    Ask for a source or destination ip.  Kinds accepted:
    'source, 'destination'
    """
    ip_addr = input(POLITE_STRING + str(kind) + IP_STRINGS[0]) or "any"
    ip_addr = ip_addr.replace(' ', '')
    ip_addr = ip_addr.split(',')
    is_true = ip_check(ip_addr)
    valid_input = False

    while valid_input is False:
        if is_true is True:
            return ip_addr
        else:
            ip_addr = input(str(ip_addr) + INVALID_STRING + str(kind) + IP_STRINGS[1]) or "any"
            ip_addr = ip_addr.replace(' ', '')
            ip_addr = ip_addr.split(',')
            is_true = ip_check(ip_addr)


def q_port(kind):
    """
    Ask for a source or destination port.  Kinds accepted:
    'source, 'destination'
    """

    service = input(POLITE_STRING + str(kind) + PORT_STRINGS[0]) or "any"
    service = service.replace(' ', '')
    service = service.split(',')
    is_true = service_check(service)
    valid_input = False

    while valid_input is False:
        if is_true is True:
            return service
        else:
            service = input(
                str(service) + INVALID_STRING + str(kind) + PORT_STRINGS[1]) or "any"
            is_true = service_check(service)


def q_protocol():
    """Ask for a protocol.  Accepts no arguments"""
    protocol = input(POLITE_STRING + PROTOCOL_STRINGS['general']) or "any"
    is_true = key_word_check(protocol, "protocol")
    valid_input = False

    while valid_input is False:
        if is_true is True:
            return protocol
        else:
            protocol = input(
                str(protocol) + INVALID_STRING + PROTOCOL_STRINGS['invalid']) or "any"
            is_true = key_word_check(protocol, "protocol")


def q_action(kind):
    """Ask for an action.  Kind currently doesn't matter"""
    action = input(POLITE_STRING + str(ACTION_STRINGS['general'])) or ACTION_STRINGS[kind]
    is_true = key_word_check(action, "action")
    valid_input = False

    while valid_input is False:
        if is_true is True:
            return action
        else:
            action = input(str(action) + INVALID_STRING + str(ACTION_STRINGS['general'])) or \
                     ACTION_STRINGS[kind]
            is_true = key_word_check(action, "action")


def q_new_term():
    """Ask for a new term.  Accepts no arguments"""
    new = input(POLITE_STRING + NEW_TERM_STRINGS['general']) or "n"
    is_true = key_word_check(new, "y_or_n")
    valid_input = False

    while valid_input is False:
        if is_true is True:
            return new
        else:
            new = input(str(new) + INVALID_STRING + str(NEW_TERM_STRINGS['invalid'])) or "n"
            is_true = key_word_check(new, "y_or_n")


def q_device():
    """Ask for the type of device.  Used to determine the use of Alcatel, Cisco, or Juniper"""
    device = input(POLITE_STRING + DEVICE_STRINGS['general'])
    is_true = key_word_check(device, "device")
    valid_input = False

    while valid_input is False:
        if is_true is True:
            return device
        else:
            device = input(str(device) + INVALID_STRING + str(DEVICE_STRINGS['invalid']))
            is_true = key_word_check(device, "device")


if __name__ == '__main__':
    main()
