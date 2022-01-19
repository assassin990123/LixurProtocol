from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class Server(DatagramProtocol):
    def __init__(self):
        self.clients = set()

    def datagramReceived(self, datagram, address):
        datagram = datagram.decode("utf-8")
        if datagram == "Ready":
            self.clients.add(address)
            self.transport.write(",".join([str(client) for client in self.clients]), address)

if __name__ == "__main__":
    reactor.listenUDP(9999, Server())
    reactor.run()
