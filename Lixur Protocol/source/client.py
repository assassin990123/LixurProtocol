import socket
import random
import hashlib
import threading
import subprocess as sp
from util import Util


class P2P:
    def __init__(self):
        self.peers = []
        pass

    @staticmethod
    def ping(self, ip_address):
        if sp.call(["ping", ip_address]) == 0:
            return True
        else:
            return False

    def server_functionality(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", 0))
        self.host = s.getsockname()[0]
        self.port = int(s.getsockname()[1])
        self.pair = (self.host, self.port)
        self.peers.append(self.pair)

        print(f'\nListening on {self.host}:{self.port}')
        s.listen(int(1e+9))

        while 1:
            print("Waiting for connection...\n")
            conn, address = s.accept()
            print(f'{address} has connected.')
            while 1:
                data = conn.recv(1024)
                print(f'{address} : {data.decode("utf-8")}')
                if not data:
                    break
                conn.send(data)
            conn.close()

    def connect_to_user(self, ip_address, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if ip_address == self.host and port == self.port:
            raise ValueError("You can't connect to yourself!")

        try:
            s.connect_ex((ip_address, port))
            print(f'Connected to {ip_address}:{port}')
        except ConnectionRefusedError:
            raise OSError(f"There is nothing listening at {ip_address, port}. Either it can't receive messages for some reason or is not available.")

        while 1:
            x = input("Send a message or graph? (m/g): ")
            if x == "m":
                info = bytes(input("Enter the message: "), "utf-8")
            if x == "g":
                util = Util()
                info = util.get_graph()
            try:
                s.send(info)
            except ConnectionResetError:
                print("The device you are trying to send to is offline.")
            print("Message sent.")
            continue

        data = s.recv(1024).decode('utf-8')
        s.close()
        print('Received', repr(data))

    def connect_to_all(self):
        for x in self.peers:
            for ip_address in x:
                if self.ping(ip_address):
                    self.connect_to_user(ip_address, port)
                else:
                    print(f"The device {ip_address}:{port} you are trying to connect to is offline.")

    def client_functionality(self):
        target_host = input("\nEnter the host to connect to: ")
        target_port = int(input("Enter the port to connect to: "))
        self.connect_to_user(target_host, target_port)



p = P2P()
s_thread = threading.Thread(target=p.server_functionality)
c_thread = threading.Thread(target=p.client_functionality)

s_thread.start()
c_thread.start()
