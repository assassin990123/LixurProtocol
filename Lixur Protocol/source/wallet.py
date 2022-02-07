import unicodedata
import hashlib
import time
import source.graph
from source.cryptography import KeyGen as keygen
import source.graph
from Crypto.Cipher import AES
import os
import binascii
import unicodedata
from base64 import b64encode, b64decode
from source.cryptography import KeyGen as keygen
import random

# Instantiate necessary objects
cryptography = keygen()

class Wallet:

    def __init__(self):
        self.addresses = cryptography.generate_addresses(cryptography, readable=True)
        self.alphanumeric_addresses = self.addresses[0]
        self.readable_address = self.addresses[1]
        self.addresses = self.alphanumeric_addresses, self.readable_address

    def retrieve_addresses(self):
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

    def generate_and_verify_seedphrase(self):

        cryptography = keygen()

        def hash(str_input):
            return hashlib.sha256(str_input.encode()).hexdigest()

        def bold(str_input):
            return "\033[1m" + str_input + "\033[0m"

        def generate_decryption_phrase():
            with open("decrypt_words.txt", "r", encoding="utf-8") as f:
                words = f.readlines()
            word_list = []
            number = 8  # Only 4, 6 or 8 are acceptable and the higher, the more secure.
            for i in range(number):
                index = random.randint(1, 2500)
                word_list.append(words[index].strip())
            # turn the list into a string
            word_list = " ".join(word_list)
            return word_list

        new_wallet = input('Hello! Input "new" to create a new wallet, and "existing" to access an existing one: ')

        if new_wallet == "new":
            new_wallet = True
        elif new_wallet == "existing":
            new_wallet = False
        else:
            print("Invalid input")
            exit()

        if new_wallet == True:
            # Initialization Vector
            x = generate_decryption_phrase()

            with open("phrase.txt", "w", encoding="utf-8") as f:
                f.write(x)

            y = x.replace(" ", "")
            input_encrypt = cryptography.get_private_key(cryptography)
            encrypt = str(input_encrypt)
            encrypt_x = bytes(encrypt, 'utf-8')

            # Encrypt
            cipher = AES.new(bytes(y, encoding="utf-8"), AES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(encrypt_x)
            enc_dict = {
                'cipher_text': b64encode(ciphertext).decode('utf-8'),
                'nonce': b64encode(nonce).decode('utf-8'),
                'tag': b64encode(tag).decode('utf-8'),
                'hash': hash(y)
            }

            with open("lixur_keystore.txt", "w") as f:
                f.write(str(enc_dict))

            print('Your phrase has been generated!')
            print(f'Phrase: {x}')
            print(f"Store it somewhere safe. You will need it to access your wallet. If you forget it, your funds will be lost forever.")
            print(bold("DO NOT SHARE IT WTH ANYONE! ") + "Whoever has your phrase will be able to " + bold("permanently ") +
                  "have " + bold("unlimited ") + "access your wallet and spend your funds..." + bold("forever!"))
        elif new_wallet == False:
            with open("lixur_keystore.txt", "r") as f:
                keystore_dict = eval(f.read())
                ks_cipher = b64decode(keystore_dict['cipher_text'].encode('utf-8'))
                ks_nonce = b64decode(keystore_dict['nonce'].encode('utf-8'))
                ks_tag = b64decode(keystore_dict['tag'].encode('utf-8'))
                ks_hash = keystore_dict['hash']

            user_input = input("Enter the decryption password for your wallet: ").replace(" ", "")
            if hash(user_input) == ks_hash:
                cipher = AES.new(bytes(user_input, encoding='utf-8'), AES.MODE_EAX, ks_nonce)
                plaintext = cipher.decrypt(ks_cipher)
                cipher.verify(ks_tag)

            else:
                while hash(user_input) != ks_hash:
                    user_input = input("Incorrect, try again: ").replace(" ", "")
                    if hash(user_input) == ks_hash:
                        cipher = AES.new(bytes(user_input, encoding='utf-8'), AES.MODE_EAX, ks_nonce)
                        plaintext = cipher.decrypt(ks_cipher)
                        cipher.verify(ks_tag)
                        break

                cipher = AES.new(bytes(user_input, encoding='utf-8'), AES.MODE_EAX, ks_nonce)
                plaintext = cipher.decrypt(ks_cipher)
                cipher.verify(tag)

            try:
                print(f'{encrypt_x} -> {ciphertext} -> {plaintext}')
                print("Successfully decrypted!")

            except NameError:
                if hash(user_input) == ks_hash:
                    print(f'{ks_cipher} -> {plaintext}')
                    print("Successfully decrypted!")
                else:
                    print(f'Decryption failed!, hash of input: {hash(user_input)} does not match hash of keystore: {ks_hash}')

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
