from lib.util import Util
from lib.transaction import Transaction
from random import randint
from threading import Timer
from collections import OrderedDict
import networkx as nx

utils = Util()


class Tangle(object):
    def __init__(self, isgenesis=True, *args):
        # represent the "sites" containing transactions
        # self.tngl = nx.DiGraph()

        if isgenesis:
            self.DAG = OrderedDict()
            genesis_tx = Transaction('genesis_address1.lxr', 'genesis_address1.lxr', 0)
            genesis_tx_key = self.attach_transaction(genesis_tx, ['genesis_tx'])

            founding_txA = Transaction('genesis_address1.lxr', 'genesis_address2.lxr', 0)
            self.attach_transaction(founding_txA, [genesis_tx_key])

            founding_txB = Transaction('genesis_address1', 'genesis_address3.lxr', 0)
            self.attach_transaction(founding_txB, [genesis_tx_key])

        else:
            print("[+] Genesis tangle is already done, connect and sync from neighbours")

    def str_join(self, *args):
        return ''.join(map(str, args))

    def attach_transaction(self, transaction, confirmed_transactions):
        if self.is_valid_transaction(transaction):
            x = utils.str_join([
                transaction.time_stamp,
                transaction.pow,
                transaction.tnx['sndr_addr'],
                transaction.tnx['rcvr_addr'],
                transaction.tnx['value']])
            transaction.key = utils.hash(x)

            for trans in confirmed_transactions:
                transaction.pre_transactions.add(trans)

            self.DAG.update({transaction.key: transaction})
            # return transaction

            # switch transaction state to revealed after 30 secs.
            # Timer(30, lambda: self.reveal(transaction), None).start()
            Timer(5, self.reveal, [transaction]).start()

            print(str({'msg': 'Transaction successful. Will be revealed in 5 seconds'}))
            return transaction.key

        print(str({'msg': '[!!!] invalid transaction. Attachment failed'}))
        return None

    def is_valid_transaction(self, transaction):
        # TODO: implement transaction validation logic
        # we need to check if the sending wallet has enough amount.
        # also calculate the hash value of transaction to verify it is correct.
        return True

    def reveal(self, transaction):
        transaction.state = 1
        print("[+] transaction (t.key: %s) is revealed " % transaction.key)

    # I believe when you make a transaction, you can only use your wallet's address as sender
    def make_transaction(self, sending_addr, receiving_addr, value):
        '''
            1. Pick at least two transactions in Tangle to confirm
            2. Check picked transactions for conflict
            3. Approve non conflicting transactions
            4. Perform proof of work
            5. Send transaction to tangle
        '''
        confirmed_transactions = self.confirm_transactions()

        if len(confirmed_transactions) >= 2:
            proof_of_work = self.proof_of_work(''.join(confirmed_transactions))
            new_transaction = Transaction(
                # self.wallet.generate_address(),
                sending_addr,
                receiving_addr,
                value
            )
            new_transaction.pow = proof_of_work
            return self.attach_transaction(new_transaction, confirmed_transactions)

        return {'msg': 'transaction failed'}

    def confirm_transactions(self):
        '''
            Even when a node is not making any transactions, it must participate
            in confirming transactions in the network. A lazy node risks being dropped by its neighbour

            Different approaches to picking transactions to confirm>
            1. Randomly pick any N visible transactions

            2. Pick r.N/n transactions.
            r=rate of new transaction attachment to Tangle.
            N=number of visible transactions.
            n=number of neighbour nodes.

            we will pick the naive one.
            TODO: check the validity of the PoW of selected transactions
        '''

        '''
            Select tips and assume the transactions are non-conflicting.
        '''
        return self.select_tips()

    def select_tips(self):
        available_transactions = []
        selected_transactions = []

        for key in self.DAG:
            _transaction = self.DAG[key]
            if _transaction.state == 1:
                available_transactions.append(_transaction)

        if len(available_transactions) >= 1:
            for i in range(2):
                selected_transactions.append(available_transactions[randint(0, len(available_transactions) - 1)].key)

        return selected_transactions

    def proof_of_work(self, str_input):
        proof = 0
        while self.is_valid_proof(str_input, proof) is False:
            proof += 1
        print("[+] Proof of Work found!! Proof: %d, str_input: %s" % (proof, str_input))
        return proof

    def is_valid_proof(self, str_input, proof):
        result = utils.hash(str_input + str(proof))
        return result.count("00") >= 2 and result[-4:] == "0000"
