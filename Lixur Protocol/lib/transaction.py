import time
from hashlib import sha256 as sha256

class Transaction:
    def __init__(self, sending_addr, receiving_addr, value, *args):
        # state 0: hidden, state 1: revealed
        self.state = 0
        self.weight = 1
        self.key = None
        self.pow = None
        self.data = "encrypted_info: " + sha256(str(args).encode('utf-8')).hexdigest()
        self.pre_transactions = set()
        self.time_stamp = time.time()
        self.tnx = {
            'sndr_addr': sending_addr,
            'rcvr_addr': receiving_addr,
            'value': value 
        }

    '''
            1. pre-transactions: A ref collection of transactions confirmed by the issuing node to 
            attach a new transaction to tangle

            2. post_transactions" A ref collection of post transactions that confirmed this transaction              
    '''

        # self.post_transactions = set()
    
    def height(self):
        pass

    def depth(self):
        pass

    def own_weight(self):
        return self.weight

    def cumulative_weight(self):
        pass
    def gettransactionasdict(self):
        x = self.__dict__
        x['pre_transactions'] = list(x['pre_transactions'])
        return x

"""
class TransactionEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Transaction):
            x = o.__dict__
            x['pre_transactions'] = list(x['pre_transactions'])
            return x
        else:
            return json.JSONEncoder.default(self, o)
"""