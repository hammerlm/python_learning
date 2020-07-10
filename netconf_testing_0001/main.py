from ncclient import manager

router = {"host": "ip-address-of-networkdevice", "port": "10000", "username": "developer", "password": "cisco"}

with manager.connect(host=router["host"], port=router["port"], username=router["username"], password=router["password"], hostkey_verify=False) as m:
    m.close_session()
