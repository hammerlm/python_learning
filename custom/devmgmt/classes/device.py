class Device:
    def __init__(self, idnum, serialnum):
        self.idnum = idnum
        self.snr = serialnum

    def __str__(self):
        returnval = "idnum=" + str(self.idnum) + ",serialnum=" + self.snr
        return returnval

