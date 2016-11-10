import re
class network_checks:
    
    def protocol_check(self, protocol):
        self.protocol = protocol
        protocols = ["*", "any", "tcp", "udp", "icmp", "gre", "esp"]
        
        #for i in range(0, len(protocols)):
        if protocol in protocols:
            return protocol
        else:
            protocol = raw_input("Please input a valid protocol (tcp, udp, icmp, gre, esp, [any]: ") or "*"
            protocol = self.protocol_check(protocol)
            return protocol         

         
    def ip_check(self, ip_addr):
    #Provided a string of text, ensure it is a valid IP/CIDR for our Alcatel device. 
        self.ip_addr = ip_addr
        
        #regex checking for an ip address in the EXACT format: ###.###.###.###/##  Anything else will be rejected  NOTE: messes up on 1.1.1.1/33 due to a match of everything before the last 3.
        valid_ip = re.compile(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(?:3[0-2]|2[0-9]|1[0-9]|[0-9]?)$")
        
        if valid_ip.search(ip_addr) is not None:
            #import pdb; pdb.set_trace()
            return ip_addr
        elif ip_addr == "any":
            return ip_addr
        else:
            ip_addr = raw_input(ip_addr + " is invalid. Please specify a valid IP/CIDR in the format #.#.#.#/# or [any]: ") or "any"
            ip_addr = self.ip_check(ip_addr)
            return ip_addr
    
    
    def service_check(self, service):
    #Provided a string, determine if it is a valid port, or "any".  Return result as a string
        self.service = service
        #check if the input is a digit. If it is, ensure its within our valid port range (0-65535)
        if service.isdigit() is True:
            if (int(service) <= 65535) and (int(service) > 0):
                return str(service)
            else:
                service = raw_input(str(service) + " is invalid.  Please specify a valid IP port or [any]: ") or "any"
                service = self.service_check(service)
        
        #Ensure the string is "any", protecting the user from self idiocy
        else:
            if service == "any":
                return service
            else:
                service = raw_input(str(service) +" is invalid.  Please specify a valid IP port or [any]: ") or "any"
                service = self.service_check(service)
    
    def space_check(self, name):
        self.name = name
        
        valid_name = re.compile(' ')
        if valid_name.search(name) is None:
            return name
        else:
            name = raw_input(str(name) + " is invalid, use the underscore character instead of spaces: ")
            name = self.space_check(name)
            return name 