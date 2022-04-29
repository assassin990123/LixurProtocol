import socket
import random
import hashlib
import threading
import json
import os
import subprocess as sp

from graph import Graph

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
    def server_functionality(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('0.0.0.0',self.port))
        sock.listen()

        while 1:
            connection, client_address = sock.accept()
            print(f"{client_address} has connected.")
            self.peers.append(client_address)

        while True:
            data = connection.recv(1024).decode()
            if "cipher_text" in eval(data):
                self.is_keystore = True
    def return_server_address(self):
        return self.server_address[0], self.server_address[1]
    def run_socket(self):
        s_thread = threading.Thread(target=self.server_functionality)
        s_thread.start()
    def writeGraphToJSONfile(self):
        try:
            filename = "source/graph.json"
            with open(filename, 'w') as f:
                json.dump(self.getGraphAsJSONdict(), f)
        except FileNotFoundError:
            filename = "graph.json"
            with open(filename, 'w') as f:
                json.dump(self.getGraphAsJSONdict(), f)
    def readGraphFromJSONfile(self):
        filename = "source/graph.json"
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

node = Node()
node.run_socket()
