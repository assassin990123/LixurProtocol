import socket
import time
import threading
import hashlib
import json
import flask
from base64 import b64encode, b64decode
from flask import Flask, jsonify, request
from Crypto.Cipher import AES


class Run:
    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = "170.187.204.77"
        server_port = int(input("Enter port number: \n"))
        try:
            self.s.connect((server_ip, server_port))
            print("You have connected to the server successfully!")
            while True:
                try:
                    self.data = self.s.recv(500000).decode('utf-8')
                    print(self.data)
                except ConnectionResetError:
                    print("The server has shut down!")
                    exit()
        except socket.error:
            print("Your attempt to connect to the server failed!")
            exit()

    def send(self, message):
        try:
            self.s.send(str(message).encode())
            return True
        except socket.error:
            print("Your attempt to send a message to the server failed!")

    def bold(self, text):
        return "\033[1m" + text + "\033[0m"

    def get_graph(self):
        self.send("get_graph")
        time.sleep(0.1)
        if "index" in util.data:
            graph = eval(util.data)
            with open("graph.json", "w") as f:
                f.truncate(0)
                json.dump(graph, f)

    def get_graph_file(self):
        with open("graph.json", "r") as f:
            graph = dict(json.load(f))
        return graph

    def aes_wallet_decrypt(self, phrase_hash, keystore):
        with open ("lixur_phrase.txt", "r") as f:
            user_input = f.read().replace(" ", "")
        if hashlib.sha256(user_input.encode('utf-8')).hexdigest() == phrase_hash:
            cipher = AES.new(bytes(user_input, encoding='utf-8'), AES.MODE_EAX, b64decode(keystore['nonce'].encode('utf-8')))
            plaintext = cipher.decrypt(b64decode(keystore['cipher_text'].encode('utf-8')))
            cipher.verify(b64decode(keystore['tag'].encode('utf-8')))
            private_key = eval(plaintext.decode('utf-8'))['_']
            public_key = eval(plaintext.decode('utf-8'))['__']
            readable_address = eval(plaintext.decode('utf-8'))['___']
            alphanumeric_address = hashlib.sha256(public_key).hexdigest()
            try:
                return private_key, public_key, alphanumeric_address, readable_address

            except NameError:
                if hash(user_input) == ks_hash:
                    return private_key, public_key, alphanumeric_address, readable_address
                else:
                    print(f'Decryption failed!, hash of input: {hash(user_input)} does not match hah of keystore: {phrase_hash}')

    def get_balance(self, address):
        balance = 0
        graph_data = self.get_graph_file()
        for tx in graph_data:
            if graph_data[tx]['sender'] == address and graph_data[tx]['recipient'] == address:
                balance += float(graph_data[tx]['amount'])
            if address == graph_data[tx]['sender']:
                balance -= float(graph_data[tx]["amount"])
            if address == graph_data[tx]["recipient"]:
                balance += float(graph_data[tx]["amount"])
        balance = float(balance)
        return balance

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
            self.get_graph()
            self.get_graph()

app = Flask(__name__)
util = Run()


@app.route("/", methods=['GET', 'POST'])
def graph():
    util.get_graph()
    util.get_graph()
    time.sleep(0.1)
    with open('graph.json', 'r') as f:
        serializable_format = dict(json.load(f))
    graph = sorted(serializable_format.items(), key=lambda x: x[1]["index"], reverse=True)
    return jsonify(graph), 201


@app.route('/wallet', methods=['GET', 'POST'])
def main():
    msg = input("Welcome to Lixur! Input 'new' to create a new wallet or 'existing' to access an existing one: ").lower()
    if msg == "new" or msg == "existing":
        if msg == "existing":
            is_existing = True
        util.send(msg)
        time.sleep(0.5)
        if type(util.data) == str or "send" in util.data:
            if util.data == "send_ks":
                print("Your private key has been sent to your email!")
                is_existing = True
                with open("lixur_keystore.txt", "r") as f:
                    keystore = str(f.read())
                    util.send(keystore)
                    time.sleep(0.2)
            if util.data == "send_phr" or "send_phr" in util.data:
                phrase = input("Enter your decryption seedphrase to access your wallet: ")
                util.send(phrase)
                time.sleep(1)
        if type(eval(util.data)) == tuple and "is_existing" not in locals():
            keystore = eval(util.data)[0]
            try:
                with open("lixur_keystore.txt", "x") as f:
                    f.write(keystore)
                    f.close()
                    print("Your keystore has been saved to the file 'lixur_keystore.txt'!")
            except FileExistsError:
                with open("lixur_keystore.txt", "w") as f:
                    f.truncate(0)
                    f.write(keystore)
                    f.close()
                    print("Your keystore has been saved to the file 'lixur_keystore.txt'!")

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
            print(f"Your generated seedphrase for your new wallet is: {util.bold(str(phrase))}")
            print("Write it down, store it in a safe place as you'll need it to access your wallet. "
                  "If you lose your seedphrase, you will lose access to your wallet!")
            print("Do not share it with anyone! Anyone with your seedphrase will have unlimited access over your funds, forever!")
            print("You can also find your phrase saved in the file 'lixur_phrase.txt'")

            wallet_info = eval(util.data)[2]
            print(f"Your wallet has been recovered successfully! Your wallet address is: {util.bold(str(wallet_info[0]))}")
            util.make_transaction(wallet_info[0], wallet_info[0], 69420000, wallet_info[2], wallet_info[3])
            return_response = {
                "address": wallet_info[0],
                "balance": f'{"{:,}".format(util.get_balance(wallet_info[0]))} LXR',
            }
            print(f"Your address is: {util.bold(str(wallet_info[0]))}")
            print(f'Your balance is: {util.bold(str("{:,}".format(util.get_balance(wallet_info[0]))))} LXR')
            global user_info
            user_info = {
                "address": wallet_info[0],
                "balance": f'{util.bold(str("{:,}".format(util.get_balance(wallet_info[0]))))} LXR',
                "public_key": wallet_info[2],
                "private_key": wallet_info[3],
            }
        elif is_existing == True and "is_existing" in locals():
            global ex_user_info
            ex_user_info = {
                "address": eval(util.data)[0],
                "balance": f'{util.bold(str("{:,}".format(util.get_balance(str(util.data)[0]))))} LXR',
                "public_key": eval(util.data)[2],
                "private_key": eval(util.data)[3],
            }
            print(f"Your wallet address is: {util.bold(ex_user_info['address'])}")
            print(f'Your balance is: {util.bold(str("{:,}".format(util.get_balance(str(util.data)[0]))))} LXR')
            return_response = {
                "address": ex_user_info['address'],
                "balance": ex_user_info['balance'],
            }
    else:
        print("Something went wrong! Please try again!")
        exit()

    time.sleep(0.5)
    return jsonify(return_response)


@app.route("/transaction", methods=['GET', 'POST'])
def make_transaction():
    with open ("lixur_keystore.txt", "r") as f:
        keystore = eval(f.read())
    decrypted_keystore = util.aes_wallet_decrypt(keystore['hash'], keystore)
    user_private_key = decrypted_keystore[0]
    user_public_key = decrypted_keystore[1]
    user_address = decrypted_keystore[2]
    prep_arguments = {
        "sender": user_address,
        "receiver": input("Enter the receiver's address: "),
        "amount": float(input("Enter the amount of LXR you want to send: ")),
        "public_key": user_public_key,
        "private_key": user_private_key,
    }
    if prep_arguments['sender'] == prep_arguments['receiver']:
        print("You cannot send LXR to yourself!")
        exit()
    if prep_arguments['amount'] == None or float(prep_arguments['amount']) <= 0:
        print("You cannot send 0 or less LXR!")
        exit()
    print(f"{util.bold(user_address)} -> {util.bold(str(prep_arguments['amount']))} LXR -> {util.bold(prep_arguments['receiver'])}")
    util.send(prep_arguments)
    util.get_graph()
    util.get_graph()
    return jsonify("The transaction has been sent! Refresh the graph and check to see if it has been validated and added to the graph!"), 200


if __name__ == "__main__":
    threading.Thread(target=util.connect).start()
    time.sleep(.5)
    app.run()

# -----------------------------------------------------------------------------------------------------------------------------------------------------
