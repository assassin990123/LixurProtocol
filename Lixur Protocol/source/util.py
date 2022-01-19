import hashlib
from uuid import uuid4


class Util:
    def __init__(self, *args):
        pass
    def hash(self, str_input):
        return hashlib.sha256(str_input.encode()).hexdigest()
    def unique_gen(self):
        return str(uuid4()).replace('-', '')
    def str_join(self, *args):
        return ''.join(map(str, args))