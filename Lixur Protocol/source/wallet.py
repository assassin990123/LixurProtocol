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
        self.wallet = cryptography.generate_and_verify_seedphrase(cryptography)
        if self.wallet == True: # If a new wallet is created
            self.alphanumeric_address = cryptography.get_address_pair(cryptography)[0]
            self.readable_address = cryptography.get_address_pair(cryptography)[1]
            self.addresses = self.alphanumeric_address, self.readable_address
        elif self.wallet == False or util.get_graph_tx_count() < 4: # If a wallet exists already and is being loaded
            self.alphanumeric_address = cryptography.get_ex_alphanumeric_address(cryptography)
            self.readable_address = cryptography.get_ex_readable_address(cryptography)
            self.addresses = self.alphanumeric_address, self.readable_address