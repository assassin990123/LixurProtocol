import socket
import time
import threading
import hashlib
import json
from base64 import b64encode, b64decode

from flask import Flask, jsonify, request
from Crypto.Cipher import AES
from cryptography import KeyGen
import graph
from node import Node
from numba import jit

crypto = KeyGen()
node = Node()

app = Flask(__name__)

@jit(forceobj=True)
@app.route('/tps', methods=['GET', 'POST'])
def new_transaction():
    oldtime = time.time()
    counter = 0
    while True:
        prk = crypto.generate_keys()[1]
        pub = crypto.generate_keys()[0]
        alp = crypto.generate_keys()[2]
        response = node.graph.make_transaction(alp, None, 0, crypto.sign_tx(pub, prk, "Lixur"))
        counter += 1

        if time.time() - oldtime > 1:
            print(f'Lixur TPM: {counter}, Lixur Approximate TPS: {counter}')
            break

    return jsonify(f'Lixur TPM: {counter}, Lixur Approximate TPS: {counter/60}')




@app.route('/', methods=['GET', 'POST'])
def graph():
    node.refresh()
    return jsonify(node.getGraphAsJSONdict())
if __name__ == "__main__":
    app.run()