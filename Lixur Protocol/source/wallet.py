from source.cryptography import KeyGen as keygen
from source.graph import Graph, tx
from source.node import Node as node
from source.util import Util as util

# Instantiate necessary objects
cryptography = keygen()
graph = Graph()
node = node()
util = util()

class Wallet:
    def access_wallet(self):
        self.is_new_wallet = cryptography.generate_and_verify_seedphrase(cryptography)
        if self.is_new_wallet == True: # If a new wallet is created
            self.alphanumeric_address = cryptography.get_address_pair(cryptography)[0]
            self.readable_address = cryptography.get_address_pair(cryptography)[1]
            self.addresses = self.alphanumeric_address, self.readable_address
        elif self.is_new_wallet == False: # Retrieve existing wallet
            self.alphanumeric_address = cryptography.get_ex_alphanumeric_address(cryptography)
            self.readable_address = cryptography.get_ex_readable_address(cryptography)
            self.addresses = self.alphanumeric_address, self.readable_address