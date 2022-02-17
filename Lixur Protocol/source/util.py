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

# Code for recycling
'''
    def transfer(self, public_key, private_key, recipient, amount):
        recipient = next(v for k, v in self.network_assets["list"] if str(recipient) in k)
        # If a recipient address doesn't exist, return an error
        # I also need to verify signatures as well
        # Hash signatures and append them to the transaction

        def cryptographic_police(public_key, private_key, recipeint, amount):
            try:
                signature = sphincs_sign(private_key, bytes(f"{public_key} -> {recipient}"), 'utf-8')
                assert signature
                assert verify(public_key, bytes((f"{public_key} -> {recipient}: Amount: {amount}"), 'utf-8'), signature)
                print("[+] Transaction verified.")
            except AssertionError:
                print("[-] Transaction failed, invalid cryptographic signature.")

        if public_key in network_assets["list"].keys():
            if amount >= self.balance[balance]:
                tangle = Tangle()
                tangle.make_transaction()
                cryptographic_police(public_key, private_key, recipient, amount)
                self.addresses[balance] -= amount
                recipient[balance] += amount
                print("[+] Withdraw Successful. Current Balance: (%s)" % str(self.addresses[address]))
                return self.addresses[balance]
            else:
                print("[-] Insufficient Funds")
                return None
        else:
            print("[-] This wallet does not have such an address!! (%s)" % address)
            return None
'''