import requests
import json

"""
Modify these please
"""
switchuser='admin'
switchpassword='cisco'

url='http://192.168.8.221/ins'
myheaders={'content-type':'application/json'}
payload={
  "ins_api": {
    "version": "1.0",
    "type": "cli_show",
    "chunk": "0",
    "sid": "1",
    "input": "show int status",
    "output_format": "json"
  }
}
response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
print(json.dumps(response, indent=2, sort_keys=True))