from base64 import b64encode, b64decode
from Crypto.Cipher import AES
import threading
import hashlib
import json

class Util:
    def __init__(self, *args):
        pass
    def hash(self, str_input):
        return hashlib.sha256(str_input.encode()).hexdigest()
    def str_join(self, *args):
        return ''.join(map(str, args))
    def get_graph(self):
        try:
            filename = "server/graph.json"
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
    def bold(self, str_input):
        return "\033[1m" + str_input + "\033[0m"
    def aes_wallet_encrypt(self, input, phrase):
        encrypt_phrase = phrase.replace(" ", "")
        cipher = AES.new(bytes(str(encrypt_phrase), encoding="utf-8"), AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(input)
        hash = self.hash(encrypt_phrase)
        self.keystore = {
            "cipher_text": b64encode(ciphertext).decode('utf-8'),
            "nonce": b64encode(nonce).decode('utf-8'),
            "tag": b64encode(tag).decode('utf-8'),
            "hash": hash
        }
        return self.keystore
    def aes_wallet_decrypt(self, input, phrase_hash, keystore):
        user_input = input.replace(" ", "")
        if self.hash(user_input) == phrase_hash:
            cipher = AES.new(bytes(user_input, encoding='utf-8'), AES.MODE_EAX, b64decode(keystore['nonce'].encode('utf-8')))
            plaintext = cipher.decrypt(b64decode(keystore['cipher_text'].encode('utf-8')))
            cipher.verify(b64decode(keystore['tag'].encode('utf-8')))
            private_key = eval(plaintext.decode('utf-8'))['_']
            public_key = eval(plaintext.decode('utf-8'))['__']
            readable_address = eval(plaintext.decode('utf-8'))['___']
            alphanumeric_address = hashlib.sha256(public_key).hexdigest()
            balance = self.get_balance(alphanumeric_address)
            try:
                return alphanumeric_address, balance, public_key, private_key

            except NameError:
                if hash(user_input) == phrase_hash:
                    return alphanumeric_address, balance, public_key, private_key
                else:
                    print(f'Decryption failed!, hash of input: {hash(user_input)} does not match hah of keystore: {phrase_hash}')
        else:
            print("Incorrect phrase" + user_input)
    def encode_data(self, data):
        return bytes(str(data), encoding="utf-8")
    def decode_data(self, data):
        return eval(data.decode("utf-8"))
