# import requests
# from uuid import uuid4
from flask import Flask, jsonify, request
from flask import send_file
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

# custom classes
from lib.node import Node
from lib.util import Util
from lib.wallet import Wallet as wallet

app = Flask(__name__)

@app.route('/node/register_neighbours', methods=['GET', 'POST'])
def register_new_node():
	print("register_new node")
	response = node.register_neighbours(request.get_json())
	return jsonify(response), 201
@app.route('/transactions/new', methods=['GET', 'POST'])
def make_transaction():
	# request_params = request.get_json(force=True)
	response = node.tangle.make_transaction(request.form.get('sndr_addr'),
											request.form.get('rcvr_addr'),
											request.form.get('value'))
	return jsonify(response), 201
@app.route('/wallet/balance', methods=['GET', 'POST'])
def wallet_balance():
	address = request.form.get('address')
	if address in node.wallet.getWalletAddresses():
		return "[+] Wallet balance for address [%s] is: %s " % (address, node.wallet.getbalance(address))
	else:
		return "[-] This node's wallet has no such address: %s" % address
@app.route('/wallet/addresses', methods=['GET', 'POST'])
def wallet_addresses():
	return "[+] Wallets addresses of this node: " + str(node.wallet.getWalletAddresses().keys())
@app.route('/dag', methods=['GET', 'POST'])
def show_DAG():
	serializable_format = node.getTangleAsJSONdict()
	node.writeTangleToJSONfile()
	return jsonify(serializable_format), 201
# return jsonify(node.tangle.DAG), 201
	# problem with the original code was that, DAG dictionary has Transaction Objects as values,
	# and those are not serializable as JSON objects.
	# return jsonify(node.DAG), 201
@app.route('/dag/png', methods=['GET', 'POST'])
def get_DAG_as_png():
	serializable_format = node.getTangleAsJSONdict()
	node.writeTangleToJSONfile()

	ledger = nx.DiGraph()

	for n in serializable_format:
		print("[+] node: " + n + ", edge: " + str(serializable_format[n]['pre_transactions']))
		for x in serializable_format[n]['pre_transactions']:
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
@app.route('/', methods=['GET', 'POST'])
def hello():
	return "You're at the homepage"
# print "[+] __name__: " + __name__


# TODO:
# (1) When we start multiple Nodes, they both start from Genesis.
# 	 -> We need to specify the second node (or later ones) that it is not Genesis node, should not create a tangle
# 	 -> Sequential nodes, can contact their neighbours (if they have one)
# 	 -> or read from a JSON file for the current state of the tangle
if __name__ == '__main__':
	# reload each time a code change happens (ali)
	# app.debug = True

	if len(sys.argv) <= 1:
		print("[-] ip and port number are required to run this node.\n")
		("$ python runNode.py <ip-address> <portnumber>")
		sys.exit(0)

	# Instantiate our Node
	# Instantiate Tangle

	utils = Util()

	print("[+] Node object is being created.")
	node = Node(utils.unique_gen())

	ip = sys.argv[1]
	port = sys.argv[2]

	print("[+] In main function, starting flask app on host: %s, port: %s" % (ip, port))
	app.run(host=ip, port=int(port))
