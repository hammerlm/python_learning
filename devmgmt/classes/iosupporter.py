import pickle

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
            
        
