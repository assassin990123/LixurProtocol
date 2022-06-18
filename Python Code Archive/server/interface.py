from flask import Flask, jsonify

# imported classes
from node import Node
from util import Util
from graph import Graph
from cryptography import KeyGen as keygen

app = Flask(__name__)
cryptography = keygen()
node = Node()
util = Util()
graph = Graph()


@app.route('/stats', methods=['GET', 'POST'])
def stats():
    graph = Graph()
    ledger = util.get_graph()
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
        "Successful Transaction Count": util.get_graph_tx_count(),
        "Total Unique Addresses": number_of_unique_addresses,
        "Total Supply of LXR": total_amount_of_lxr,
        "Pending Transaction Count": len(graph.get_pending_transactions()),
        "Failed Transaction Count": failed_transactions
    }

    return jsonify(response), 201


@app.route('/', methods=['GET', 'POST'])
def show_DAG():
    serializable_format = util.get_graph()
    for (k, v) in serializable_format.items():
        sort_by = "index"  # Options are: "index", "amount", "own_weight" or "timestamp"
    serializable_format = sorted(serializable_format.items(), key=lambda x: x[1][sort_by], reverse=True)
    return jsonify(serializable_format), 201

if __name__ == '__main__':
    util.thread(node.server_functionality)
    util.thread(app.run)
