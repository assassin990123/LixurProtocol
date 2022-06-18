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
    def writeGraphToJSONfile(self):
        try:
            filename = "graph.json"
            with open(filename, 'w') as f:
                print(self.getGraphAsJSONdict())
                json.dump(self.getGraphAsJSONdict(), f)
        except FileNotFoundError:
            filename = "graph.json"
            with open(filename, 'w') as f:
                json.dump(self.getGraphAsJSONdict(), f)
    def readGraphFromJSONfile(self):
        filename = "graph.json"
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
