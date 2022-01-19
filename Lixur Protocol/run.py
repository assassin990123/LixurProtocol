from flask import Flask, jsonify, request
from flask import send_file
import json
import socket
import networkx as nx
from flask_ngrok import run_with_ngrok as run
import matplotlib.pyplot as plt
import os
import sys
import datetime, time

# imported classes
from source.node import Node
from source.util import Util
from source.graph import Keys
from source.wallet import Wallet

# Get IP address of the host
hostname = socket.gethostname()
ip_address = str(socket.gethostbyname(hostname))

# Find an available port number for the host
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 0))
port = sock.getsockname()[1]

app = Flask(__name__)

@app.route('/node', methods=['GET', 'POST'])
def register_new_node():
    node.register_neighbours(ip_address, port)
    response = node.check_node_status()
    return jsonify(response), 201

# Might contain unneeded/redundant code
@app.route('/transactions/new', methods=['GET', 'POST'])
def new_transaction():
    response = node.graph.make_transaction(
        request.form.get('sender_public_key'),
        request.form.get('recipient_public_key'),
        request.form.get('amount'),
        request.form.get('signature'),
        request.form.get('info'),
        request.form.get('approved_tx'),
        request.form.get('nonces'),
        request.form.get('previous_hashes'))
    return jsonify(response), 201

@app.route('/wallet/address', methods=['GET', 'POST'])
def address_retrieval():
    wallet = Wallet()
    return f"Addresses of this Wallet: {str(wallet.retrieve_address_list()[0])}, {str(wallet.retrieve_address_list()[1])}"

@app.route('/wallet/balance', methods=['GET', 'POST'])
def balance_retrieval():
    wallet = Wallet()
    return "Balance of this Wallet: " + "{:,}".format(wallet.get_balance()) + " LXR"

@app.route('/', methods=['GET', 'POST'])
def show_DAG():
    serializable_format = node.getGraphAsJSONdict()
    node.writeGraphToJSONfile()
    return jsonify(serializable_format)

# Might need repair
@app.route('/dag/png', methods=['GET', 'POST'])
def get_DAG_as_png():
    serializable_format = node.getGraphAsJSONdict()
    node.writeGraphToJSONfile()

    ledger = nx.DiGraph()

    for n in serializable_format:
        print("[+] node: " + n + ", edge: " + str(serializable_format[n]['previous_hashes']))
        for x in serializable_format[n]['previous_hashes']:
            ledger.add_edge(n, x)

    lbls = {}
    for k in ledger.nodes().keys():
        lbls.update({k: k[0:3]})
    pos = nx.spring_layout(ledger)  # positions for all nodes
    nx.draw_networkx_nodes(ledger, pos, node_size=70)
    nx.draw_networkx_labels(ledger, pos, labels=lbls, font_size=8, font_family='sans-serif')
    nx.draw_networkx_edges(ledger, pos, width=2)
    # nx.draw(ledger)
    # plt.show(block=False)

    if "Graph.png" in os.listdir("."):
        print("[+] Deleting Graph.png")
        os.remove("Graph.png")

    plt.axis('off')
    plt.savefig("Graph.png", format="PNG")
    plt.clf()

    return send_file("Graph.png", mimetype='image/png')

# TODO:
# (1) When we start multiple Nodes, they both start from Genesis.
# 	 -> We need to specify the second node (or later ones) that it is not Genesis node, should not create a graph
# 	 -> Sequential nodes, can contact their neighbours (if they have one)
# 	 -> or read from a JSON file for the current state of the graph

if __name__ == '__main__':
    print("[+] Loading...")

    utils = Util()
    node = Node(utils.unique_gen())

    print("[+] Starting flask app with the following IP Address: %s, Port: %s" % (ip_address, port))
    app.run()
