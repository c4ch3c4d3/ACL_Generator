# pylint: disable=C0301, W0201
# Generate an entry in an Alcatel ACL from command line arguments in the following form:
# Entry, Source IP, Destination IP, Protocol, Port, Fragment Status, Action
from Generators import alcatel_filter_generator, cisco_filter_generator
from Checks import key_word_check, ip_check, service_check, space_check, length_check

valid_input = False
# Variables of strings used modularity in the below questions.
# May need to be changed to dicts as we work on multiple types of routers
POLITE_STRING = "Please specify a "
INVALID_STRING = " is invalid. Specify a valid "
DEVICE_STRINGS = {
    'general': 'platform, alcatel (a), cisco (c), or juniper (j): ',
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

IP_STRINGS = {
    'single' : ' IP/CIDR network or [any]: ',
    'single error' : 'single IP/CIDR network formatted as #.#.#.#/# or [any]: ',
    'multiple' : ' IP/CIDR network or [any].  Seperate multiples with commas: ',
    'multiple error' : 'IP/CIDR network formatted as #.#.#.#/# or [any].  All elements must be correct to be accepted: '
}


PORT_STRINGS = [
    " port or [any]: ",
    " port between 1-65535 or [any]: "
]
ACTION_STRINGS = {
    'alcatel': 'action, forward | [drop]: ',
    'cisco': 'action, permit | [deny]: ',
    'juniper': "reject"
}
NEW_TERM_STRINGS = {
    'general': 'Do you need another term? y | [n]: ',
    'invalid': 'input, y | [n]: '
}


def main():
    """
    Initiates the program. Asks for device kind, and calls the appropriate device method
    """
    device_type = q_device()
    if str(device_type) == "a" or str(device_type) == "alcatel":
        alcatel()
    elif str(device_type) == "j" or str(device_type) == "juniper":
        pass
    elif str(device_type) == "c" or str(device_type) == "cisco":
        cisco()

def alcatel():
    """
    Alcatel ACL generation.  
    """
    
    entry_number = 10
    acl_vars = []
    filter_number = q_name("number")
    filter_name = q_name("filter") or "acl"
    print("")
    need_term = "y"
    
    while need_term == "y":
        acl_vars.append(all_device_questions("alcatel", entry_number))
        need_term = q_new_term()
        print("")
        if need_term == "y":
            entry_number += 10

    alcatel_filter_generator(filter_number, filter_name, acl_vars, entry_number)

def cisco():
    """
    Cisco ACL generation.  Distinguishes between basic and extended using the user provided filter number.
    """
    
    acl_vars = []
    need_term = "y"
 
    filter_number = q_name("number")
    filter_name = q_name("filter") or "acl"
    
    if int(filter_number) <= 99 or int(filter_number) <= 1300 and int(filter_number) >= 1999:
        while need_term == "y":
            source_ip = q_ip("", "single")
            action = q_action("cisco")
            acl_vars.append([source_ip, action])
            need_term = q_new_term()
            
            if need_term == "y":
                print("")
            else:
                print("")
                need_term = "n"
                cisco_filter_generator(filter_number, filter_name, acl_vars)

            
    elif int(filter_number) >= 100 and int(filter_number) <= 199 or int(filter_number) >= 2000 and int(filter_number) <= 2699:
        while need_term == "y":
            acl_vars.append(all_device_questions("cisco"))
            need_term = q_new_term()
        cisco_filter_generator(filter_number, filter_name, acl_vars)


def all_device_questions(kind, *entry_number):
    acl_vars = []

    if kind == "alcatel":
        entry_number = entry_number[0]
        acl_vars.append(entry_number)
        acl_vars.append(q_name("entry"))

    acl_vars.append(q_protocol())
    acl_vars.append(q_ip("source"))
    acl_vars.append(q_port("source"))
    acl_vars.append(q_ip("destination"))
    acl_vars.append(q_port("destination"))
    acl_vars.append(q_action(kind))
    return acl_vars


# Functions for each type of information we need to query. There is almost certainly a way to combine all of these
# into one function that requires more inputs, but this is easier for now. Each method follows the same general logic:
# Ask for input, call the appropriate checking function in Checks, and ask
# the user again if the check returns false
def q_name(kind):
    """
    Ask for various kinds of names. Kinds accepted:
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

def q_ip(kind, basic = None):
    """
    Ask for a source or destination ip.  
    Kinds -- 'source', 'destination'
    device -- 'alcatel', 'cisco', 'juniper'
    """
    if basic is not None:
        m_or_s = "single"
    else:
        m_or_s = "multiple"
    
    if m_or_s == "multiple":
        ip_addr = input(POLITE_STRING + str(kind) + IP_STRINGS['multiple']) or "any"
        ip_addr = ip_addr.replace(' ', '')
        ip_addr = ip_addr.split(',')
        is_true = ip_check(ip_addr)
    elif m_or_s == "single":
        ip_addr = input(POLITE_STRING + str(kind) + IP_STRINGS['single']) or "any"
        ip_addr = ip_addr.replace(' ', '')
        ip_addr = ip_addr.split(',')
        if len(ip_addr) == 1:
            is_true = ip_check(ip_addr)
        else:
            is_true = False
        
    valid_input = False

    while valid_input is False:
        if is_true is True:
            return ip_addr
        else:
            if m_or_s == "multiple":
                ip_addr = input(str(ip_addr) + INVALID_STRING + str(kind) + IP_STRINGS['multiple error']) or "any"
                ip_addr = ip_addr.replace(' ', '')
                ip_addr = ip_addr.split(',')
                is_true = ip_check(ip_addr)
            elif m_or_s == "single":
                ip_addr = input(POLITE_STRING + str(kind) + IP_STRINGS['single error']) or "any"
                ip_addr = ip_addr.replace(' ', '')
                ip_addr = ip_addr.split(',')
                if len(ip_addr) == 1:
                    is_true = ip_check(ip_addr)
                else:
                    is_true = False

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
    """
    Ask for an action.
    Accepts the following kinds: alcatel, cisco, juniper
    
    """
    
    DROP_KINDS = {'alcatel': 'drop', 'juniper': 'reject', 'cisco': 'deny'}
    action = input(POLITE_STRING +
                   str(ACTION_STRINGS[kind])) or DROP_KINDS[kind]
    is_true = key_word_check(action, "action")
    valid_input = False

    while valid_input is False:
        if is_true is True:
            return action
        else:
            action = input(str(action) + INVALID_STRING + str(ACTION_STRINGS[kind])) or DROP_KINDS[kind]
            is_true = key_word_check(action, "action")


def q_new_term():
    """Ask for a new term.  Accepts no arguments"""
    new = input(NEW_TERM_STRINGS['general']) or "n"
    is_true = key_word_check(new, "y_or_n")
    valid_input = False

    while valid_input is False:
        if is_true is True:
            return new
        else:
            new = input(str(new) + INVALID_STRING +
                        str(NEW_TERM_STRINGS['invalid'])) or "n"
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
