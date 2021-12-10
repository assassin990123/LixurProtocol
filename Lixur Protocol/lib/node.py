from lib.util import Util
from lib.wallet import Wallet
from lib.tangle import Tangle
import json

utils = Util()


class Node:
    def __init__(self, seed, *args):
        self.seed = seed
        self.wallet = Wallet(utils.hash(str(self.seed)))
        self.neighbours = set()

        ####
        # self.DAG = {}
        # root_transaction = Transaction('0000', 'root', 25000000000)        
        # self.attach_transaction(root_transaction, ['root'])
        self.tangle = Tangle()

    # Sample input JSON data;
    # {"neighbours": [{"ip": "localhost", "port": 8080}, {"ip": "192.168.1.2", "port": 1234}]}
    def register_neighbours(self, jsondata):
        listofneighours = jsondata["neighbours"]
        print("[+] Registering %d neighbours." % len(listofneighours))

        # https://stackoverflow.com/questions/34097959/add-a-dictionary-to-a-set-with-union
        for n in listofneighours:
            # for each new neighbour, add tuples like (("ip": "192.168.1.2"), ("port": 8080))
            self.neighbours.add(tuple(n.items()))
        print("[+] Total neighbours of node: %d" % len(self.neighbours))

        self.sync_neighbour()

        return {'msg': '%d' % len(self.neighbours) + ' nodes added as neighbours'}

        self.sync_neighbour()

        return {'msg': '%d' % len(self.neighbours) + ' nodes added as neighbours'}

    def sync_neighbour(self):
        # TODO: for each ip:port pair in the self.neighbours:
        #       - Check if they are up/alive (maybe ping first)
        #       - if they are up, ask them for their Tangle.
        print("[+] Syncing with Neighbours...")
        pass

    def writeTangleToJSONfile(self):
        filename = "db/tangledb.json"
        with open(filename, 'w') as f:
            json.dump(self.getTangleAsJSONdict(), f)

    def readTangleFromJSONfile(self):
        filename = "db/tangledb.json"
        with open(filename, 'r') as f:
            tangleJSON = json.load(f)
        return tangleJSON

    def getTangleAsJSONdict(self):
        serializable_format = {}
        for (k, v) in self.tangle.DAG.items():
            serializable_format.update({k: v.gettransactionasdict()})

        return serializable_format


"""
    def attach_transaction(self, transaction, confirmed_transactions):
        if self.is_valid_transaction(transaction):
            x = utils.str_join([transaction.time_stamp, transaction.pow, transaction.tnx['sending_addr'], transaction.tnx['receiving_addr'], transaction.tnx['value']])
            transaction.key = utils.hash(x)

            for trans in confirmed_transactions:
                transaction.pre_transactions.add(trans)

            self.DAG[transaction.key] = transaction

            # switch transaction state to revealed after 30 secs.
            # Timer(30, lambda: self.reveal(transaction), None).start()
            Timer(30, self.reveal, [transaction]).start()

            return {'msg': 'Transaction successful'}

        return {'msg': 'invalid transaction. Attachment failed'}

    def is_valid_transaction(self, transaction):
        # TODO: implement transaction validation logic
        return True

    def reveal(self, transaction):
        transaction.state = 1
        print("[+] transaction (t.key: %s) is revealed " % transaction.key)
"""
""" # moved to tangle.py

    def select_tips(self):
        available_transactions = []
        selected_transactions = []

        for key in self.DAG:
            _transaction = self.DAG[key]
            if _transaction.state == 1:
                available_transactions.append(_transaction)

        if len(available_transactions) >= 1:
            for i in range(2):
                selected_transactions.append(available_transactions[randint(0, len(available_transactions)-1)].key)

        return selected_transactions
"""

""" # moved to tangle.py

    def make_transaction(self, receiving_addr, value):
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
                self.wallet.generate_address(),
                receiving_addr,                 
                value
            )
            new_transaction.pow =  proof_of_work
            return self.attach_transaction(new_transaction, confirmed_transactions)

        return {'msg': 'transaction failed'}


    # moved to tangle.py

    def confirm_transactions(self):
        '''
            Even when a node is not making any transactions, it must participate 
            in confirming transactions in the network. A lazy node risks being dropped by its neighbour 

            Different approches to picking transactions to confirm>
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
"""