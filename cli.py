#pylint: disable=C0301
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

    filter_number = question.q_name("number")
    filter_name = question.q_name("filter")
    print ""

    #user interaction, obtain the necessary components for an ACL, calling on General_Qs to generate queries
    while new_term is True:

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
            print ""
            new_term = False
            Generators.alcatel_filter_generator(filter_number, filter_name, acl_vars, entry_number)

cli()