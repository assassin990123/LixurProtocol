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
        self.value = None
        self.peers = []
        self.peer_count = len(self.peers)
        self.query_num = 3
        self.your_id = None
        self.port = random.randint(1024, 65000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('170.187.204.77', self.port))
        self.sock.listen()
        print(f'Selected Port: {self.port}')
    def server_functionality(self):
        while True:
            self.connection, client_address = self.sock.accept()
            print(f"{client_address} has connected.")
            self.data = self.connection.recv(500000).decode()
            print(f'Data received from {client_address}:{self.data}')
            self.eval_command(self.data)

    def eval_command(self, comm):
        if comm == "new" or "existing":
            if comm == "new":
                k.wallet(k, comm)
                keystore = f'''{k.get_keystore(k)}'''
                phrase = str(k.get_phrase(k))
                print(phrase)
                stats = util.aes_wallet_decrypt(
                    phrase, eval(keystore)['hash'], eval(keystore))
                all = keystore, phrase, stats
                self.connection.send(util.encode_data(all))

            elif comm == "existing":
                self.connection.send(util.encode_data("send_ks"))
                time.sleep(.1)
            elif "cipher_text" in comm:
                self.keystore = eval(comm)
                self.connection.send(util.encode_data("send_phr"))
                time.sleep(.1)

            elif len(comm) == 42 or len(comm) == 39 or len(comm) == 32:
                self.phrase = comm
                self.decryption_ready = True
                self.connection.send(util.encode_data(util.aes_wallet_decrypt(
                    self.phrase, self.keystore['hash'], self.keystore)))
            elif comm == "get_graph" or "get_graph" in comm:
                self.connection.send(util.encode_data(str(util.get_graph())))
                print("Graph sent.")
            elif "public_key" and "private_key" in comm:
                print("Received a new transaction, adding...")
                arguments = eval(comm)
                sender = arguments['sender']
                receiver = arguments['receiver']
                amount = arguments['amount']
                signature = k.sign_tx(arguments['public_key'], arguments['private_key'], "Lixur")
                tx = graph.make_transaction(sender, receiver, amount, signature)
                self.connection.send(util.encode_data(tx))
    def return_server_address(self):
        return self.server_address[0], self.server_address[1]
    def run_socket(self):
        s_thread = threading.Thread(target=self.server_functionality)
        s_thread.start()
    def writeGraphToJSONfile(self):
        try:
            filename = "server/graph.json"
            with open(filename, 'w') as f:
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