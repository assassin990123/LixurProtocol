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
    genesis_alphanumeric_address = genesis_keys
    genesis_private_key = cryptography.get_private_key(cryptography)
    genesis_public_key = cryptography.get_public_key(cryptography)

difficulty = 1

class tx:
    def __init__(self, sender_public_key, recipient_public_key, amount, signature, info, index):
        self.state = 0
        self.own_weight = round(1 * difficulty)
        self.cumulative_weight = 0 + self.own_weight
        self.previous_hashes = []
        self.info = ({info})
        self.timestamp = datetime.now().strftime('%Y-%m-%d, %H:%M:%S.%f EST')
        self.signature = signature
        self.recipient_public_key = recipient_public_key
        self.sender_public_key = sender_public_key
        self.amount = amount
        self.index = index + 1
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
            'sender' : self.sender_public_key,
            'recipient' : self.recipient_public_key,
            'amount': self.amount,
            'time' : self.timestamp,
            'own_weight' : self.own_weight,
            'cumulative_weight' : self.cumulative_weight,
            'tips' : self.previous_hashes,
            'index' : self.index,
            'signature' : self.signature
        })
        return transaction_dict

class Graph():

    def __init__(self, *args):
        self.graph = OrderedDict()
        self.state = 0
        while self.state != 3:

            keys = Keys()
            genesis_address = keys.genesis_alphanumeric_address
            genesis_private_key = keys.genesis_private_key
            genesis_public_key = keys.genesis_public_key

            gen_tx_one = tx(genesis_address, genesis_address, 0,
                            keygen.sign_tx(genesis_public_key, genesis_private_key, "Genesis Transaction 1"), None,
                            index=self.count_tx_number())
            self.update_cumulative_weights(gen_tx_one)
            gen_tx_key = self.attach_transaction(gen_tx_one, ["None"])
            self.state += 1

            gen_tx_two = tx(genesis_address, None, 0,
                            keygen.sign_tx(genesis_public_key, genesis_private_key, "Genesis Transaction 2"), None,
                            index=self.count_tx_number())
            self.update_cumulative_weights(gen_tx_two)
            self.attach_transaction(gen_tx_two, [gen_tx_key])
            self.state += 1

            gen_tx_three = tx(genesis_address, None, 0,
                            keygen.sign_tx(genesis_public_key, genesis_private_key, "Genesis Transaction 3"), None,
                            index=self.count_tx_number())
            self.update_cumulative_weights(gen_tx_three)
            self.attach_transaction(gen_tx_three, [gen_tx_key])
            self.state += 1
        if self.state == 3 or self.state < 3:
            pass

    def count_tx_number(self):
        tx_number = 0
        for x in self.graph:
            tx_number += 1
        return tx_number

    def attach_transaction(self, transaction, confirmed_transactions):
        if self.is_valid_transaction(transaction):
            utils = Util()
            x = utils.str_join([
                transaction.timestamp,
                transaction.sender_public_key,
                transaction.recipient_public_key,
                transaction.amount,
                transaction.previous_hashes,
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
        '''
        TODO: implement transaction validation logic.

        We first need to make sure necessary things are appended such as a valid signature, and confirmed transactions.

        We then to check if the sending wallet has enough amount if the transaction isn't void. Look through the ledger for this or we can
        use the get_balance() function to instantly determine the balance of a given sending address.

        After transaction validation has been completed, consensus has to be ran. This is where we need to implement the consensus algorithm.

        If anywhere we encounter an error, we cancel and revoke the transaction and say it's invalid and list why.
        If there is no errors, we append the transaction to the ledger.
        '''
        return True

    def confirm_transactions(self):
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

            if selected_transactions[0] == selected_transactions[1]:
                while selected_transactions[0] == selected_transactions[1]:
                    selected_transactions[1] = available_transactions[randint(0, len(available_transactions) - 1)].key

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
        # May have to add additional code for the validity of the proof, remember to add this to prevent spam

    def update_cumulative_weights(self, transaction):
        pass

    def make_transaction(self, sender_public_key, recipient_public_key, amount, signature, info):
        confirmed_transactions = self.confirm_transactions()
        if len(confirmed_transactions) >= 2:
            if recipient_public_key == None:
                recipient_public_key = "None"
            if amount == None:
                amount = 0
            if signature == None:
                print("[!] INVALID OR NON-EXISTENT SIGNATURE!")
                exit()
            else:
                new_transaction = tx(sender_public_key, recipient_public_key, amount, signature, info, index=self.count_tx_number())
                self.update_cumulative_weights(new_transaction)
                return self.attach_transaction(new_transaction, confirmed_transactions)

        return {'[-] Transaction Failed...'}











