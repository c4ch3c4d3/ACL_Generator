#pylint: disable=C0301
import Checks
import Generators

class General_Questions():


    check = Checks.network_checks()
    valid_input = False
    #Variables of strings used modularly in the below questions.  May need to be changed to dicts as we work on multiple types of routers
    POLITE_STRING = "Please specify a "
    INVALID_STRING = " is invalid. Specify a valid "
    DEVICE_STRINGS = {
        'general' : 'platform, aclatel (a), cisco (c), or juniper (j): ',
        'invalid' : 'platform using a, c, or j: '
    }
    NAME_STRINGS = {
        'descriptor': ' (use _ for spaces): ',
        'entry' : 'description for this entry, using underscores (_) for spaces: ',
        'filter' : 'description for this filter, using underscores (_) for spaces: '
    }

    PROTOCOL_STRINGS = {
        'general': 'protocol or [any]: ',
        'invalid' : 'protocol (tcp, udp, icmp, gre, esp) or [any]: '
    }
    IP_STRINGS = [
        " IP/CIDR or [any].  You can also provide multiple IP/CIDRs, seperated by a comma: ",
        " IP/CIDR in the form of #.#.#.#/# or [any].  Multiple IP/CIDRs must ALL be correclty formatted, or they will be rejected: "
        ]
    PORT_STRINGS = [
        " port or [any]: ",
        " port between 1-65535 or [any]: "
    ]
    ACTION_STRINGS = {
        'general': 'action, forward/[drop]: ',
        'alcatel' : 'drop',
        'juniper' : "reject"
    }
    NEW_TERM_STRINGS = {
        'general' : 'Do you need another term? y/[n]: ',
        'invalid' : 'input, y/[n]: '
    }




    #Methods for each type of information we need to query. There is almost certaintly a way to combine all of these into one function that requires more inputs, but this is easier for now)
    #Each method follows the same general logic: Ask for input, call the appropriate checking function in Checks.network_checks, and ask the user again if the check returns false


    def q_name(self, kind):
        self.name = raw_input(self.POLITE_STRING + self.NAME_STRINGS[kind])
        self.is_true = self.check.space_check(self.name)
        self.valid_input = False

        while self.valid_input is False:
            if self.is_true == True:
                return self.name
            else:
                self.name = raw_input(str(self.name) + self.INVALID_STRING + self.NAME_STRINGS[kind])
                self.is_true = self.check.space_check(self.name)

    def q_ip(self, kind):
        self.ip_addr = raw_input(self.POLITE_STRING + str(kind) + self.IP_STRINGS[0] ) or "any"
        self.ip_addr = self.ip_addr.replace(' ','')
        self.ip_addr = self.ip_addr.split(',')
        self.is_true = self.check.ip_check(self.ip_addr)
        self.valid_input = False

        while self.valid_input is False:
            if self.is_true == True:
                return self.ip_addr
            else:
                self.ip_addr = raw_input(str(self.ip_addr) + self.INVALID_STRING + str(kind) + self.IP_STRINGS[1] ) or "any"
                self.is_true = self.check.ip_check(self.ip_addr)


    def q_port(self, kind):
        self.service = raw_input(self.POLITE_STRING + str(kind) + self.PORT_STRINGS[0] ) or "any"
        self.service = self.service.replace(' ','')
        self.service = self.service.split(',')
        self.is_true = self.check.service_check(self.service)
        self.valid_input = False

        while self.valid_input is False:
            if self.is_true == True:
                return self.service
            else:
                self.service = raw_input(str(self.service) + self.INVALID_STRING + str(kind) + self.PORT_STRINGS[1] ) or "any"
                self.is_true = self.check.service_check(self.service)

    def q_protocol(self):
        self.protocol = raw_input(self.POLITE_STRING + self.PROTOCOL_STRINGS['general']) or "*"
        self.is_true = self.check.key_word_check(self.protocol, "protocol")
        self.valid_input = False

        while self.valid_input is False:
            if self.is_true == True:
                return self.protocol
            else:
                self.protocol = raw_input(str(self.protocol) + self.INVALID_STRING + self.PROTOCOL_STRINGS['invalid']) or "*"
                self.is_true = self.check.key_word_check(self.protocol, "protocol")


    def q_action(self, kind):
        self.action = raw_input(self.POLITE_STRING + str(self.ACTION_STRINGS['general'])) or self.ACTION_STRINGS[kind]
        self.is_true = self.check.key_word_check(self.action, "action")
        self.valid_input = False

        while self.valid_input is False:
            if self.is_true == True:
                return self.action
            else:
                self.action = raw_input(str(self.action) + self.INVALID_STRING + str(self.ACTION_STRINGS['general'])) or self.ACTION_STRINGS[kind]
                self.is_true = self.check.key_word_check(self.action, "action")

    def q_new_term(self):
        self.new = raw_input(self.POLITE_STRING + self.NEW_TERM_STRINGS['general']) or "n"
        self.is_true = self.check.key_word_check(self.new, "y_or_n")
        self.valid_input = False

        while self.valid_input is False:
            if self.is_true == True:
                return self.new
            else:
                self.new = raw_input(str(self.new) + self.INVALID_STRING + str(self.NEW_TERM_STRINGS['invalid'])) or "n"
                self.is_true = self.check.key_word_check(self.new, "y_or_n")

    def q_device(self):
        self.device = raw_input(self.POLITE_STRING + self.DEVICE_STRINGS['general'])
        self.is_true = self.check.key_word_check(self.device, "device")
        self.valid_input = False

        while self.valid_input is False:
            if self.is_true == True:
                return self.device
            else:
                self.device = raw_input(str(self.device) + self.INVALID_STRING + str(self.DEVICE_STRINGS['invalid']))
                self.is_true = self.check.key_word_check(self.device, "device")
