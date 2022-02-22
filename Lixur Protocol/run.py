import hashlib

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
from source.graph import Keys, Graph
from source.wallet import Wallet
from source.cryptography import KeyGen as keygen

app = Flask(__name__)
cryptography = keygen()

@app.route('/node', methods=['GET', 'POST'])
def register_new_node():
    node.register_neighbours(ip_address, port)
    response = node.check_node_status()
    return jsonify(response), 201

@app.route('/transactions/new', methods=['GET', 'POST'])
def new_transaction():
    private_key = cryptography.get_ex_private_key(cryptography)
    public_key = cryptography.get_ex_public_key(cryptography)
    alphanumeric_address = cryptography.get_ex_alphanumeric_address(cryptography)

    if private_key and public_key != None:
        response = node.graph.make_transaction(
            alphanumeric_address,
            request.form.get('recipient_public_key'),
            request.form.get('amount'),
            cryptography.sign_tx(public_key, private_key, "Lixur"),
            request.form.get('info'))
    else:
        return jsonify("[-] Private key or public key is not found "), 400

    return jsonify(response), 201

@app.route('/wallet', methods=['GET', 'POST'])
def address_retrieval():
    wallet = Wallet()
    wallet.access_wallet()

    if wallet.access_wallet() == True:
        node.graph.make_transaction(
        wallet.retrieve_addresses()[0],
        wallet.retrieve_addresses()[0],
        69420000,
        cryptography.sign_tx(cryptography.get_public_key(cryptography), cryptography.get_private_key(cryptography), "Lixur"),
        None)
        node.refresh()
        print("[+] Genesis Wallet created")
    else:
        node.graph.make_transaction(
            cryptography.get_alphanumeric_address(cryptography),
            cryptography.get_alphanumeric_address(cryptography),
            21000000, cryptography.sign_tx(cryptography.get_public_key(cryptography), cryptography.get_private_key(cryptography), "Lixur"),
            None)
        node.refresh()

    response = {
        "alphanumeric_address": wallet.retrieve_addresses()[0],
        "readable_address": wallet.retrieve_addresses()[1],
        "balance": "{:,}".format(wallet.get_balance(wallet.retrieve_addresses()[0])) + " LXR"
    }

    return jsonify(response), 201

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    graph = Graph()
    ledger = utils.get_graph()
    unique_addresses = []
    for key in ledger:
        unique_addresses.append(ledger[key]['sender'])
        unique_addresses.append(ledger[key]['recipient'])
    unique_addresses = list(set(unique_addresses))
    unique_addresses.remove("None")
    unique_addresses.pop()
    number_of_unique_addresses = len(unique_addresses)
    total_amount_of_lxr = 0
    for key in ledger:
        total_amount_of_lxr += ledger[key]['amount']
    total_amount_of_lxr = "{:,}".format(total_amount_of_lxr) + " LXR"

    try:
        failed_transactions = len(graph.get_failed_transactions())
    except TypeError:
        failed_transactions = None

    response = {
    "Successful Transaction Count": utils.get_graph_tx_count(),
    "Total Unique Addresses" : number_of_unique_addresses,
    "Total Supply of LXR" : total_amount_of_lxr,
    "Pending Transaction Count": len(graph.get_pending_transactions()),
    "Failed Transaction Count": failed_transactions
    }

    return jsonify(response), 201

@app.route('/', methods=['GET', 'POST'])
def show_DAG():
    serializable_format = node.getGraphAsJSONdict()
    node.refresh()
    return jsonify(serializable_format), 201

if __name__ == '__main__':
    # print("Loading Lixur Testnet Beta Version 1.0.0")
    utils = Util()
    node = Node(utils.unique_gen())
    app.run()