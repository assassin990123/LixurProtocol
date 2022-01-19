import networkx as nx
from source.util import Util
from random import randint
from collections import OrderedDict
import time
from datetime import datetime
import binascii
import hashlib
from uuid import uuid4
from source.cryptography import KeyGen as keygen
cryptography = keygen()

class Keys:
    genesis_keys = cryptography.generate_addresses(keygen())

    genesis_alphanumeric_address = genesis_keys[0]

    # The following are the keys for the genesis block in bytes
    genesis_private_key = cryptography.get_private_key(keygen())
    genesis_public_key = cryptography.get_public_key(keygen())

difficulty = 1
walletList = []

class tx:
    def __init__(self, sender_public_key, recipient_public_key, amount, signature, info, approved_tx, nonces, previous_hashes):
        self.state = 0
        self.own_weight = round(1 * difficulty)
        self.cumulative_weight = 0 + self.own_weight
        self.nonces = nonces
        self.previous_hashes = []
        self.info = ({info})
        self.timestamp = datetime.utcnow().strftime('%Y-%m-%d, %H:%M:%S.%f UTC')
        self.signature = signature
        self.recipient_public_key = recipient_public_key
        self.sender_public_key = sender_public_key
        self.amount = amount
    def previous(self):
        x = self.__dict__
        x['previous_hashes'] = list(x['previous_hashes'])
        return x
    def hash_data(data):
        data = str(data).encode('utf-8')
        h = hashsourcenew('sha256')
        h.update(data)
        return h.hexdigest()
    def get_hash(self):
        return hash_data(self.get_transaction_dict())
    def get_transaction_dict(self):
        transaction_dict = OrderedDict({
            'transaction' : (f'{self.sender_public_key} → {self.recipient_public_key}'),
            'amount': self.amount,
            'time' : self.timestamp,
            'own_weight' : self.own_weight,
            'cumulative_weight' : self.cumulative_weight,
            'tips' : self.previous_hashes,
        })
        return transaction_dict

def verify_falcon_signature(public_key, message, signature):
    try:
        assert keygen.verify_signature(public_key_bytes, message, signature)
        valid_signature = True
        return signature
    except AssertionError:
        valid_signature = False
        return signature

class Graph():

    def __init__(self, *args): # Generates a genesis transaction
        self.graph = OrderedDict()
        self.state = 0
        while self.state != 3:

            keys = Keys()
            genesis_public_key = keys.genesis_alphanumeric_address
            genesis_private_key = keys.genesis_private_key

            gen_tx_one = tx(genesis_public_key, genesis_public_key, 0,
                            keygen.falcon_sign(genesis_private_key, "Genesis Transaction 1"), None, None, nonces=0,previous_hashes = None)
            self.update_cumulative_weights(gen_tx_one)
            gen_tx_key = self.attach_transaction(gen_tx_one, ["None"])
            self.state += 1

            gen_tx_two = tx(genesis_public_key, None, 0,
                            keygen.falcon_sign(genesis_private_key, "Genesis Transaction 2"), None, None, nonces=0, previous_hashes = None)
            self.update_cumulative_weights(gen_tx_two)
            self.attach_transaction(gen_tx_two, [gen_tx_key])
            self.state += 1

            gen_tx_three = tx(genesis_public_key, None, 0,
                            keygen.falcon_sign(genesis_private_key, "Genesis Transaction 3"), None, None, nonces=0, previous_hashes = None)
            self.update_cumulative_weights(gen_tx_three)
            self.attach_transaction(gen_tx_three, [gen_tx_key])
            self.state += 1
        if self.state == 3 or self.state < 3:
            print("[+] Genesis transactions have already been done, connect and sync from neighbours")
            pass

    def attach_transaction(self, transaction, confirmed_transactions):
        if self.is_valid_transaction(transaction):
            utils = Util()
            x = utils.str_join([
                transaction.timestamp,
                transaction.sender_public_key,
                transaction.recipient_public_key,
                transaction.amount,
                transaction.previous_hashes
            ])
            transaction.key = utils.hash(x)
            self.tx_key = transaction.key

            for tx in confirmed_transactions:
                transaction.previous_hashes.append(tx)

            self.graph.update({transaction.key: transaction})
            return self.tx_key

            self.state += 1
        print(str({'[!] Invalid transaction. Attachment failed'}))
        return None

    def is_valid_transaction(self, transaction):
        # TODO: implement transaction validation logic
        # we need to check if the sending wallet has enough amount.
        # also calculate the hash value of transaction to verify it is correct.

        # I am assuming this is to make sure that the balance is valid.
        # This is where we need to implement the consensus algorithm.

        # I don't know if we implement the consensus algorithm in the is_valid_transaction function
        # or the confirm_transaction function.

        # When a new wallet is made, a transaction needs to be made to itself of it initial balance
        return True

    def confirm_transactions(self):
        '''
            Even when a node is not making any transactions, it must participate
            in confirming transactions in the network. A lazy node risks being dropped by its neighbour

            Different approaches to picking transactions to confirm>
            1. Randomly pick any N visible transactions

            2. Pick r.N/n transactions.
            r=rate of new transaction attachment to graph.
            N=number of visible transactions.
            n=number of neighbour nodes.

            we will pick the naive one.
            TODO: check the validity of the PoW of selected transactions

            I am assuming consensus is here

        '''

        '''
            Select tips and assume the transactions are non-conflicting. 
            We will have to resolve this later to check if they are conflicting.
        '''
        return self.select_tips()

    def select_tips(self):
        available_transactions = []
        selected_transactions = []

        tip_quantity = 2

        for key in self.graph:
            _transaction = self.graph[key]
            available_transactions.append(_transaction)

        if len(available_transactions) >= 1:
            for i in range(tip_quantity):
                selected_transactions.append(available_transactions[randint(0, len(available_transactions) - 1)].key)

        return selected_transactions[0], selected_transactions[1]

    def puzzle(self, str_input):
        proof = 0
        while self.is_valid_proof(str_input, proof) is False:
            proof += 1
        print("[+] Puzzle Solved! Proof: %d, str_input: %s" % (proof, str_input))
        return proof

    def is_valid_proof(self, str_input, proof):
        result = utils.hash(str_input + str(proof))
        return result.count("00") >= 2 and result[-4:] == "0000"
    #   May have to add additional code for the validity of the proof

    def update_cumulative_weights(self, transaction):
        pass

    def make_transaction(self, sender_public_key, recipient_public_key, amount, signature, info, approved_tx, nonces, previous_hashes):
        '''
            1. Pick at least two transactions in graph to confirm
            # 2. Check picked transactions for conflict
            # 3. Approve non conflicting transactions
            4. Perform proof of work
            5. Send transaction to graph
        '''
        confirmed_transactions = self.confirm_transactions()
        if len(confirmed_transactions) >= 2:
            self.approved_tx = self.confirm_transactions()
            approved_tx = self.approved_tx
            new_transaction = tx(sender_public_key, recipient_public_key, amount, info, signature, approved_tx, nonces,
            previous_hashes)
            self.update_cumulative_weights(new_transaction)
            return self.attach_transaction(new_transaction, confirmed_transactions)

        return {'[-] Transaction Failed...'}




