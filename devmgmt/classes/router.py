from classes.networkdevice import NetworkDevice

class RouterPort:
    def __init__(self, mac, ip, mask, is_up, is_switchport, is_trunk,):
        self.idnum = idnum
        self.snr = serialnum

    def __str__(self):
        returnval = "idnum=" + str(self.idnum) + ",serialnum=" + self.snr
        return returnval



class Router(NetworkDevice):
    def __init__(self, idnum, serialnum, macaddress, ipaddress, ip_subnetmask, ):
        super().__init__(idnum, serialnum, macaddress, ipaddress)
        self.numports = numports

    def __str__(self):
        returnval = "idnum=" + str(self.idnum) + ",serialnum=" + self.snr + ",mac=" + self.mac + ",ip=" + self.ip + ",numports=" + str(self.numports)
        return returnval

