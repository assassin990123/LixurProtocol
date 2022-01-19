from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from random import randint

class Client(DatagramProtocol):
    def __init__(self, host, port):
        if host == 'localhost':
            host = "127.0.0.1"

        self.id = host, port
        self.addresses = None
        self.server = '127.0.0.1', 9999
        print("Working on:", self.id)

    #     Port : 5000

    def startProtocol(self):
        self.transport.write("Prepared!".encode("utf-8"), self.server)

    def datagramReceived(self, datagram, address):
        data = datagram.decode("utf-8")
        if address == self.server:
            print("Choose a client from these\n", data)
            self.address = input("Enter the host: "), int(input("Enter the port: "))
            reactor.callInThread(self.send_message)
        else:
            print("Message from", address, ":", data)

def send_message(self):
    while True:
        self.transport.write(input("Message:").encode("utf-8"), self.address)

if __name__ == "__main__":
    port = randint(1000, 5000)
    reactor.listenUDP(port, Client("localhost", port))
    reactor.run()