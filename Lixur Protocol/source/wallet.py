import unicodedata
import hashlib
import time
import source.graph
from source.cryptography import KeyGen as keygen
import source.graph

# Instantiate necessary objects
cryptography = keygen()

class Wallet:

    def __init__(self):
        self.addresses = cryptography.generate_addresses(cryptography, readable=True)
        self.alphanumeric_addresses = self.addresses[0]
        self.readable_address = self.addresses[1]
        self.addresses = self.alphanumeric_addresses, self.readable_address

    def retrieve_address_list(self):
        return self.addresses

    def get_balance(self):
        number_of_wallet_addresses = (len(self.network_assets["list"]))
        if number_of_wallet_addresses == 0:
            self.balance = 69420000
            balance_dictionary = {frozenset(self.addresses): self.balance}
            self.network_assets["list"].append(balance_dictionary)
        elif number_of_wallet_addresses != 0:
            self.balance = 0
            balance_dictionary = {frozenset(self.addresses): self.balance}
            self.network_assets["list"].append(balance_dictionary)
        else:
            print("Something went wrong.")
        return self.balance

    def mnemonic(self):

        # Generates a mnemonic phrase using the private key
        private_key = cryptography.get_private_key()
        random_hex = binascii.hexlify(private_key)
        binary = bin(int(random_hex, 16))[800:]
        print(binary)

        index_list = []
        with open("database/words.txt", "r", encoding="utf-8") as f:
            for w in f.readlines():
                index_list.append(w.strip())
        wordlist = []
        for i in range(len(binary) // 11):
            index = int(binary[i * 11: (i + 1) * 11], 2)
            wordlist.append(index_list[index])
        phrase = " ".join(wordlist)
        seedphrase = unicodedata.normalize("NFKD", phrase)
        self.seedphrase = seedphrase
        give_seedphrase = "Your mnemonic is: " + seedphrase
        print(give_seedphrase)

    def verify_seedphrase(self):
        user_input = input("Enter your seedphrase: ")
        while user_input is not self.seedphrase:
            if user_input == seedphrase:
                print("Your seedphrase is correct!")
                break
            elif user_input is not self.seedphrase:
                print("Your seedphrase is incorrect. Please try again.")
                user_input = input("Enter your seedphrase: ")

    def transfer(self, public_key, private_key, recipient, amount):
        recipient = next(v for k, v in self.network_assets["list"] if str(recipient) in k)

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
