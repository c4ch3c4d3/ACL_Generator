import Checks

def alcatel_generator(filter_number, name, acl_vars_array, entry_number):
    #acl_vars.append([entry_number, entry_description, protocol, source_ip, source_service, destination_ip, destination_service, action])
    #[[10, 'entry', 'tcp', ['192.168.1.1/32', '192.168.1.2/32'], ['80', '443'], ['10.0.0.1/32', '10.0.0.0/8'], ['any'], 'forward'], [20, 'entry_2', '*', ['192.18.1.1/32'], ['any'], ['any'], ['any'], 'drop']]
    check = Checks.network_checks()

    ip_list_number = 1
    port_list_number = 1
    existing_list_names = []
    existing_list_numbers = []
    
    for x in range(0, len(acl_vars_array)):
        for y in range(3, 7):
            for z in range(0, len(existing_list_numbers)):
                if existing_list_numbers[z] == acl_vars_array[x][y]:
                    acl_vars_array[x][y] = existing_list_names[z]
                    continue
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
            else:
                acl_vars_array[x][y] = acl_vars_array[x][y][0]

    print "configure filter ip-filter " + str(filter_number)
    print ""
    print "description " + str(name)
    print ""

    i = entry_number
    for i in range(0, i/10, 1):
        print "entry " + str(acl_vars_array[i][0]) + " create"
        print "\tdescription " + str(acl_vars_array[i][1])
        print "\tmatch protocol " + str(acl_vars_array[i][2])
        
        if check.ip_check(str(acl_vars_array[i][3])) is False:
            print "\t\tsrc-ip ip-prefix-list " + str(acl_vars_array[i][3])
        else:
            print "\t\tsrc-ip " + str(acl_vars_array[i][3])
            
        if check.service_check(str(acl_vars_array[i][4])) is False:
            print "\t\tsrc-port port-list " + str(acl_vars_array[i][4])
        else:
            print "\t\tsrc-port eq " + str(acl_vars_array[i][4])
            
        if check.ip_check(str(acl_vars_array[i][5])) is False:
            print "\t\tdst-ip ip-prefix-list " + str(acl_vars_array[i][5])
        else:
            print "\t\tdst-ip " + str(acl_vars_array[i][5])
            
        if check.service_check(str(acl_vars_array[i][6])) is False:
            print "\t\tdst-port port-list " + str(acl_vars_array[i][6])
        else:
            print "\t\tdst-port eq " + str(acl_vars_array[i][6])
            
        print "\texit"
        print "\taction " + str(acl_vars_array[i][7])
        print "exit"
        print ""
        
    print "entry 10" + str(entry_number)
    print "\tmatch"
    print "exit"
    print "action forward"
    print ""
    
def list_generator(name, kind, numbers):
    LIST_STRING = {
        'ip_list' : "ip-prefix-list ",
        'port_list' : "port-list "
    }
    
    print "configure filter match-list " + LIST_STRING[kind] + str(name)
    for k in kind:
        if kind == "ip_list":
            for ip in numbers:
                print "\tprefix " + str(ip)
            print "exit"
            print ""
            return name   
        elif kind == "port_list":
            
            for port in numbers:
                print "\tport " + str(port)
            print "exit"
            print ""
            return name