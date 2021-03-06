from ncclient import manager
from router_info import router

config_template = open(
    "C:/Users/hammermi/Documents/work/Activities/Knowledge/SW-DEV/Python/python_learning/knox_hutchinson_codesamples/Python/Networking/IOS-XE/ios_config.xml").read()

netconf_config = config_template.format(
    interface_name="GigabitEthernet2", interface_desc="#LINK-TO-sc1")

with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], hostkey_verify=False) as m:
    #target="running" in this case means: make the changes directly to the RUNNING-CONFIG
    device_reply = m.edit_config(netconf_config, target="running")
    print(device_reply)
