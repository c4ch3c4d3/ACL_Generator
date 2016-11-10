#Generate an entry in an Alcatel ACL from command line arguments in the following form:
#Entry, Source IP, Destination IP, Protocol, Port, Fragment Status, Action 
import General_Qs
import Generators


def cli():
    #Declaration of variables used below
    new_term = True
    acl_vars = []
    entry_number = 10
    question = General_Qs.General_Questions()
    
    #One time questions for the user to answer
    #device_type = question.q_device()
    '''
    filter_name = question.q_name("filter")
    filter_number = question.q_name("filter number")
    
    #user interaction, obtain the necessary components for an ACL, calling on General_Qs to generate queries
    while new_term == True:
    
        entry_description = question.q_name("entry")
        
        protocol = question.q_protocol()

        source_ip = question.q_ip("source")
        source_service = question.q_port("source")
        
        destination_ip = question.q_ip("destination")
        destination_service = question.q_port("destination")

        action = question.q_action("alcatel")

        acl_vars.append([entry_number, entry_description, protocol, source_ip, source_service, destination_ip, destination_service, action])
        
        
        need_term = question.q_new_term()
        if need_term == "y":
            entry_number += 10
            print ""
        else:
            new_term = False
            Generators.alcatel_generator(100, filter_name, acl_vars, entry_number)
        '''

    acl_vars.append([10, 'entry', 'tcp', ['192.168.1.1/32', '192.168.1.2/32'], ['80', '443'], ['10.0.0.1/32', '10.0.0.0/8'], ['any'], 'forward'])
    acl_vars.append([20, 'entry_2', '*', ['192.18.1.1/32'], ['any'], ['any'], ['any'], 'drop'])
    acl_vars.append([30, 'entry_3', 'udp', ['192.168.1.1/32', '192.168.1.2/32'], ['80', '443'], ['8.8.8.8/10'], ['80', '443'], 'forward'])
    Generators.alcatel_generator(100, "test_filter", acl_vars, 30)

        

cli()