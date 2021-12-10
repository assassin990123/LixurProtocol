from lib.util import Util
# from util import Util
from flask import request
utils = Util()

class Wallet:
    def __init__(self, seed):
        self.seed = seed
        self.addresses = {}
        self.generate_address()
    def generate_address(self):
        name = input("[+] Please type in a readable address for Lixur "
                     "(Note: Do not add .lxr at the end, as it will by default & this will be permanent): ")
        readable_address = name.lower() + ".lxr"
        address = utils.hash(str(self.seed) + str(len(self.addresses)))
        user_addresses = [address, readable_address]
        balance = "{:,}".format(69420000) + " LXR"
        for address in user_addresses:
            self.addresses[address] = balance
        return user_addresses
    def getWalletAddresses(self):
        return self.addresses
    def getbalance(self, address):
        if address in self.addresses.keys():
            return self.addresses[address]
        else:
            print("[-] This wallet does not have such an address!! (%s)" % address)
            return None
    def send(self, address, amount):
        if address in self.addresses.keys():
            if amount <= self.addresses[address]:
                self.addresses[address] = "{:,}".format(int(self.addresses[address].replace(",", "")) - int(amount.replace(",", "")))
                print("[+] You have successfully sent %s to %s" % (amount, address))
                return True
            else:
                print("[-] You do not have enough funds to send %s to %s" % (amount, address))
                return False
        else:
            print("[-] This wallet does not have such an address!! (%s)" % address)
            return False
    def receive(self, address, amount):
        if address in self.addresses.keys():
            self.addresses[address] = "{:,}".format(int(self.addresses[address].replace(",", "")) + int(amount.replace(",", "")))
            print("[+] You have successfully received %s from %s" % (amount, address))
            return True
        else:
            print("[-] This wallet does not have such an address!! (%s)" % address)
            return False

# how to use wallet.py
# wallet = Wallet("seed")
# wallet.generate_address()
# wallet.getbalance("address")
# wallet.send("address", "amount")
# wallet.receive("address", "amount")
# wallet.getWalletAddresses()
# wallet.getbalance("address")
# wallet.send("address", "amount")
# wallet.receive("address", "amount")
# wallet.getWalletAddresses()

# how to send LXR
# wallet.send("address", "amount")

# how to receive LXR
# wallet.receive("address", "amount")

# how to send LXR using Flask
# @app.route('/send', methods=['POST'])
# def send():
#     address = request.form['address']
#     amount = request.form['amount']
#     wallet.send(address, amount)
#     return "Success"

# how to receive LXR using Flask
# @app.route('/receive', methods=['POST'])
# def receive():
#     address = request.form['address']
#     amount = request.form['amount']
#     wallet.receive(address, amount)
#     return "Success"
