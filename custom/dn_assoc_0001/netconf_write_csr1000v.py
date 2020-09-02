from ncclient import manager
from router_info import router

config_template = open(
    "C:/Users/hammermi/Documents/work/Activities/Knowledge/SW-DEV/Python/python_learning/dn_assoc_0001/netconf_ios_config.xml").read()

netconf_config_g2 = config_template.format(interface_name="GigabitEthernet2", interface_desc="#LINK-TO-sc1", interface_ip="10.12.0.1", interface_netmask="255.255.255.252")
netconf_config_g3 = config_template.format(interface_name="GigabitEthernet3", interface_desc="#LINK-TO-sc2", interface_ip="10.13.0.1", interface_netmask="255.255.255.252")
netconf_config_l0 = config_template.format(interface_name="Loopback0", interface_desc="#Loopback0-interface", interface_ip="192.168.0.1", interface_netmask="255.255.255.255")
netconf_config_l1 = config_template.format(interface_name="Loopback1", interface_desc="#Loopback1", interface_ip="192.168.1.1", interface_netmask="255.255.255.255")

with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], hostkey_verify=False) as m:
    #target="running" in this case means: make the changes directly to the RUNNING-CONFIG
    #device_reply = m.edit_config(netconf_config_g2, target="running")
    #print(device_reply)
    #device_reply = m.edit_config(netconf_config_g3, target="running")
    device_reply = m.edit_config(netconf_config_l0, target="running")
    print(device_reply)
