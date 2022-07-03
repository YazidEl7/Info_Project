
class Info:
    # Class Variable
    #   animal = 'dog'

    # The init method or constructor
    def __init__(self, computername):
        # Instance Variable
        self.computername = computername

        # Adds an instance variable

    def setinfo(self, infodata):
        self.username = infodata[0]["username"]
        self.domain = infodata[1]["domain"]
        self.adress = infodata[2]["IP"]
        self.status = infodata[3]["status"]
        self.biosserial = infodata[4]["bios_serial"]

    # Retrieves instance variable
    def getbios(self):
        return self.biosserial
