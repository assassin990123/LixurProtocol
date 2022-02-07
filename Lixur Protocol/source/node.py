from source.util import Util
from source.graph import Graph
import json
import os
import time
import hashlib
import sys
import time
import util

class Node:
    def __init__(self, ip_address, port, *args):
        self.neighbours = {"neighbours": []}
        self.graph = Graph()
        self.node_id = util.hash(ip_address + port)[:24]
        self.ip_address = ip_address
        self.port = port


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
        return serializable_format
