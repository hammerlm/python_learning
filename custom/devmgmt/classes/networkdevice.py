from classes.device import Device

class NetworkDevice(Device):
    def initPortCollection(self, numports):
        for x in range(numports):
            self.ports["pt" + str(x)] = ""
            
    def __init__(self, idnum, serialnum, sys_macaddress, man_ipaddress, ip_subnetmask, hostname, numports):
        super().__init__(idnum, serialnum)
        self.sys_mac=sys_macaddress
        self.man_ip=man_ipaddress
        self.ip_subnetmask=ip_subnetmask
        self.hostname = hostname
        self.numports = numports
        self.ports = {}
        self.initPortCollection(numports)    

    def __str__(self):
        returnval = super().__str__() + ",name=" + self.hostname + ",mac=" + self.sys_mac + ",ip=" + self.man_ip + ",mask=" + self.ip_subnetmask + ",numports=" + str(self.numports)
        return returnval

