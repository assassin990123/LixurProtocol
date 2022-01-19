import time
from hashlib import sha256 as sha256
import time
from datetime import datetime
import hashlib

class tx:
    def __init__(self, sender_public_key, recipient_public_key, amount, signature, tx_id, approved_tx, nonces, previous_hashes):
        start_time = time.time()
        self.tx_id = tx_id
        self.own_weight = 1
        self.cumulative_weight = 0
        self.nonces = nonces
        self.previous_hashes = previous_hashes
        self.approved_tx = approved_tx,
        self.payload = ''
        self.timestamp = datetime.utfnow().strftime('%Y-%m-%d, %H:%M:%S.%f EST')
        self.signature = signature
        self.recipient_public_key = recipient_public_key
        self.sender_public_key = sender_public_key
        self.amount = amount
        time.sleep(0.0000001)
        end_time = time.time()
        time_interval = end_time - start_time
        self.finality_time = (str(float(time_interval * 1000)) + " ms")
    def hash_data(data):
        data = str(data).encode('utf-8')
        h = hashlib.new('sha256')
        h.update(data)
        return h.hexdigest()
    def get_hash(self):
        return hash_data(self.get_transaction_dict())
    def get_transaction_dict(self):
        transaction_dict = OrderedDict({
            'transaction' : (f'{self.sender_public_key} => {self.recipient_public_key}'),
            'amount': self.amount,
            'time' : self.timestamp,
            'finality_time' : self.finality_time
        })





