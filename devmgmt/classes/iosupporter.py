import pickle
import json

class IOSupporter:
    def __init__(self, filename):
        self.filename = filename
        
    def loadDevices(self):
        with open(self.filename, 'rb') as rfile:
            loaded_switchobjList = pickle.load(rfile)
            return loaded_switchobjList

    def writeDevices(self, switchobjList):
        with open(self.filename, 'wb') as wfile:
            pickle.dump(switchobjList, wfile, protocol=pickle.HIGHEST_PROTOCOL)

    def loadDevicesJSON(self):
        return False
        
    def writeDevicesJSON(self, switchobjList):
        adapted_switchobj_list = list()
        for switchdev in switchobjList:
            switch_to_add = {"id": switchdev.idnum, "snum": switchdev.snr, "sys_mac": switchdev.sys_mac, "man_ip": switchobj.man_ipaddress, "ip_subnetmask": switchdev.ip_subnetmask, "numports": switchdev.numports, "ports": switchdev.ports}
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