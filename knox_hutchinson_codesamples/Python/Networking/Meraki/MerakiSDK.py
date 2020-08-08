from meraki_sdk.meraki_sdk_client import MerakiSdkClient
import json
from pprint import pprint
# import logging
# logging.basicConfig(level=logging.DEBUG)


# CREATE Connection Object
x_cisco_meraki_api_key = '614438ffec2468d44a7ef1bd58dfecf8f9847c3a'  # Demo DevNet Sandbox
meraki = MerakiSdkClient(x_cisco_meraki_api_key)

# Get Orgs
orgs = meraki.organizations.get_organizations()
# print(json.dumps(orgs, indent=2, sort_keys=True))
# pprint(orgs)


# Set OrgId
for org in orgs:
    if org['name'] == "DevNet Sandbox":
        orgId = org['id']

# Get Networks in Org
params = {}
params['organization_id'] = orgId
networks = meraki.networks.get_organization_networks(params)
pprint(networks)

# Set NetworkId
for network in networks:
    if network['name'] == "DevNet Sandbox ALWAYS ON":
        netId = network['id']
# print(netId)

# GET VLANS
vlans = meraki.vlans.get_network_vlans(netId)

vlan = vlans[0]
# CHANGE VLAN NAME HERE
vlan['name'] = 'Default'


updatedVlan = {}
updatedVlan['network_id'] = netId
updatedVlan['vlan_id'] = vlan['id']
updatedVlan['update_network_vlan'] = vlan
# pprint(updatedVlan)
result = meraki.vlans.update_network_vlan(updatedVlan)

# VERIFY
vlans = meraki.vlans.get_network_vlans(netId)
pprint(vlans)
