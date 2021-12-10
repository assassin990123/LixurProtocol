class Neighbour:
    def __init__(self, *args):
        self.IPaddress = None
        self.portnumber = None
        self.lastComm = None
        self.isonline = False

    def setIP(self, ip):
        self.IPaddress = ip

    def setPort(self, port):
        self.portnumber = port

    def setLastTalk(self, timestamp):
        lastComm = timestamp

    def checkOnline(self):
        #TODO: try to ping, or connect to the ip:port and update status
        return None