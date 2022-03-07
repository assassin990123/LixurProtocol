import random
from collections import Counter
from numpy import array as nparray
import time

# Consensus takes an average of 2.736 seconds to reach, and this is with a node count of 10,000. Also, 

consensus_values = nparray([True, False])
max_rounds = 25

class Node:
    def __init__(self, id, value=None, peer_connections=9, rounds=max_rounds, peers=[], alpha=0.5):
        self.id = id
        self.value = value
        self.peer_connections = peer_connections
        self.rounds = rounds
        self.peers = peers
        self.alpha = alpha

    def on_query(self, value):
        if self.value is None:
            self.value = value
        return self.value

    def slush_query(self, all_nodes):
        self.peers = random.sample(all_nodes, self.peer_connections)
        value_estimate = [peer.on_query(self.value) for peer in self.peers]
        self.counter = Counter(value_estimate)
        return self.counter, self.slush_result()

    def slush_result(self):
        for value in self.counter:
            if self.counter[value] > self.alpha * self.peer_connections:
                return value
        raise Exception("Slush did not return any value!")

    def slush_update(self):
        self.value = self.slush_result()
        return self.value

all_nodes = [Node(x, random.choice(consensus_values)) for x in range(10000)]
node_count = len(all_nodes)

def see_split():
    value_counter = {}
    for value in consensus_values:
        value_counter[value] = 0
    for node in all_nodes:
        value_counter[node.value] += 1
    return value_counter

def run_slush_round():
    for node in all_nodes:
        node.slush_query(all_nodes)
    for node in all_nodes:
        node.slush_update()
    return see_split()

def consensus_reached():
    var_1 = consensus_values[0]
    var_2 = consensus_values[1]
    while run_slush_round() != {var_1: node_count, var_2: 0} or run_slush_round() != {var_1: 0, var_2: node_count}:
        pass
        if run_slush_round() == {var_1: node_count, var_2: 0} or run_slush_round() == {var_1: 0, var_2: node_count}:
            return True

def run_consensus():
    for x in range(max_rounds):
        run_slush_round()
        consensus = consensus_reached()
        if consensus == True:
            break


