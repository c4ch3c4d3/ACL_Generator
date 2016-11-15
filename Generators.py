#pylint: disable=C0301, C0103
import Checks

def alcatel_filter_generator(filter_number, name, acl_vars_array, entry_number):
    #[[10, 'entry', 'tcp', ['192.168.1.1/32', '192.168.1.2/32'], ['80', '443'], ['10.0.0.1/32', '10.0.0.0/8'], ['any'], 'forward'], [20, 'entry_2', '*', ['192.18.1.1/32'], ['any'], ['any'], ['any'], 'drop']]
    """
    Generates an alcatel acl from scratch.  Requires:
    filter_number: a number for the filter, similar to a name
    filter_name: a description for the filter
    acl_vars_array: an array with all of the users input variables. An array should look like
    [entry_number, entry_description, protocol, source_ips, source_services, destination_ips, destination_services, action])

    entry_number: the amount of entries the user needs.
    """
    #import pdb; pdb.set_trace()
    with open(name + ".txt", 'w') as acl:
        alcatel_vars_fixer(name, acl_vars_array, acl)

        acl.write("configure filter ip-filter " + str(filter_number) + " create\n")
        acl.write("description " + str(name) + "\n")

        entry_generator(acl_vars_array, entry_number, acl)

        acl.write("entry 10" + str(entry_number) + " create\n")
        acl.write("\tmatch\n")
        acl.write("exit\n")
        acl.write("action forward\n")
        acl.write("exit\n\n")
        acl.write("info\n")
    
    with open(name + ".txt", 'r') as acl:
        print acl.read()    
    
def alcatel_vars_fixer(name, acl_vars_array, file):
    """
    The following loops through our entire array, and calls list_generator.
    Additionally, it checks to see if a list has already been created for any given set of numbers
    If such a list already exists, it passes on making another list.
    x y and z are all iterators

    Accepts:
    name: name of the filter
    acl_vars_array: an array of vars for an ACL
    """
    check = Checks.network_checks()
    ip_list_number = 1
    port_list_number = 1
    existing_list_names = []
    existing_list_numbers = []
    duplicate = False


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
                acl_vars_array[x][y] = list_generator(str(name) + "_ip_list_" + str(ip_list_number), "ip_list", acl_vars_array[x][y], file)
                existing_list_names.append(str(name) + "_ip_list_" + str(ip_list_number))
                ip_list_number += 1
            elif len(acl_vars_array[x][y]) > 1 and y == 4 and check.service_check(acl_vars_array[x][y]) is True or len(acl_vars_array[x][y]) > 1 and y == 6 and check.service_check(acl_vars_array[x][y]) is True:
                existing_list_numbers.append(acl_vars_array[x][y])
                acl_vars_array[x][y] = list_generator(str(name) + "_port_list_" + str(port_list_number), "port_list", acl_vars_array[x][y], file)
                existing_list_names.append(str(name) + "_port_list_" + str(port_list_number))
                port_list_number += 1
            elif duplicate is True:
                acl_vars_array[x][y] = existing_list_names[z]
            #Strip single entry values out of their array for acl.write(ing
            else:
                acl_vars_array[x][y] = acl_vars_array[x][y][0]

def list_generator(name, kind, numbers, file):
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

    file.write("configure filter match-list " + LIST_STRING[kind] + str(name) + " create\n")
    if kind == "ip_list":
        for ip_addr in numbers:
            file.write("\tprefix " + str(ip_addr) + "\n")
        file.write("exit\n")
        return name
    elif kind == "port_list":
        for port in numbers:
            file.write( "\tport " + str(port) + "\n")
        file.write("exit\n\n")
        return name

def entry_generator(acl_vars_array, entry_number, file):
    """
    Generates entries for each list of variables in acl_vars_array.

    acl_vars_array: an array with all of the users input variables. An array should look like
    [entry_number, entry_description, protocol, source_ips, source_services, destination_ips, destination_services, action])

    entry_number: the amount of entries the user needs.

    """
    check = Checks.network_checks()
    i = entry_number
    
    for i in range(0, i/10, 1):
        file.write( "entry " + str(acl_vars_array[i][0]) + " create\n")
        file.write( "\tdescription " + str(acl_vars_array[i][1]) + "\n")
        
        if acl_vars_array[i][2] == "any":
            file.write("\tmatch protocol *\n")
        else:
            file.write("\tmatch protocol " + str(acl_vars_array[i][2]) + "\n")

        is_title = check.ip_check(str(acl_vars_array[i][3]))
        if is_title is False:
            file.write("\t\tsrc-ip ip-prefix-list " + str(acl_vars_array[i][3]) + "\n")
        elif acl_vars_array[i][3] == "any":
            pass
        else:
            file.write("\t\tsrc-ip " + str(acl_vars_array[i][3]) + "\n")

        is_title = check.service_check(str(acl_vars_array[i][4]))
        if is_title is False:
            file.write("\t\tsrc-port port-list " + str(acl_vars_array[i][4]) + "\n")
        elif acl_vars_array[i][4] == "any":
            pass
        else:
            file.write( "\t\tsrc-port eq " + str(acl_vars_array[i][4]) + "\n")

        is_title = check.ip_check(str(acl_vars_array[i][5]))
        if is_title is False:
            file.write( "\t\tdst-ip ip-prefix-list " + str(acl_vars_array[i][5]) + "\n")
        elif acl_vars_array[i][5] == "any":
            pass
        else:
            file.write( "\t\tdst-ip " + str(acl_vars_array[i][5]) + "\n")

        is_title = check.service_check(str(acl_vars_array[i][6]))
        if is_title is False:
            file.write( "\t\tdst-port port-list " + str(acl_vars_array[i][6]) + "\n")
        elif acl_vars_array[i][6] == "any":
            pass
        else:
            file.write( "\t\tdst-port eq " + str(acl_vars_array[i][6]) + "\n")

        file.write("\texit\n")
        file.write("\taction " + str(acl_vars_array[i][7]) + "\n")
        file.write("exit\n\n")
    '''
    keywords = {
        'src-ip' : 'src-ip ',
        'dst-ip' : 'dst-ip ',
        'src-port' : 'src-port',
        'dst-port' : 'dst-port',
        'prefix' : 'ip-prefix-list',
        'port' : 'port-list'
    }

    for i in range(0, i/10, 1):
        for j in range (0, 7):
            src_or_dst = "src"
            if j == 0:
                file.write( "entry " + str(acl_vars_array[i][j]) + " create\n")
                file.write( "\tdescription " + str(acl_vars_array[i][1]) + "\n")
            elif j == 2:
                if acl_vars_array[i][2] == "any":
                    file.write("\tmatch protocol *\n")
                else:
                    file.write("\tmatch protocol " + str(acl_vars_array[i][j]) + "\n")
            elif j == 3 or j == 4 or j == 5 or j == 6:
                if j == 5:
                    src_or_dst = "dst"
                is_title = check.ip_check(str(acl_vars_array[i][j]))
                if acl_vars_array[i][j] == "any":
                    pass
                elif is_title is False:
                    if j == 3 or j == 5:
                        prefix_or_port = "prefix"
                    else:
                        prefix_or_port = "port"
                    file.write("\t\t" + keywords[src_or_dst] + keywords[prefix_or_port] + str(acl_vars_array[i][j]) + "\n")
                else:
                    file.write("\t\t" + keywords[src_or_dst] +  str(acl_vars_array[i][j]) + "\n")
            elif j == 7:
                file.write("\texit\n")
                file.write("\taction " + str(acl_vars_array[i][7]) + "\n")
                file.write("exit\n\n")
                        
    '''
                
        
