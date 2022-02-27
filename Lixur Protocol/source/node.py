from source.util import Util
from source.graph import Graph
from collections import OrderedDict
import json
import os
import time
import hashlib
import sys
import time

class Node:
    def __init__(self, *args):
        self.neighbours = {"neighbours": []}
        self.graph = Graph()
    def send_ping(self, ip_address):
        # This is for Windows only, won't work on MacOS or Linux until the code gets upgraded :(

        exit_code = os.system(f"ping {ip_address}")
        if "0" in str(exit_code):
            print("Ping successful!")
            self.ping = True
            duration_s = end_time - start_time
        else:
            print("Ping unsuccessful or unsatisfactory...")
            print(f"The error code is {exit_code}")
            self.ping = False
        return self.ping
    def register_neighbours(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        length = len(self.neighbours["neighbours"])
        if length == 0:
            self.neighbours["neighbours"].append({"ip": ip_address, "port": port})
            print("[+] Neighbour added: %s:%d" % (ip_address, port))
            self.is_genesis_node = True
            self.neighbours["neighbours"][0].update({"genesis_node": self.is_genesis_node})
            print("[+] Registering %d neighbour..." % len(self.neighbours["neighbours"]))
            print("[+] Total nodes on the network: %d" % len(self.neighbours["neighbours"]))
            self.sync_neighbour()
        elif length > 0:
            for i in self.neighbours["neighbours"]:
                if i["ip"] == ip_address and i["port"] == port:
                    print("[+] This node is already registered...")
                    break
                elif i["ip"] != ip_address and i["port"] != port:
                    self.neighbours["neighbours"].append({"ip": ip_address, "port": port})
                    self.ip = ip_address
                    self.port = port

                    self.is_genesis_node = False
                    self.neighbours["neighbours"][0].update({"genesis_node": self.is_genesis_node})

                    listofneighbours = self.neighbours["neighbours"]
                    print("[+] Registering %d neighbours..." % len(listofneighbours))

                    for n in listofneighbours:
                        # for each new neighbour, add tuples like (("ip": "192.168.1.2"), ("port": 8080))
                        self.neighbours.update(tuple(n.items()))
                    print("[+] Total nodes on the network: %d" % len(self.neighbours["neighbours"]))

                    self.sync_neighbour()
                else:
                    print("[?] Weird input, neighbour not added")

        if len(self.neighbours["neighbours"]) == 1:
            return {'msg': '%d' % len(self.neighbours["neighbours"]) + ' node added as neighbour'}
        elif len(self.neighbours["neighbours"]) > 1:
            return {'msg': '%d' % len(self.neighbours["neighbours"]) + ' nodes added as neighbours'}
        elif len(self.neighbours["neighbours"]) == 0:
            return {'msg': 'No neighbours added'}
    def sync_neighbour(self):
        # TODO: for each ip:port pair in the self.neighbours:
        # Check if they are up/alive (maybe ping first)
        # if they are up, ask them for their Graph.
        # My note: Sync with first node for each new node?
        print("[+] Syncing with neighbours...")
        for i in self.neighbours["neighbours"]:
            print("[+] Syncing with %s:%d" % (i["ip"], i["port"]))
            ip_address_of_self = i["ip"]
            self.send_ping(ip_address_of_self)
            if self.ping is True:
                Graph = self.getGraphAsJSONdict()
            elif self.ping is False:
                pass

        alive_nodes = []
        dead_nodes = []
        for i in self.neighbours["neighbours"]:
            if self.ping is True:
                alive_nodes.append(i["ip"])
                self.alive_count = len(alive_nodes)
                self.alive_list = alive_nodes
                self.active = True
                self.active_prompt = "Active"
            elif self.ping is False:
                dead_nodes.append(i["ip"])
                self.dead_count = len(dead_nodes)
                self.dead_list = dead_nodes
                self.active = False
                self.active_prompt = "Inactive"
            if len(self.neighbours["neighbours"]) == 1 and self.ping is False: # AKA if the only node in the network is dead
                self.alive_count = 0
                self.alive_list = alive_nodes
                self.active = False
    def check_node_status(self):
        self.sync_neighbour()
        print("[+] Checking node and network status...")
        status_dict = {"[+] Message": f"You've successfully connected to the network, your IP address and port are: {self.ip_address}:{self.port}",
                   "Amount of Total Nodes On The Network ": len(self.neighbours["neighbours"]),
                   "List of Nodes On The Network ": self.neighbours["neighbours"],
                   "Is This Node The Genesis": self.neighbours["neighbours"][0]["genesis_node"],
                   "Amount of Alive Nodes On The Network ": len(self.alive_list),
                   "List of Alive Nodes On The Network ": self.alive_list,
                   "Amount of Dead Nodes On The Network ": len(self.dead_list),
                   "List of Dead Nodes On The Network ": self.dead_list,
                   "Percentage of Active Nodes On The Network ":
                        str(float(len(self.alive_list) / round(len(self.alive_list) + len(self.dead_list))) * 100) + " %",
                   "Percentage of Inactive Nodes On The Network ":
                        str(float(len(self.dead_list) / round(len(self.alive_list) + len(self.dead_list))) * 100) + " %",
                   "Node Status ": self.active_prompt,
                   "Number of Transactions on Lixur": self.graph.count_tx_number()},

        return status_dict
    def writeGraphToJSONfile(self):
        filename = "database/graph.json"
        with open(filename, 'w') as f:
            json.dump(self.getGraphAsJSONdict(), f)
    def readGraphFromJSONfile(self):
        filename = "database/graph.json"
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