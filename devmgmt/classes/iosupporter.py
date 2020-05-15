import pickle
import json
import yaml
from classes.switch import Switch
from classes.switch import SwitchPort

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
        with open(self.filename) as json_file:
            switches_loaded = json.load(json_file)
            switches_to_return = list()
            for s in switches_loaded:                
                ports_to_add = list()
                for port_key in s["ports"]:
                    #SwitchPort-Init: mac, is_trunk, native_vlan
                    #Format in json-file:{"mac" : self.mac, "is_trunk" : self.is_trunk, "native_vlan" : self.native_vlan}
                    ports_to_add.append(SwitchPort(s["ports"][port_key]["mac"], s["ports"][port_key]["is_trunk"], s["ports"][port_key]["native_vlan"]))
                #Switch-Init: idnum, serialnum, sys_macaddress, man_ipaddress, ip_subnetmask, hostname, numports
                #Format in json-file: switch_to_add = {"id", "snum", "sys_mac", "man_ip", "ip_subnetmask", "numports", "ports"}
                switch_to_add = Switch(s["id"], s["snum"], s["sys_mac"], s["man_ip"], s["ip_subnetmask"], s["hostname"], s["numports"])
                switch_to_add.ports = ports_to_add
                switches_to_return.append(switch_to_add)
            return switches_to_return
                
        
    def writeDevicesJSON(self, switchobjList):
        adapted_switchobj_list = list()
        for switchdev in switchobjList:
            switch_to_add = {"id": switchdev.idnum, "snum": switchdev.snr, "sys_mac": switchdev.sys_mac, "man_ip": switchdev.man_ip, "ip_subnetmask": switchdev.ip_subnetmask, "hostname" : switchdev.hostname, "numports": switchdev.numports, "ports" : switchdev.getPortsAsDict()}
            adapted_switchobj_list.append(switch_to_add)
        with open(self.filename, 'w') as outfile:
            json.dump(adapted_switchobj_list, outfile)
            
    def loadDevicesXML(self):
        return False
        
    def writeDevicesXML(self, switchobjList):
        return False

    def loadDevicesYAML(self):
        with open(self.filename) as yaml_file:
            switches_loaded = yaml.full_load(yaml_file)
            switches_to_return = list()
            for s in switches_loaded:                
                ports_to_add = list()
                for port_key in s["ports"]:
                    #SwitchPort-Init: mac, is_trunk, native_vlan
                    #Format in json-file:{"mac" : self.mac, "is_trunk" : self.is_trunk, "native_vlan" : self.native_vlan}
                    ports_to_add.append(SwitchPort(s["ports"][port_key]["mac"], s["ports"][port_key]["is_trunk"], s["ports"][port_key]["native_vlan"]))
                #Switch-Init: idnum, serialnum, sys_macaddress, man_ipaddress, ip_subnetmask, hostname, numports
                #Format in json-file: switch_to_add = {"id", "snum", "sys_mac", "man_ip", "ip_subnetmask", "numports", "ports"}
                switch_to_add = Switch(s["id"], s["snum"], s["sys_mac"], s["man_ip"], s["ip_subnetmask"], s["hostname"], s["numports"])
                switch_to_add.ports = ports_to_add
                switches_to_return.append(switch_to_add)
            return switches_to_return
        
    def writeDevicesYAML(self, switchobjList):
        adapted_switchobj_list = list()
        for switchdev in switchobjList:
            switch_to_add = {"id": switchdev.idnum, "snum": switchdev.snr, "sys_mac": switchdev.sys_mac, "man_ip": switchdev.man_ip, "ip_subnetmask": switchdev.ip_subnetmask, "hostname" : switchdev.hostname, "numports": switchdev.numports, "ports" : switchdev.getPortsAsDict()}
            adapted_switchobj_list.append(switch_to_add)
        with open(self.filename, 'w') as outfile:
            yaml.dump(adapted_switchobj_list, outfile)