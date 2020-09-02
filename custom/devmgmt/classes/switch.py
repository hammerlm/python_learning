from classes.networkdevice import NetworkDevice

class SwitchPort:
    def __init__(self, mac, is_trunk, native_vlan):
        self.mac = mac
        self.is_trunk = is_trunk
        self.native_vlan = native_vlan

    def getDict(self):
        returnval = {"mac" : self.mac, "is_trunk" : self.is_trunk, "native_vlan" : self.native_vlan}
        return returnval

    def __str__(self):
        returnval = "mac=" + self.mac + ",is_trunk=" + str(self.is_trunk) + ",n_vlan=" + str(self.native_vlan)
        return returnval

class Switch(NetworkDevice):
    def initSwitchPortCollection(self):
        for key in self.ports:
            self.ports[key] = SwitchPort("0000.0000.0000", False, 1)
    
    def __init__(self, idnum, serialnum, sys_macaddress, man_ipaddress, ip_subnetmask, hostname, numports):
        super().__init__(idnum, serialnum, sys_macaddress, man_ipaddress, ip_subnetmask, hostname, numports)
        self.initSwitchPortCollection()

    def __str__(self):
        returnval = super().__str__()
        return returnval
    
    def getObjectWithPorts_asString(self):
        returnval = self.__str__() + "\nList of ports:\n"
        for key in self.ports:
            returnval = returnval + str(key) + "==>" + self.ports[key].__str__() + "\n"
        return returnval

    def getPortsAsDict(self):
        returnval = {}
        for switchport_key in self.ports:
            returnval[switchport_key] = self.ports[switchport_key].getDict()
        return returnval

