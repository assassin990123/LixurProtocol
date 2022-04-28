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
        try:
            file = open("lixur_keystore.txt", "x")
            file.write(json.dumps(self.keystore))
            file.close()
        except FileExistsError:
            file = open("lixur_keystore.txt", "w")
            file.truncate(0)
            file.write(json.dumps(self.keystore))
            file.close()
        print('Your phrase has been generated!, your phrase is: ' + self.bold(phrase))
        print(f"Store it somewhere safe. You will need it to access your wallet. If you forget it, your funds will be lost forever.")
        print(self.bold("DO NOT SHARE IT WTH ANYONE! ") + "Whoever has your phrase will be able to " + self.bold("permanently ") +
              "have " + self.bold("unlimited ") + "access your wallet and spend your funds..." + self.bold("forever!"))
    def aes_wallet_decrypt(self, phrase_hash, keystore):
        user_input = input("Enter the decryption password for your wallet: ").replace(" ", "")
        if self.hash(user_input) == phrase_hash:
            cipher = AES.new(bytes(user_input, encoding='utf-8'), AES.MODE_EAX, b64decode(keystore['nonce'].encode('utf-8')))
            plaintext = cipher.decrypt(b64decode(keystore['cipher_text'].encode('utf-8')))
            cipher.verify(b64decode(keystore['tag'].encode('utf-8')))
            private_key = eval(plaintext.decode('utf-8'))['_']
            public_key = eval(plaintext.decode('utf-8'))['__']
            readable_address = eval(plaintext.decode('utf-8'))['___']
            alphanumeric_address = hashlib.sha256(public_key).hexdigest()
            try:
                print(f'Your public address is: {alphanumeric_address}')
                print(f'Your readable address is: {readable_address}')
                print("Successfully decrypted!")
                return private_key, public_key, alphanumeric_address, readable_address

            except NameError:
                if hash(user_input) == ks_hash:
                    print(f'Your public address is: {alphanumeric_address}')
                    print(f'Your readable address is: {readable_address}')
                    print("Successfully decrypted!")
                    return private_key, public_key, alphanumeric_address, readable_address
                else:
                    print(f'Decryption failed!, hash of input: {hash(user_input)} does not match hah of keystore: {phrase_hash}')
        else:
            while self.hash(user_input) != phrase_hash:
                print("Incorrect password, try again!")
                self.aes_wallet_decrypt(phrase_hash, keystore)

