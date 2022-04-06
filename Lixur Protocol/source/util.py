from base64 import b64encode, b64decode
import hashlib
from uuid import uuid4
import sys
import json
import random
import socket
import os
import threading

class Util:
    def __init__(self, *args):
        pass
    def hash(self, str_input):
        return hashlib.sha256(str_input.encode()).hexdigest()
    def unique_gen(self):
        return str(uuid4()).replace('-', '')
    def str_join(self, *args):
        return ''.join(map(str, args))
    def assemble_graph(self, list):
        assembled = ''
        for x in range(len(list)):
            assembled += list[x]
        return str(assembled)
    def get_keystore(self):
        try:
            filename = "lixur_keystore.txt"
            with open(filename, "r") as f:
                keystore_dict = eval(f.read())
                ks_cipher = b64decode(keystore_dict['cipher_text'].encode('utf-8'))
                ks_nonce = b64decode(keystore_dict['nonce'].encode('utf-8'))
                ks_tag = b64decode(keystore_dict['tag'].encode('utf-8'))
                ks_hash = keystore_dict['hash']
                return ks_cipher, ks_nonce, ks_tag, ks_hash
        except FileNotFoundError:
            try:
                filename = "source/lixur_keystore.txt"
                with open(filename, "r") as f:
                    keystore_dict = eval(f.read())
                    ks_cipher = b64decode(keystore_dict['cipher_text'].encode('utf-8'))
                    ks_nonce = b64decode(keystore_dict['nonce'].encode('utf-8'))
                    ks_tag = b64decode(keystore_dict['tag'].encode('utf-8'))
                    ks_hash = keystore_dict['hash']
                    return ks_cipher, ks_nonce, ks_tag, ks_hash
            except FileNotFoundError:
                raise FileNotFoundError("Keystore not found.")
    def get_phrase(self):
        try:
            filename = "phrase.txt"
            with open(filename, "r") as f:
                user_input = f.read().replace(" ", "")
                return user_input
        except FileNotFoundError:
            try:
                filename = "source/phrase.txt"
                with open(filename, "r") as f:
                    user_input = f.read().replace(" ", "")
                    return user_input
            except:
                raise FileNotFoundError("Phrase not found.")
    def get_graph(self):
        try:
            filename = "source/graph.json"
            with open(filename, 'r') as f:
                graph_data = dict(json.load(f))
            return graph_data
        except FileNotFoundError:
            try:
                filename = "graph.json"
                with open(filename, 'r') as f:
                    graph_data = dict(json.load(f))
                return graph_data
            except FileNotFoundError:
                raise FileNotFoundError("Graph not found.")
    def get_graph_tx_count(self):
        try:
            graph_data = self.get_graph()
            return len(graph_data.keys())
        except TypeError:
            graph_data = self.get_graph(self)
            return len(graph_data.keys())
        except FileNotFoundError:
            raise FileNotFoundError("Graph not found.")
    def get_appearances(self, address):
        appearances = 0
        graph_data = self.get_graph()
        for tx in graph_data:
            if address == graph_data[tx]['sender'] or address == graph_data[tx]['recipient']:
                appearances += 1
        return appearances
    def get_balance(self, address):
        balance = 0
        graph_data = self.get_graph()
        for tx in graph_data:
            if graph_data[tx]['sender'] == address and graph_data[tx]['recipient'] == address:
                balance += float(graph_data[tx]['amount'])
            if address == graph_data[tx]['sender']:
                balance -= float(graph_data[tx]["amount"])
            if address == graph_data[tx]["recipient"]:
                balance += float(graph_data[tx]["amount"])
        balance = float(balance)
        return balance
    def thread(self, func, *args):
        thread = threading.Thread(target=func, args=args)
        thread.start()
        return thread
    def get_peer_list(self):
        with open("source/peers.txt", 'r') as f:
            data = eval(f.read())
        return data
    def encode(self, data):
        return bytes(str(data), encoding='utf-8')
    def decode(self, data):
        return eval(data.decode("utf-8"))