import socket
import time
import threading
import hashlib
import json
from base64 import b64encode, b64decode

from flask import Flask, jsonify, request
from Crypto.Cipher import AES


class Run:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        server_ip = "170.187.204.77"
        server_port = int(input("Enter port number: \n"))
        try:
            self.s.connect((server_ip, server_port))
            print("You have connected to the server successfully!")
            while True:
                try:
                    self.data = self.s.recv(500000000).decode('utf-8')
                except ConnectionResetError:
                    raise RuntimeError("The server has shut down!")
                except ConnectionAbortedError:
                    raise RuntimeError("The server has shut down!")
                except AttributeError:
                    raise AssertionError("Either you have not connected to the server, or you just need to refresh the page you're trying to access!")
        except socket.error:
            raise RuntimeError("Your attempt to connect to the server failed!")

    def send(self, message):
        try:
            self.s.send(str(message).encode())
            return True
        except socket.error:
            raise RuntimeError("Your attempt to send a message to the server failed!")

    @staticmethod
    def bold(self, text):
        return "\033[1m" + text + "\033[0m"

    def get_graph(self):
        self.send("get_graph")
        time.sleep(0.1)
        try:
            if "index" in util.data:
                graph_ = eval(util.data)
                try:
                    with open("graph.json", "x") as f:
                        json.dump(graph_, f)
                        f.close()
                except FileExistsError:
                    with open("graph.json", "w") as f:
                        f.truncate(0)
                        json.dump(graph_, f)
                        f.close()
        except AttributeError:
            raise AssertionError("Either you have not connected to the server, or you just need to refresh the page you're trying to access!")

    @staticmethod
    def get_graph_file(self):
        with open("graph.json", "r") as f:
            graph_from_file = dict(json.load(f))
        return graph_from_file

    @staticmethod
    def aes_wallet_decrypt(self, phrase_hash, keystore):
        with open("lixur_phrase.txt", "r") as f:
            user_input = f.read().replace(" ", "")
        if hashlib.sha256(user_input.encode('utf-8')).hexdigest() == phrase_hash:
            cipher = AES.new(bytes(user_input, encoding='utf-8'), AES.MODE_EAX, b64decode(keystore['nonce'].encode('utf-8')))
            plaintext = cipher.decrypt(b64decode(keystore['cipher_text'].encode('utf-8')))
            cipher.verify(b64decode(keystore['tag'].encode('utf-8')))
            private_key = eval(plaintext.decode('utf-8'))['_']
            public_key = eval(plaintext.decode('utf-8'))['__']
            alphanumeric_address = hashlib.sha256(public_key).hexdigest()
            try:
                return private_key, public_key, alphanumeric_address

            except NameError:
                if hash(user_input) == ks_hash:
                    return private_key, public_key, alphanumeric_address
                else:
                    print(f'Decryption failed!, hash of input: {hash(user_input)} does not match hah of keystore: {phrase_hash}')

    def get_balance(self, address):
        balance = 0
        graph_data = self.get_graph_file(self)
        for tx in graph_data:
            if graph_data[tx]['sender'] == address and graph_data[tx]['recipient'] == address:
                balance += float(graph_data[tx]['amount'])
            if address == graph_data[tx]['sender']:
                balance -= float(graph_data[tx]["amount"])
            if address == graph_data[tx]["recipient"]:
                balance += float(graph_data[tx]["amount"])
        balance = float(balance)
        return balance

    def does_address_exist(self, address):
        with open('graph.json', 'r') as f:
            data = dict(json.load(f))
        addresses = []
        for x in data.values():
            addresses.append(x['sender'])
            addresses.append(x['recipient'])
        if address in addresses:
            return True
        else:
            return False

    def make_transaction(self, sender, receiver, amount, public_key, private_key):
        if amount <= 0:
            raise ValueError("You must have LXR to send!")
        else:
            arguments = {
                "sender": sender,
                "receiver": receiver,
                "amount": amount,
                "public_key": public_key,
                "private_key": private_key
            }
            self.send(arguments)
            time.sleep(2)
            util.get_graph()


app = Flask(__name__)
util = Run()


@app.route("/", methods=['GET', 'POST'])
def graph():
    util.get_graph()
    time.sleep(0.1)
    with open('graph.json', 'r') as f:
        serializable_format = dict(json.load(f))
    graph = sorted(serializable_format.items(), key=lambda x: x[1]["index"], reverse=True)
    return jsonify(graph), 201


@app.route("/stats", methods=['GET', 'POST'])
def stats():
    ledger = util.get_graph_file(util)
    unique_addresses = []
    for key in ledger:
        if ledger[key]['sender'] not in unique_addresses:
            unique_addresses.append(ledger[key]['sender'])
        if ledger[key]['recipient'] not in unique_addresses:
            unique_addresses.append(ledger[key]['recipient'])
    unique_addresses = list(set(unique_addresses))
    unique_addresses.remove("None")
    number_of_unique_addresses = len(unique_addresses) - 1
    total_amount_of_lxr = 0
    for key in ledger:
        total_amount_of_lxr += ledger[key]['amount']
    total_amount_of_lxr = "{:,}".format(total_amount_of_lxr) + " LXR"

    response = {
        "Successful Transaction Count": len(ledger.keys()),
        "Total Unique Addresses": number_of_unique_addresses,
        "Total Supply of LXR": total_amount_of_lxr,
    }
    return jsonify(response), 201


@app.route('/wallet/new', methods=['GET', 'POST'])
def new_wallet():
    util.send('new')
    time.sleep(0.5)
    if type(eval(util.data)) == tuple and "is_existing" not in locals():
        keystore = eval(util.data)[0]
        try:
            with open("lixur_keystore.txt", "x") as f:
                f.write(keystore)
                f.close()
        except FileExistsError:
            with open("lixur_keystore.txt", "w") as f:
                f.truncate(0)
                f.write(keystore)
                f.close()

        phrase = eval(util.data)[1]
        try:
            with open("lixur_phrase.txt", "x") as f:
                f.write(str(phrase))
                f.close()
        except FileExistsError:
            with open("lixur_phrase.txt", "w") as f:
                f.truncate(0)
                f.write(str(phrase))
                f.close()
        print(f"Your seedphrase for your new wallet is: {util.bold(util, str(phrase))}")
        print("Write it down, store it in a safe place as you'll need it to access your wallet. If you lose your seedphrase, you will lose access to your wallet!")
        print("Do not share it with anyone! Anyone with your seedphrase will have unlimited access over your funds, forever!")
        print("Your keystore and your phrase have been saved onto your device.")

        with open("lixur_keystore.txt", "r") as f:
            keystore_ = eval(f.read())
        wallet_info = util.aes_wallet_decrypt(util, keystore_['hash'], keystore_)
        util.make_transaction(wallet_info[2], wallet_info[2], 69420000, wallet_info[1], wallet_info[0])
    else:
        raise RuntimeError("Something went wrong! Please try again!")
    return jsonify('If you have been given your seedphrase, Go to /wallet/info to see your address and balance! If not, refresh the page and try again.')


@app.route("/wallet/load", methods=['GET', 'POST'])
def get_balance():
    with open("lixur_keystore.txt", "r") as f:
        ks = eval(f.read())
    decrypt_ks = util.aes_wallet_decrypt(util, ks['hash'], ks)
    util.get_graph()
    time.sleep(0.5)
    if util.does_address_exist(decrypt_ks[2]) == True:
        user_stats = {
            "address": decrypt_ks[2],
            "balance": f'{"{:,}".format(util.get_balance(decrypt_ks[2]))} LXR',
        }
    else:
        raise ValueError(
            "The wallet address you're trying to access does not exist on the blockchain. Refresh the page and try again, if the error persists, it means it doesn't exist at all.")
    return jsonify(user_stats)


@app.route("/transaction", methods=['GET', 'POST'])
def make_transaction():
    with open("lixur_keystore.txt", "r") as f:
        keystore = eval(f.read())
    decrypted_keystore = util.aes_wallet_decrypt(util, keystore['hash'], keystore)
    user_private_key = decrypted_keystore[0]
    user_public_key = decrypted_keystore[1]
    user_address = decrypted_keystore[2]
    if util.does_address_exist(user_address) == True:
        prep_arguments = {
            "sender": user_address,
            "receiver": input("Enter the receiver's address: "),
            "amount": float(input("Enter the amount of LXR you want to send: ")),
            "public_key": user_public_key,
            "private_key": user_private_key,
        }
        if prep_arguments['sender'] == prep_arguments['receiver']:
            raise ValueError("You cannot send LXR to yourself!")
        if prep_arguments['amount'] == None or float(prep_arguments['amount']) <= 0:
            raise ValueError("You cannot send 0 or less LXR!")
        if util.does_address_exist(prep_arguments['receiver']) == False:
            raise ValueError("The receiver's address does not exist on the blockchain! Refresh the blockchain and try again. If it still persists, it means that it doesn't "
                             "exist at all.")
        else:
            print(f"Sending {util.bold(util, str(prep_arguments['amount']))} to {util.bold(util, prep_arguments['receiver'])}...")
            util.send(prep_arguments)
            time.sleep(1.2)
            util.get_graph()
    else:
        raise ValueError("Your wallet address does not exist on the blockchain. Please try again.")
    return jsonify("The transaction has been sent! Refresh the graph and check to see if it has been validated and added to the graph!"), 200


if __name__ == "__main__":
    print("Booting up Lixur Testnet [Beta] v0.0.1...\n")
    threading.Thread(target=util.connect).start()
    time.sleep(.5)
    app.run()
