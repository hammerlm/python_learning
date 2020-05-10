import pickle
import json

class IOSupporter:
    def __init__(self, filename):
        self.filename = filename
        
    def loadDevices(self):
        with open(self.filename, 'rb') as rfile:
            loaded_switchobjList = pickle.load(rfile)
            return loaded_switchobjList

    def loadDevicesJSON(self):
        return False
        
        #self.sys_mac=sys_macaddress
        #self.man_ip=man_ipaddress
        #self.ip_subnetmask=ip_subnetmask
        #self.hostname = hostname
        #self.numports = numports
        #self.ports = {}
        #self.initPortCollection(numports) 
    def writeDevicesJSON(self, switchobjList):
        adapted_switchobj_list = list()
        for switch in switchobjList:
            switch_to_add = {
                "id": switch.idnum, 
                "snum": switch.snr, 
                "sys_mac": switch.sys_mac, 
                "man_ip": switch.man_ipaddress, 
                "ip_subnetmask": switch.ip_subnetmask, 
                "numports": switch.numports
                "ports": switch.ports}
            adapted_switchobj_list.append(switch_to_add)
        print(adapted_switchobj_list)
            
    def loadDevicesXML(self):
        return False
        
    def writeDevicesXML(self, switchobjList):
        return False

    def loadDevicesYAML(self):
        return False
        
    def writeDevicesYAML(self, switchobjList):
        return False