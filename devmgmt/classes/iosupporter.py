import pickle
import json
import yaml
from lxml import etree
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
                ports_to_add = {}
                for port_key in s["ports"]:
                    #SwitchPort-Init: mac, is_trunk, native_vlan
                    #Format in json-file:{"mac" : self.mac, "is_trunk" : self.is_trunk, "native_vlan" : self.native_vlan}
                    ports_to_add[port_key] = SwitchPort(s["ports"][port_key]["mac"], s["ports"][port_key]["is_trunk"], s["ports"][port_key]["native_vlan"])
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
        #Alternative
        #with open(xmlFile) as fobj:
        #    xml = fobj.read()
        #root = etree.fromstring(xml)
        tree = etree.parse(self.filename)
        root = etree.fromstring(etree.tostring(tree).decode())
        devicelist = list()
        for switch in root.getchildren():
            id_param = int(switch.attrib["id"])
            for key in switch.getchildren():
                if key.tag == "snum":
                    snum_param = key.value
                elif key.tag == "sys_mac":
                    sys_mac_param = key.value
                elif key.tag == "man_ip":
                    man_ip_param = key.value
                elif key.tag == "ip_subnetmask":
                    ip_subnetmask_param = key.value
                elif key.tag == "hostname":
                    hostname_param = key.value
                elif key.tag == "numports":
                    numports_param = int(key.value)
                elif key.tag == "ports":
                    ports_dict_param = {}
                    for key2 in key.getchildren():
                        port_key_param = key2.attrib["pt"]
                        if key2.tag == "mac":
                            port_mac_param = key2.attrib["mac"]                            
                        elif key2.tag == "is_trunk":
                            port_is_trunk_param = bool(key2.attrib["is_trunk"])
                        elif key2.tag == "native_vlan":
                            port_native_vlan_param = int(key2.attrib["native_vlan"])
                        #def __init__(self, mac, is_trunk, native_vlan):
                        ports_dict_param[port_key_param] = SwitchPort(port_mac_param, port_is_trunk_param, port_native_vlan_param)
            #def __init__(self, idnum, serialnum, sys_macaddress, man_ipaddress, ip_subnetmask, hostname, numports):
            new_switch = Switch(id_param, snum_param, sys_mac_param, man_ip_param, ip_subnetmask_param, hostname_param, numports_param)
            new_switch.ports = ports_dict_param
            devicelist.append(new_switch)
        return devicelist
        
    def writeDevicesXML(self, switchobjList):
        devices_tag = etree.Element("devices")
        for switchdev in switchobjList:
            #switch_to_add =
            #    {"id": switchdev.idnum,
            #     "snum": switchdev.snr,
            #     "sys_mac": switchdev.sys_mac,
            #     "man_ip": switchdev.man_ip,
            #     "ip_subnetmask": switchdev.ip_subnetmask,
            #     "hostname" : switchdev.hostname,
            #     "numports": switchdev.numports,
            #     "ports" : switchdev.getPortsAsDict()}
            switch_tag = etree.Element("switch", id=str(switchdev.idnum))
            snum_tag = etree.Element("snum")
            snum_tag.text = switchdev.snr
            switch_tag.append(snum_tag)
            sys_mac_tag = etree.Element("sys_mac")
            sys_mac_tag.text = switchdev.sys_mac
            switch_tag.append(sys_mac_tag)
            man_ip_tag = etree.Element("man_ip")
            man_ip_tag.text = switchdev.man_ip
            switch_tag.append(man_ip_tag)
            ip_subnetmask_tag = etree.Element("ip_subnetmask")
            ip_subnetmask_tag.text = switchdev.ip_subnetmask
            switch_tag.append(ip_subnetmask_tag)
            hostname_tag = etree.Element("hostname")
            hostname_tag.text = switchdev.hostname
            switch_tag.append(hostname_tag)
            numports_tag = etree.Element("numports")
            numports_tag.text = str(switchdev.numports)
            switch_tag.append(numports_tag)
            ports_tag = etree.Element("ports")            
            for port_key in switchdev.ports:
                #SwitchPort-Init: mac, is_trunk, native_vlan
                port_tag = etree.Element("port", pt=str(port_key))
                ports_tag.append(port_tag)
                port_tag.append(etree.Element("mac", mac=switchdev.ports[port_key].mac))
                port_tag.append(etree.Element("is_trunk", is_trunk=str(switchdev.ports[port_key].is_trunk)))
                port_tag.append(etree.Element("native_vlan", native_vlan=str(switchdev.ports[port_key].native_vlan)))
            switch_tag.append(ports_tag)
            devices_tag.append(switch_tag)
        #print(etree.tostring(devices_tag, pretty_print=True).decode())
        tree = etree.ElementTree(devices_tag)
        tree.write(self.filename)        

    def loadDevicesYAML(self):
        with open(self.filename) as yaml_file:
            switches_loaded = yaml.full_load(yaml_file)
            switches_to_return = list()
            for s in switches_loaded:                
                ports_to_add = {}
                for port_key in s["ports"]:
                    #SwitchPort-Init: mac, is_trunk, native_vlan
                    #Format in json-file:{"mac" : self.mac, "is_trunk" : self.is_trunk, "native_vlan" : self.native_vlan}
                    ports_to_add[port_key] = SwitchPort(s["ports"][port_key]["mac"], s["ports"][port_key]["is_trunk"], s["ports"][port_key]["native_vlan"])
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