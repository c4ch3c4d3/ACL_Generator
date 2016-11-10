#Prompt users for arguments, call on the specified router (assuming its supported), hand off ACL generation to the required script

import Alcatel
def main():
    userdevice = "none"
    userdevice = raw_input(prompt = "Select Alcatel (a), Cisco (c), or Juniper (j)")
    extras = raw_input(prompt = "Do you require device specific features? y/n [n]") or "n"
    if extras == "n":
        source = raw_input(prompt = "Specify a source IP/CIDR [any]") or "any"
        destination = raw_input(prompt = "Specify a destination IP/CIDR [any]") or "any"
        service = raw_input(prompt = "Specify a service by port number [any]") or "any"
        action = raw_input(prompt = "Specify an action ")
    else:
        if userdevice == "Alcatel" or userdevice == "a":
            Alcatel
        elif userdevice == "Cisco" or userdevice == "c":
            pass
        elif userdevice == "Juniper" or userdevice == "j":
            pass
        else:
            print "Please type Alcatel (a), Juniper (j), or Cisco (c)"
            main()
main