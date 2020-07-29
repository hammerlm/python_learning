from ncclient import manager
import xmltodict
from prettytable import PrettyTable
from router_info import router
# import logging
# logging.basicConfig(level=logging.DEBUG)

netconf_filter = open("C:/Users/hammermi/Documents/work/Activities/Knowledge/SW-DEV/Python/python_learning/dn_assoc_0001/netconf-filter.xml").read()

with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], hostkey_verify=False) as m:
    # get the running config on the filtered out interface
    print('Connected')
    interfaces_netconf = m.get(netconf_filter)
    print('getting running config')

# XMLTODICT for converting xml output to a python dictionary
interfaces_python = xmltodict.parse(interfaces_netconf.xml)["rpc-reply"]["data"]

t = PrettyTable(['Name', 'Description', 'Enabled', 'IP', 'Netmask'])
for interface_python in interfaces_python["interfaces"]["interface"]:
    name = interface_python["name"]
    enabled = interface_python["enabled"]
    try:
        description = interface_python["description"]        
    except:
        description = ""
    try:
        ip = interface_python["ipv4"]["address"]["ip"]        
    except:
        ip = ""
    try:
        netmask = interface_python["ipv4"]["address"]["netmask"]        
    except:
        netmask = "" 
    t.add_row([name, description, enabled, ip, netmask])
print(t)