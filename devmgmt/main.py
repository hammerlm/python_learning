#added a comment
from classes.iosupporter import IOSupporter
from classes.switch import Switch
import os
import sys

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

continue_bool = True
prompt = "-new->"
devicelist = list()
iosupportobj = IOSupporter("")
data_dir_path = get_script_path() + "/data/"
data_file_path = ""

def deviceListContains(key, value):
    global devicelist
    if key == "-sn":
        for device in devicelist:
            if device.snr == value:
                return True
    elif key == "-mac":
        for device in devicelist:
            if device.sys_mac == value:
                return True
    elif key == "-ip":
        for device in devicelist:
            if device.man_ip == value:
                return True
    elif key == "-name":
        for device in devicelist:
            if device.hostname == value:
                return True
    return False

def getNextDeviceID():
    global devicelist
    next_id = 0
    for device in devicelist:
        if device.idnum > next_id:
            next_id = device.idnum
    next_id = next_id + 1
    return next_id

def getDeviceByHostname(hostname):
    global devicelist
    for device in devicelist:
        if device.hostname == hostname:
            return device
    return False

def evaluate_loadInput(inputList):
    global data_dir_path
    filename = data_dir_path + inputList[2]
    if os.path.exists(filename) and inputList[1] in ["json", "yaml", "xml"]:
        return True
    else:
        print("Either File:", inputList[1], "does not exist or (json/yaml/xml)-Parameter-failure")
        return False
    

def evaluate_writeInput(inputList):
    global prompt
    if prompt == "-new->":
        if inputList[2] == "this":
            print("File can't be saved with the 'this'-Parameter as this process is still unsaved.")
            return False
        if inputList[1] not in ["json", "yaml", "xml"]:
            return False
    return True

def evaluate_addInput(inputList):
    #for switch: type, serialnum, sys_macaddress, man_ipaddress, ip_subnetmask, hostname, numports
    type_param = str(inputList[1])
    snum_param = str(inputList[6])
    sysmac_param = str(inputList[3])
    manip_param = str(inputList[4])
    mask_param = str(inputList[5])
    hostname_param = str(inputList[2])
    numports_param = inputList[7]
    if type_param == "switch":
        if str(type(snum_param)) == "<class 'str'>":
            if str(type(sysmac_param)) == "<class 'str'>":
                if str(type(manip_param)) == "<class 'str'>":
                    if str(type(mask_param)) == "<class 'str'>":
                        if str(type(hostname_param)) == "<class 'str'>":
                            try:
                                is_unique = True
                                if deviceListContains("-sn", snum_param):
                                    print("The provided serialnumber already exists in devicelist.")
                                    is_unique = False
                                if deviceListContains("-mac", sysmac_param):
                                    print("The provided sysmac already exists in devicelist.")
                                    is_unique = False
                                if deviceListContains("-ip", manip_param):
                                    print("The provided sysmac already exists in devicelist.")
                                    is_unique = False
                                if deviceListContains("-name", hostname_param):
                                    print("The provided sysmac already exists in devicelist.")
                                    is_unique = False
                                if is_unique == False:
                                    return False
                                if str(type(int(numports_param))) == "<class 'int'>":
                                    if int(numports_param) >= 8 and int(numports_param) <= 48 and int(numports_param) % 8 == 0:
                                        return True
                                    else:
                                        print("Wrong value for numports_param.")
                                        return False
                                else:
                                    print("Wrong format for numports_param.")
                                    return False
                            except:
                                print("Unexpected error with numports_param:", sys.exc_info()[0])
                                return False    
                        else:
                            print("Wrong format for hostname.")
                            return False
                    else:
                        print("Wrong format for subnetmask.")
                        return False
                else:
                    print("Wrong format for man_ip.")
                    return False
            else:
                print("Wrong format for sys_mac.")
                return False
        else:
            print("Wrong format for serial_num.")
            return False     
    elif type_param == "router":
        print("router-functionality is not yet implemented.")
        return False
    elif type_param == "hub":
        print("hub-functionality is not yet implemented.")
        return False
    else:
        print("Unrecognized type specified:", str(type_param))
        return False

def evaluate_modifyInput(hostname_param, allowed_param_list, modifydict):
    #allowed_param_list = ["-sn", "-mac", "-ip", "-name"]
    try:
        for key in modifydict:
            if key == "-sn":
                if str(type(modifydict[key])) == "<class 'str'>":
                    if deviceListContains("-sn", modifydict[key]):
                        print("Parametervalue of -sn is already existing in modifylist")
                        return False
                else:
                    print("Parametervalue of -sn is not formatted correctly")
                    return False
            elif key == "-mac":
                if str(type(modifydict[key])) == "<class 'str'>":
                    if deviceListContains("-mac", modifydict[key]):
                        print("Parametervalue of -mac is already existing in devicelist")
                        return False
                else:
                    print("Parametervalue of -mac is not formatted correctly")
                    return False
            elif key == "-ip":
                if str(type(modifydict[key])) == "<class 'str'>":
                    if deviceListContains("-ip", modifydict[key]):
                        print("Parametervalue of -ip is already existing in devicelist")
                        return False
                else:
                    print("Parametervalue of -ip is not formatted correctly")
                    return False
            elif key == "-name":
                if str(type(modifydict[key])) == "<class 'str'>":
                    if deviceListContains("-ip", modifydict[key]):
                        print("Parametervalue of -name is already existing in devicelist")
                        return False
                else:
                    print("Parametervalue of -name is not formatted correctly")
                    return False
            elif key == "-mask":
                if str(type(modifydict[key])) == "<class 'str'>":
                    if deviceListContains("-mask", modifydict[key]):
                        print("Parametervalue of -mask is already existing in devicelist")
                        return False
                else:
                    print("Parametervalue of -mask is not formatted correctly")
                    return False
        return True
    except:
        print("Unexpected error with modifyinput-command-evaluation", sys.exc_info()[0])
        return False

def process_loadCommand(inputList):
    global data_dir_path, data_file_path, iosupportobj, prompt, devicelist
    print("processing loadcommand")
    if evaluate_loadInput(inputList):
        try:
            data_file_path = data_dir_path + inputList[2]
            iosupportobj.filename = data_file_path
            prompt = inputList[2] + "->"
            if(inputList[1] == "json"):
                devicelist = iosupportobj.loadDevicesJSON()
            elif(inputList[1] == "yaml"):
                devicelist = iosupportobj.loadDevicesYAML()
            elif(inputList[1] == "xml"):
                devicelist = iosupportobj.loadDevicesXML()
            print("File loaded successfully.")
        except IOError:
            print("I/O error")
            data_file_path = ""
            iosupportobj.filename = ""
            prompt = "-new->"
            devicelist = list()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            data_file_path = ""
            iosupportobj.filename = ""
            prompt = "-new->"
            devicelist = list()      
    else:
        print("Wrong parameters for Load-Command.")
    
def process_writeCommand(inputList):
    global data_dir_path, data_file_path, iosupportobj, prompt, devicelist
    print("process writeCommand")
    if evaluate_writeInput(inputList):
        data_file_path_old = data_file_path
        filename_old = iosupportobj.filename
        prompt_old = prompt
        try:
            if(inputList[2] != "this"):
                data_file_path = data_dir_path + inputList[2]
                iosupportobj.filename = data_file_path
                prompt = inputList[2] + "->"
                if(inputList[1] == "json"):
                    iosupportobj.writeDevicesJSON(devicelist)
                elif(inputList[1] == "yaml"):
                    iosupportobj.writeDevicesYAML(devicelist)
                elif(inputList[1] == "xml"):
                    iosupportobj.writeDevicesXML(devicelist)
                print("File written successfully.")
                return True
            else:
                return False
        except:
            print("Unexpected error:", sys.exc_info()[0])
            data_file_path = data_file_path_old
            iosupportobj.filename = filename_old
            prompt = prompt_old
            return False
    else:
        print("Wrong parameters for Write-Command.")
        return False
    
def process_quitCommand():
    global continue_bool
    print("processing quitcommand")
    continue_bool = False
    print("program closed")
    
def process_addCommand(inputList):
    #for swtich: type, serialnum, sys_macaddress, man_ipaddress, ip_subnetmask, hostname, numports
    global devicelist
    type_param = str(inputList[1])
    snum_param = str(inputList[6])
    sysmac_param = str(inputList[3])
    manip_param = str(inputList[4])
    mask_param = str(inputList[5])
    hostname_param = str(inputList[2])
    numports_param = inputList[7]
    
    print("processing addcommand")
    if evaluate_addInput(inputList):
        if type_param == "switch":
            switch_to_add = Switch(getNextDeviceID(), snum_param, sysmac_param, manip_param, mask_param, hostname_param, int(numports_param))
            devicelist.append(switch_to_add)
            print("Successfully added device:")
            print(switch_to_add.__str__())
        elif type_param == "router":
            print("router-functionality is not yet implemented.")
            return False
        elif type_param == "hub":
            print("hub-functionality is not yet implemented.")
            return False
        else:
            print("Unrecognized type specified:", str(type_param))
            return False            
    else:
        print("Wrong parameters for Add-Command.")
    
def process_deleteCommand(inputList):
    global devicelist
    print("process deletecommand")
    try:
        device_to_delete = getDeviceByHostname(inputList[1])
        print("Device to delte:")
        print(device_to_delete.__str__())
        devicelist.remove(device_to_delete)
        print("Delete-Operation successfully finished.")
    except:
        print("Unexpected error on delete-operation:", sys.exc_info()[0])

def process_deleteallCommand():
    global devicelist
    print("process deletallcommand")
    print("devices to be deleted:")
    for devobj in devicelist:
        print(devobj.__str__())
    if input("Are you sure? (Y/N):") == "Y":
        devicelist = list()
        print("All devices deleted.")
    else:
        print("No valid input detected.")
    
def process_showCommand(inputList):
    global devicelist
    print("process showcommand")
    try:
        print(getDeviceByHostname(inputList[1]).__str__())
    except:
        print("Unexpected error on show-operation:", sys.exc_info()[0])
    
def process_showallCommand():
    global devicelist
    print("processing showallcommand")
    for devobj in devicelist:
        print(devobj.__str__())

def process_modifyCommand(inputList):
    # for switch: hostname, -sn=serialnum, -mac=sys_macaddress, -ip=-man_ipaddress, --mask=ip_subnetmask, -name=hostname
    allowed_param_list = ["-sn", "-mac", "-ip", "-mask", "-name"]
    #dk
    modifydict = {}
    hostname_param = str(inputList[1])
    counter = 0
    counter_valid = 0
    for in_element in inputList:
        if counter >= 2:
            in_element_splitted = in_element.split("=")
            if len(in_element_splitted) == 2:
                key = in_element_splitted[0]
                val = in_element_splitted[1]
                if key in allowed_param_list:
                    modifydict[key] = val
                    counter_valid = counter_valid + 1
        else:
            counter = counter + 1
    print("processing modifycommand")
    if counter_valid > 0:
        if evaluate_modifyInput(hostname_param, allowed_param_list, modifydict):
            print("corrected parameter-list:", modifydict)
            print("------------------------------------------------------------------------------")
            deviceToModify = getDeviceByHostname(hostname_param)
            if deviceToModify != False:
                print("Device to be modified:")
                print(deviceToModify.__str__())
                for key in modifydict:
                    if key == "-sn":
                        deviceToModify.snr = modifydict[key]
                    elif key == "-mac":
                        deviceToModify.sys_mac = modifydict[key]
                    elif key == "-ip":
                        deviceToModify.man_ip = modifydict[key]
                    elif key == "-name":
                        deviceToModify.hostname = modifydict[key]
                    elif key == "-mask":
                        deviceToModify.ip_subnetmask = modifydict[key]
                print("Device successfully modified:")
                print(deviceToModify.__str__())
            else:
                print("Device with the specified hostname does not exist")
        else:
            print("Wrong parameters for Modify-Command.")
    else:
        print("Not enough valid parameters specified for Modify-Command.")
    
def process_helpCommand():
    print("Possible commands")
    print(":h ------------------------------------------------------------------------------> show help")
    print(":l (json/yaml/xml) <filename> ---------------------------------------------------> load file")
    print(":w (json/yaml/xml) <filename>-----------------------------------> write file without closing")
    print(":wq (json/yaml/xml) <filename>-------------------------------------> write file with closing")
    print(":q --------------------------------------------------------------> close file without safing")
    print(":a (switch|router|hub) <hn> <mac> <ip> <mask> <sn> <nump> -----------------------> add a row")
    print(":m <hostname> [-sn=<val>] [-ip=<val>] [-mask=<val>] [-sn=<val>] [name=<val>] -> modify a row")
    print(":d <hostname> ----------------------------------------------------> delete row with given id")
    print(":da -----------------------------------------------------------------------> delete all rows")
    print(":s <hostname> ------------------------------------------------------> show row with given id")
    print(":sa -------------------------------------------------------------------------> show all rows")   
    
def process_input(inputval):
    #done :h  -> help
    #open: l  -> load file
    #open :w  -> write file without closing
    #open :wq -> write file with closing
    #done :q  -> close file without safing
    #done :a  -> add a row
    #done :m  -> modify a row
    #done :d  -> delete row with given id
    #done :da -> delete all rows
    #done :s  -> show row with given id
    #done :sa -> show all rows
    if inputval != "":
        splittedOnSpace = inputval.split(" ")
        if len(splittedOnSpace) > 0:
            command = splittedOnSpace[0]
        else:
            command = ""

        print("####################################################################################################################")
        print("input:", splittedOnSpace)
        print("--------------------------------------------------------------------------------------------------------------------")
        if command == ":l":
            if len(splittedOnSpace) >= 3:
                process_loadCommand(splittedOnSpace)
            else:
                print("Wrong parameters for Load-Command.")
        elif command == ":w":
            if len(splittedOnSpace) >= 3:
                process_writeCommand(splittedOnSpace)
            else:
                print("Wrong parameters for Write-Command")
        elif command == ":wq":
            if len(splittedOnSpace) >= 3:
                if process_writeCommand(splittedOnSpace):
                    process_quitCommand()
            else:
                print("Wrong parameters for Writequit-Command")
        elif command == ":q":
            process_quitCommand()
        elif command == ":a":
            #for switch: type, serialnum, sys_macaddress, man_ipaddress, ip_subnetmask, hostname, numports
            if len(splittedOnSpace) >= 8:
                process_addCommand(splittedOnSpace)
            else:
                print("Wrong parameters for Add-Command.")
        elif command == ":m":
            # for switch: hostname, -sp=serialnum, -mac=sys_macaddress, -ip=-man_ipaddress, --mask=ip_subnetmask, -name=hostname, -c=numports
            if len(splittedOnSpace) >= 2:
                process_modifyCommand(splittedOnSpace)
            else:
                print("Wrong parameters for Modify-Command.")
        elif command == ":d":
            # for switch: hostname
            if len(splittedOnSpace) >= 2:
                process_deleteCommand(splittedOnSpace)
            else:
                print("Wrong parameters for Delete-Command.")
        elif command == ":da":
            process_deleteallCommand()
        elif command == ":s":
            # for switch: hostname
            if len(splittedOnSpace) >= 2:
                process_showCommand(splittedOnSpace)
            else:
                print("Wrong parameters for Show-Command.")
        elif command == ":sa":
            process_showallCommand()
        elif command == ":h":
            process_helpCommand()
        else:
            print("Unrecognized command executed.")
        print("####################################################################################################################")

print("##############################################################################")
print("Program starting-variables:")
print("prompt:       ", "\"" + prompt + "\"")
print("data_dir_path:", "\"" + data_dir_path + "\"")
print("##############################################################################")

while (continue_bool):
    process_input(input(prompt))