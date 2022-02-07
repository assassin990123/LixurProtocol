import hashlib
from uuid import uuid4
from p2pnetwork.node import Node

class Util:
    def __init__(self, *args):
        pass
    def hash(self, str_input):
        return hashlib.sha256(str_input.encode()).hexdigest()
    def unique_gen(self):
        return str(uuid4()).replace('-', '')
    def str_join(self, *args):
        return ''.join(map(str, args))
    def generate_ip_address(self):
        pass

class P2P(Node):
        # Python class constructor
    def __init__(self, host, port, id=None, callback=None, max_connections=0):
        super(P2P, self).__init__(host, port, id, callback, max_connections)

    def outbound_node_connected(self, connected_node):
        print("Outbound Node Connected: " + connected_node.id)

    def inbound_node_connected(self, connected_node):
        print("Inbound Node Connected: " + connected_node.id)

    def inbound_node_disconnected(self, connected_node):
        print("Inbound Node Disconnected: " + connected_node.id)

    def outbound_node_disconnected(self, connected_node):
        print("Outbound Node Disconnected: " + connected_node.id)

    def node_message(self, connected_node, data):
        print("Message from: " + connected_node.id + ": " + str(data))

    def node_disconnect_with_outbound_node(self, connected_node):
        print("Node wants to disconnect with other outbound node: " + connected_node.id)

    def node_request_to_stop(self):
        print("Node is requested to stop!")

    # OPTIONAL
    # If you need to override the Node Connection as well, you need to
    # override this method! In this method, you can initiate
    # you own NodeConnection class.

    def create_new_connection(self, connection, id, host, port):
        return MyOwnNodeConnection(self, connection, id, host, port)