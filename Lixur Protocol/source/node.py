import socket
import random
import hashlib
import threading
import json
import os
import subprocess as sp

from source.util import Util
from source.graph import Graph
from source.cloud import Cloud

util = Util()
cloud = Cloud()

# Do not forget to add IPv6 Functionality!

class Node:
    def __init__(self):
        self.graph = Graph()
        self.info = []

    def server_functionality(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('127.0.0.1', random.randint(1024, 65000))
        print('Server starting up, your server IP: {}, Port: {}\n'.format(*server_address))
        sock.bind(server_address)

        self.s_ip = server_address[0]
        self.s_port = server_address[1]
        self.add_to_info(self.s_ip, self.s_port)

        sock.listen()
        x = []

        while True:
            print('Waiting for a connection...')
            connection, client_address = sock.accept()
            print(f"{client_address} has connected.")

            while True:
                data = connection.recv(1024).decode()
                filename = "source/graph.json"
                stop_msg = "~~~"
                if data:
                    print('Server received: {!r}'.format(data))

                    if "sender" or "amount" or "amount" or "signature" or "timestamp" or "weight" or "nonce" or "index" or "edges" in data:
                        if data != stop_msg:
                            x.append(data)

                    if stop_msg in data or data == stop_msg:
                        asm_graph = util.assemble_graph(x).replace(stop_msg, '')
                        print("Entire graph has been received. Adding to graph...")
                        with open(filename, "w") as u:
                            u.truncate()
                            u.write(asm_graph)
                            u.close()
                            x.clear()
                        self.refresh()
                        print("Graph refreshed!")

                    elif data == "True" or data == "False":
                        vote = eval(data)
                else:
                    pass

    def client_functionality(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        complete = None
        print("Node started!, downloading the peer list...")
        cloud.download_peer_list()
        print("Peer list downloaded!")
        print("Adding you to the peer list...")
        cloud.add_self_to_peer_list()
        print("You have been added to the peer list!")
        print("Connecting to peers...")
        complete = True

        if complete:
            if len(self.get_peers()) >= 6:
                pl = self.get_peers()
                for x in pl:
                    try:
                        sock.connect((x[0], x[1]))
                        print(f"Connected to {sock.getpeername()}")
                    except OSError:
                        pass

        while 1:
            try:
                data = sock.recv(1024).decode()
            except OSError:
                pass

            try:
                if type(data) == bool:
                    pass
            except UnboundLocalError:
                pass

            try:
                if data == "" or data == None:
                    pass
            except UnboundLocalError:
                pass

            else:
                print('Client received:{!r}'.format(data))

        mode = None
        if mode == "G":
            self.send_graph = True
        else:
            self.send_graph = False
        if mode == "S":
            self.send_vote = True
        else:
            self.send_vote = False

        if self.send_graph == True:
            try:
                filename = "source/graph.json"
                with open(filename, "r") as f:
                    while True:
                        bytes_read = f.read()
                        sock.sendall(util.encode(bytes_read))
                        sock.sendall(util.encode("~~~"))
                        print("Everything sent successfully!")
                        break

            except FileNotFoundError:
                raise FileNotFoundError("Graph not found. Please resolve this issue before sending.")

        elif self.send_vote == True:
            self.value = None
            consensus_values = [True, False]
            self.value = random.choice(consensus_values)
            sock.send(util.encode(self.value))
            print(f"Vote sent: {self.value}")

    def add_to_info(self, s_ip, s_port):
        filename = "source/info.json"
        sending_ip_server = s_ip
        sending_port_server = s_port
        session_id = util.hash(str(s_ip + str(s_port)))[:20]
        address = [sending_ip_server, sending_port_server, session_id]
        with open(filename, 'w') as f:
            json.dump(address, f)

    def get_info(self):
        with open("source/info.json", 'r') as f:
            data = eval(f.read())
        return data

    def get_peers(self):
        return util.get_peer_list()

    def run_socket(self):
        s_thread = threading.Thread(target=self.server_functionality)
        c_thread = threading.Thread(target=self.client_functionality)
        s_thread.start()
        c_thread.start()

    def writeGraphToJSONfile(self):
        filename = "source/graph.json"
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