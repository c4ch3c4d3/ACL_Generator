# pylint: disable=C0301, C0103
from Checks import ip_check, service_check
from ipaddress import IPv4Network

#------------------------------------------------------------------------------
#                               alcatel
#------------------------------------------------------------------------------


def alcatel_filter_generator(filter_number, name, acl_vars_array, entry_number):
    # [[10, 'entry', 'tcp', ['192.168.1.1/32', '192.168.1.2/32'], ['80', '443'], ['10.0.0.1/32', '10.0.0.0/8'], ['any'], 'forward'], [20, 'entry_2', '*', ['192.18.1.1/32'], ['any'], ['any'], ['any'], 'drop']]
    """
    Generates an alcatel acl from scratch.  Requires:
    filter_number: a number for the filter, similar to a name
    filter_name: a description for the filter
    acl_vars_array: an array with all of the users input variables. An array should look like
    [entry_number, entry_description, protocol, source_ips, source_services, destination_ips, destination_services, action])

    entry_number: the amount of entries the user needs.
    """
    with open(name + ".txt", 'w') as output_file:
        alcatel_vars_fixer(name, acl_vars_array, output_file)

        output_file.write("configure filter ip-filter " +
                          str(filter_number) + " create\n")
        output_file.write("description " + str(name) + "\n")

        entry_generator(acl_vars_array, entry_number, output_file)

        output_file.write("entry 10" + str(entry_number) + " create\n")
        output_file.write("\tmatch\n")
        output_file.write("exit\n")
        output_file.write("action forward\n")
        output_file.write("exit\n\n")
        output_file.write("info\n")

    with open(name + ".txt", 'r') as output_file:
        print(output_file.read())


def alcatel_vars_fixer(name, acl_vars_array, output_file):
    """
    The following loops through our entire array, and calls list_generator.
    Additionally, it checks to see if a list has already been created for any given set of numbers
    If such a list already exists, it passes on making another list.
    x y and z are all iterators

    Accepts:
    name: name of the filter
    acl_vars_array: an array of vars for an ACL
    """

    ip_list_number = 1
    port_list_number = 1
    existing_list_names = []
    existing_list_numbers = []
    duplicate = False

    for x in range(0, len(acl_vars_array)):
        for y in range(3, 7):
            # checks for duplicates
            for z in range(0, len(existing_list_numbers)):
                duplicate = False
                if existing_list_numbers[z] == acl_vars_array[x][y]:
                    acl_vars_array[x][y] = existing_list_names[z]
                    duplicate = True
                    break
            # generates ip prefix lists or port lists based on list position.
            if len(acl_vars_array[x][y]) > 1 and y == 3 and ip_check(acl_vars_array[x][y]) is True or len(
                    acl_vars_array[x][y]) > 1 and y == 5 and ip_check(acl_vars_array[x][y]):
                existing_list_numbers.append(acl_vars_array[x][y])
                acl_vars_array[x][y] = list_generator(str(name) + "_ip_list_" + str(ip_list_number), "ip_list",
                                                      acl_vars_array[x][y], output_file)
                existing_list_names.append(
                    str(name) + "_ip_list_" + str(ip_list_number))
                ip_list_number += 1
            elif len(acl_vars_array[x][y]) > 1 and y == 4 and service_check(acl_vars_array[x][y]) is True or len(
                    acl_vars_array[x][y]) > 1 and y == 6 and service_check(acl_vars_array[x][y]) is True:
                existing_list_numbers.append(acl_vars_array[x][y])
                acl_vars_array[x][y] = list_generator(str(name) + "_port_list_" + str(port_list_number), "port_list",
                                                      acl_vars_array[x][y], output_file)
                existing_list_names.append(
                    str(name) + "_port_list_" + str(port_list_number))
                port_list_number += 1
            elif duplicate is True:
                acl_vars_array[x][y] = existing_list_names[z]
            # Strip single entry values out of their array for acl.write(ing
            else:
                acl_vars_array[x][y] = acl_vars_array[x][y][0]


def list_generator(name, kind, numbers, output_file):
    """
    Alcatels lack the capability to state multiple ips or ports in one entry.
    They can use premade lists to specify multiple items in an entry.
    This method takes the following arguments to make such a list:
    'kind': the kind of list to make, port or ip
    'numbers': the items to make the list from
    """

    LIST_STRING = {
        'ip_list': "ip-prefix-list ",
        'port_list': "port-list "
    }

    output_file.write("configure filter match-list " +
                      LIST_STRING[kind] + str(name) + " create\n")
    if kind == "ip_list":
        for ip_addr in numbers:
            output_file.write("\tprefix " + str(ip_addr) + "\n")
        output_file.write("exit\n")
        return name
    elif kind == "port_list":
        for port in numbers:
            output_file.write("\tport " + str(port) + "\n")
        output_file.write("exit\n\n")
        return name


def entry_generator(acl_vars_array, entry_number, output_file):
    """
    Generates entries for each list of variables in acl_vars_array.

    acl_vars_array: an array with all of the users input variables. An array should look like
    [entry_number, entry_description, protocol, source_ips, source_services, destination_ips, destination_services, action])

    entry_number: the amount of entries the user needs.

    """
    import pdb; pdb.set_trace()
    i = entry_number

    for i in range(0, int(i / 10)):
        output_file.write("entry " + str(acl_vars_array[i][0]) + " create\n")
        output_file.write("\tdescription " + str(acl_vars_array[i][1]) + "\n")

        if acl_vars_array[i][2] == "any":
            output_file.write("\tmatch protocol *\n")
        else:
            output_file.write("\tmatch protocol " +
                              str(acl_vars_array[i][2]) + "\n")

        j = [acl_vars_array[i][3]]
        is_title = ip_check(j)
        if is_title is False:
            output_file.write("\t\tsrc-ip ip-prefix-list " +
                              str(acl_vars_array[i][3]) + "\n")
        elif acl_vars_array[i][3] == "any":
            pass
        else:
            output_file.write("\t\tsrc-ip " + str(acl_vars_array[i][3]) + "\n")

        j = [acl_vars_array[i][4]]
        is_title = service_check(j)
        if is_title is False:
            output_file.write("\t\tsrc-port port-list " +
                              str(acl_vars_array[i][4]) + "\n")
        elif acl_vars_array[i][4] == "any":
            pass
        else:
            output_file.write("\t\tsrc-port eq " +
                              str(acl_vars_array[i][4]) + "\n")

        j = [acl_vars_array[i][5]]
        is_title = ip_check(j)
        if is_title is False:
            output_file.write("\t\tdst-ip ip-prefix-list " +
                              str(acl_vars_array[i][5]) + "\n")
        elif acl_vars_array[i][5] == "any":
            pass
        else:
            output_file.write("\t\tdst-ip " + str(acl_vars_array[i][5]) + "\n")

        j = [acl_vars_array[i][5]]
        is_title = service_check(j)
        if is_title is False:
            output_file.write("\t\tdst-port port-list " +
                              str(acl_vars_array[i][6]) + "\n")
        elif acl_vars_array[i][6] == "any":
            pass
        else:
            output_file.write("\t\tdst-port eq " +
                              str(acl_vars_array[i][6]) + "\n")

        output_file.write("\texit\n")
        output_file.write("\taction " + str(acl_vars_array[i][7]) + "\n")
        output_file.write("exit\n\n")

#------------------------------------------------------------------------------
#                               cisco
#------------------------------------------------------------------------------

def cisco_filter_generator(filter_number, name, acl_vars_array):
    """
    Provided with the variables for creating an ACL, call the correct line creator
    Note that acl_vars_array should be different depending on if it is a basic or extended ACL
    
    filter_number -- The number for the filter.  Must be an int
    name -- The name of the filter, used for the remarks
    acl_vars_array -- An array consisting the necessary variables for a Cisco ACL
    """
    
    with open(name + ".txt", 'w') as output_file:
        output_file.write("access-list %s remark %s\n" % (filter_number, name))
        
        if int(filter_number) <= 99 or int(filter_number) <= 1300 and int(filter_number) >= 1999:
            cisco_basic_line(filter_number, name, acl_vars_array, output_file)
        elif int(filter_number) >= 100 and int(filter_number) <= 199 or int(filter_number) >= 2000 and int(filter_number) <= 2699:
            cisco_extended_line()
    
    with open(name + ".txt", 'r') as output_file:
        print(output_file.read())
        
def cisco_basic_line(filter_number, name, acl_vars_array, output_file):
    """
    Create the lines for a cisco acl.
    
    filter_number -- The number for the filter.  Must be an int
    name -- The name of the filter, used for the remarks
    acl_vars_array -- An array consisting of IP/CIDR string, and actions
    output_file -- the file the function should write to
    """
    
    for i in range (0, len(acl_vars_array)):
        
        if str(acl_vars_array[i][0]) == "['any']":
            output_file.write("access-list %s %s any \n" % (filter_number, acl_vars_array[i][1]))
        else:
            ip_wildcard = cisco_ip_fixer(acl_vars_array[i][0])
            output_file.write("access-list %s %s %s %s\n" % (filter_number, acl_vars_array[i][1], ip_wildcard[0], ip_wildcard[1]))

def cisco_extended_line(filter_number, name, acl_vars_array, output_file):
    

def cisco_ip_fixer(ip_address):
    """
    Provided an ip address element from a list, 
    extracts the ip address and removes extra characters.
    
    Returns ip address, wildcard mask
    """
    
    ip_network = ip_address
    ip_network = str(ip_network)
    ip_network = ip_network.replace("'", "").replace("[", "").replace("]", "")
    ip_network = IPv4Network(ip_network)
    ip_addr = ip_network.network_address
    wildcard = ip_network.hostmask
    
    return (ip_addr, wildcard)


    
def main():
    filter_number = 123
    name = test
    acl_vars = [[10, 'entry', 'tcp', ['192.168.1.1/32', '192.168.1.2/32'], ['80', '443'], ['10.0.0.1/32', '10.0.0.0/8'], ['any'], 'forward'], [20, 'entry_2', '*', ['192.18.1.1/32'], ['any'], ['any'], ['any'], 'drop']]
    
     with open(name + ".txt", 'w') as output_file:
        output_file.write("access-list %s remark %s\n" % (filter_number, name))
        cisco_extended_line(filter_number, name, acl_vars_array, output_file)

if __name__ == '__main__':
    main()
