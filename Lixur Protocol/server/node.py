import socket
import random
import threading
import json
import time

from graph import Graph
from cryptography import KeyGen
from util import Util

k = KeyGen()
util = Util()
graph = Graph()
# Do not forget to add IPv6 Functionality!

class Node:
    def __init__(self):
        self.graph = Graph()
        self.port = random.randint(1024, 65000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('170.187.204.77', self.port))
        self.sock.listen()
        print(f'Selected Port: {self.port}')
    def server_functionality(self):
        while True:
            client_connection_socket, client_address = self.sock.accept()
            print(f'The connection with {client_address} has been established.')
            threading.Thread(target=self.client_thread,
                             args=(client_connection_socket, client_address)).start()

    def client_thread(self, client_connection_socket, client_address):
        bytes = 500000000
        try:
            data = client_connection_socket.recv(bytes).decode()
            while True:
                if data:
                    try:
                        self.eval_command(data, client_connection_socket)
                        data = client_connection_socket.recv(bytes).decode()
                    except ConnectionResetError:
                        client_connection_socket.close()
                        print(f'{client_address} has left.')
        except ConnectionResetError:
            client_connection_socket.close()
            print(f'{client_address} has left.')

    def eval_command(self, comm, conn):
        if comm == "new" or "existing":
            if comm == "new":
                k.wallet(k, comm)
                keystore = f'''{k.get_keystore(k)}'''
                phrase = str(k.get_phrase(k))
                all = keystore, phrase
                conn.send(util.encode_data(all))

            elif comm == "existing":
                pass

            elif "cipher_text" in comm:
                pass

            elif len(comm) == 42 or len(comm) == 39 or len(comm) == 32:
                self.phrase = comm
                self.decryption_ready = True
                conn.send(util.encode_data(util.aes_wallet_decrypt(
                    self.phrase, self.keystore['hash'], self.keystore)))

            elif comm == "get_graph" or "get_graph" in comm:
                conn.send(util.encode_data(str(util.get_graph())))

            elif "public_key" and "private_key" in comm:
                arguments = eval(comm)
                sender = arguments['sender']
                receiver = arguments['receiver']
                amount = arguments['amount']
                signature = k.sign_tx(arguments['public_key'], arguments['private_key'], "Lixur")
                tx = graph.make_transaction(sender, receiver, amount, signature)
                conn.send(util.encode_data(tx))

    def return_server_address(self):
        return self.server_address[0], self.server_address[1]
    def run_socket(self):
        s_thread = threading.Thread(target=self.server_functionality)
        s_thread.start()
    def writeGraphToJSONfile(self):
        try:
            filename = "server/graph.json"
            with open(filename, 'w') as f:
                print(self.getGraphAsJSONdict())
                json.dump(self.getGraphAsJSONdict(), f)
        except FileNotFoundError:
            filename = "graph.json"
            with open(filename, 'w') as f:
                json.dump(self.getGraphAsJSONdict(), f)
    def readGraphFromJSONfile(self):
        filename = "server/graph.json"
        with open(filename, 'r') as f:
            graphJSON = json.load(f)
        return graphJSON
    def getGraphAsJSONdict(self):
        serializable_format = ({})
        for (k, v) in self.graph.graph.items():
            serializable_format.update({k: v.get_transaction_dict()})
            sort_by = "index"  # Options are: "index", "amount", "own_weight" or "timestamp"
        serializable_format = sorted(serializable_format.items(), key=lambda x: x[1][sort_by], reverse=True)
        return serializable_format
    def refresh(self):
        self.writeGraphToJSONfile()