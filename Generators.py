#pylint: disable=C0301, C0103
import Checks

def alcatel_generator(filter_number, name, acl_vars_array, entry_number):
    #[[10, 'entry', 'tcp', ['192.168.1.1/32', '192.168.1.2/32'], ['80', '443'], ['10.0.0.1/32', '10.0.0.0/8'], ['any'], 'forward'], [20, 'entry_2', '*', ['192.18.1.1/32'], ['any'], ['any'], ['any'], 'drop']]
    """
    Generates an alcatel acl.  Requires:
    filter_number: a number for the filter, similar to a name
    filter_name: a description for the filter
    acl_vars_array: an array with all of the users input variables. An array should look like
    [entry_number, entry_description, protocol, source_ips, source_services, destination_ips, destination_services, action])

    entry_number: the amount of entries the user needs.
    """
    #variable initialization
    check = Checks.network_checks()
    ip_list_number = 1
    port_list_number = 1
    existing_list_names = []
    existing_list_numbers = []
    duplicate = False
    is_title = False

    #The following loops through our entire array, and calls list_generator.
    #Additionally, it checks to see if a list has already been created for any given set of numbers
    #If such a list already exists, it passes on making another list.
    #x y and z are all iterators
    for x in range(0, len(acl_vars_array)):
        for y in range(3, 7):
            #checks for duplicates
            for z in range(0, len(existing_list_numbers)):
                duplicate = False
                if existing_list_numbers[z] == acl_vars_array[x][y]:
                    acl_vars_array[x][y] = existing_list_names[z]
                    duplicate = True
                    break
            #generates ip prefix lists or port lists based on list position.
            if len(acl_vars_array[x][y]) > 1 and y == 3 and check.ip_check(acl_vars_array[x][y]) is True or len(acl_vars_array[x][y]) > 1 and y == 5 and check.ip_check(acl_vars_array[x][y]):
                existing_list_numbers.append(acl_vars_array[x][y])
                acl_vars_array[x][y] = list_generator(str(name) + "_ip_list_" + str(ip_list_number), "ip_list", acl_vars_array[x][y])
                existing_list_names.append(str(name) + "_ip_list_" + str(ip_list_number))
                ip_list_number += 1
            elif len(acl_vars_array[x][y]) > 1 and y == 4 and check.service_check(acl_vars_array[x][y]) is True or len(acl_vars_array[x][y]) > 1 and y == 6 and check.service_check(acl_vars_array[x][y]) is True:
                existing_list_numbers.append(acl_vars_array[x][y])
                acl_vars_array[x][y] = list_generator(str(name) + "_port_list_" + str(port_list_number), "port_list", acl_vars_array[x][y])
                existing_list_names.append(str(name) + "_port_list_" + str(port_list_number))
                port_list_number += 1
            elif duplicate is True:
                acl_vars_array[x][y] = existing_list_names[z]
            #Strip single entry values out of their array for printing
            else:
                acl_vars_array[x][y] = acl_vars_array[x][y][0]

    print "configure filter ip-filter " + str(filter_number) + " create"
    print ""
    print "description " + str(name)
    print ""

    i = entry_number
    for i in range(0, i/10, 1):
        print "entry " + str(acl_vars_array[i][0]) + " create"
        print "\tdescription " + str(acl_vars_array[i][1])
        if acl_vars_array[i][2] == "any":
            print "\tmatch protocol *"
        else:
            print "\tmatch protocol " + str(acl_vars_array[i][2])

        is_title = check.ip_check(str(acl_vars_array[i][3]))
        if is_title is False:
            print "\t\tsrc-ip ip-prefix-list " + str(acl_vars_array[i][3])
        elif acl_vars_array[i][3] == "any":
            pass
        else:
            print "\t\tsrc-ip " + str(acl_vars_array[i][3])

        is_title = check.service_check(str(acl_vars_array[i][4]))
        if is_title is False:
            print "\t\tsrc-port port-list " + str(acl_vars_array[i][4])
        elif acl_vars_array[i][4] == "any":
            pass
        else:
            print "\t\tsrc-port eq " + str(acl_vars_array[i][4])

        is_title = check.ip_check(str(acl_vars_array[i][5]))
        if is_title is False:
            print "\t\tdst-ip ip-prefix-list " + str(acl_vars_array[i][5])
        elif acl_vars_array[i][5] == "any":
            pass
        else:
            print "\t\tdst-ip " + str(acl_vars_array[i][5])

        is_title = check.service_check(str(acl_vars_array[i][6]))
        if is_title is False:
            print "\t\tdst-port port-list " + str(acl_vars_array[i][6])
        elif acl_vars_array[i][6] == "any":
            pass
        else:
            print "\t\tdst-port eq " + str(acl_vars_array[i][6])

        print "\texit"
        print "\taction " + str(acl_vars_array[i][7])
        print "exit"
        print ""

    print "entry 10" + str(entry_number) + " create"
    print "\tmatch"
    print "exit"
    print "action forward"
    print "exit"
    print ""
    print "info"

def list_generator(name, kind, numbers):
    """
    Alcatels lack the capability to state multiple ips or ports in one entry.
    They can use premade lists to specify multiple items in an entry.
    This method takes the following arguments to make such a list:
    'kind': the kind of list to make, port or ip
    'numbers': the items to make the list from
    """

    LIST_STRING = {
        'ip_list' : "ip-prefix-list ",
        'port_list' : "port-list "
    }

    print "configure filter match-list " + LIST_STRING[kind] + str(name) + " create"
    if kind == "ip_list":
        for ip_addr in numbers:
            print "\tprefix " + str(ip_addr)
        print "exit"
        print ""
        return name
    elif kind == "port_list":
        for port in numbers:
            print "\tport " + str(port)
        print "exit"
        print ""
        return name
