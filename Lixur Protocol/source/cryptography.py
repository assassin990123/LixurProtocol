# Lixur uses the "Falcon 1024" post quantum, lattice-based cryptography.
# Sign function signs the private keys, usage -> sign(private_key, message)
# Verify function verifies the signature, usage -> verify(public_key, message, signature)
# Generate keypair function generates the public and private keys, usage -> generate_keypair()
from pqcrypto.sign.falcon_1024 import verify, generate_keypair, sign
from hashlib import sha256
from source.util import Util as util
import binascii
import random
import os
import hashlib
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
class KeyGen:
    def __init__(self):
        self.public_key, self.private_key = generate_keypair()  # Keys are in bytes
        self.address = KeyGen.generate_addresses(self)
        self.available_addresses = []

    @staticmethod
    def add_to_address_list(self, address):
        self.addresses = ([])
        if address != None:
            self.addresses.append(address)
        else:
            pass
        return self.addresses

    @staticmethod
    def generate_addresses(self):
        self.alphanumeric_address = sha256(self.public_key).hexdigest()
        return self.alphanumeric_address

    @staticmethod
    def get_alphanumeric_address(self):
        return self.alphanumeric_address

    @staticmethod
    def get_readable_address(self):
        name = input("[+] Enter a permanent readable address for Lixur (Type '`' to cancel): ")
        if name == "`":
            print("[-] Readable Address Generation Cancelled!")
            self.readable_address = None
        else:
            while name in self.available_addresses:
                print("[!] This address is already in use! Please try again.")
                name = input("[+] Enter a permanent readable address for Lixur (Type '`' to cancel): ")
            else:
                self.readable_address = name.lower().replace(' ', '_') + ".lxr"
                self.available_addresses.append(self.readable_address)
        return self.readable_address

    @staticmethod
    def sign_tx(public_key, private_key, message):
        signature = sign(private_key, message.encode('utf-8'))
        try:
            x = verify(public_key, message.encode('utf-8'), signature)
            assert x
            hashed_signature = sha256(signature).hexdigest()
        except AssertionError:
            print("[!] Signature verification failed. Invalid or non-existent signature")
        return hashed_signature

    @staticmethod
    def get_public_key(self):
        return self.public_key

    @staticmethod
    def get_private_key(self):
        return self.private_key

    @staticmethod
    def get_address_pair(self):
        self.pair = self.alphanumeric_address, self.readable_address
        x = self.add_to_address_list(self, self.pair)
        return self.pair

    @staticmethod
    def generate_and_verify_seedphrase(self):

        def hash(str_input):
            return hashlib.sha256(str_input.encode()).hexdigest()

        def bold(str_input):
            return "\033[1m" + str_input + "\033[0m"

        def generate_decryption_phrase():
            with open("source/decrypt_words.txt", "r", encoding="utf-8") as f:
                words = f.readlines()
            word_list = []
            number = 8  # Only 4, 6 or 8 are acceptable and the higher, the more secure.
            for i in range(number):
                index = random.randint(1, 2500)
                word_list.append(words[index].strip())
            # turn the list into a string
            word_list = " ".join(word_list)
            f.close()
            return word_list

        new_wallet = input('Welcome to Lixur! Input "new" to create a new wallet, or "existing" to access an existing one: ')
        new_wallet = new_wallet.lower()

        if new_wallet == "new":
            self.is_new_wallet = True
        elif new_wallet == "existing":
            self.is_new_wallet = False
        else:
            print("Invalid input")
            exit()

        if self.is_new_wallet == True:

            x = generate_decryption_phrase()

            with open("source/phrase.txt", "w", encoding="utf-8") as f:
                f.write(x)

            y = x.replace(" ", "")

            input_encrypt = {
                "_": self.get_private_key(self),
                "__": self.get_public_key(self),
                "___": self.get_readable_address(self),
            }
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
            f.close()

            with open("source/lixur_keystore.txt", "w") as f:
                f.write(str(enc_dict))

            print('Your phrase has been generated!')
            print(f'Phrase: {x}')
            print(f"Store it somewhere safe. You will need it to access your wallet. If you forget it, your funds will be lost forever.")
            print(bold("DO NOT SHARE IT WTH ANYONE! ") + "Whoever has your phrase will be able to " + bold("permanently ") +
                  "have " + bold("unlimited ") + "access your wallet and spend your funds..." + bold("forever!"))
            f.close()

        elif self.is_new_wallet == False:
            with open("source/lixur_keystore.txt", "r") as f:
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
                cipher.verify(ks_tag)

            self.ex_private_key = eval(plaintext.decode('utf-8'))['_']
            self.ex_public_key = eval(plaintext.decode('utf-8'))['__']
            self.ex_readable_address = eval(plaintext.decode('utf-8'))['___']
            self.ex_alphanumeric_address = sha256(self.ex_public_key).hexdigest()

            try:
                print(f'Your public address is: {self.ex_alphanumeric_address}')
                print(f'Your readable address is: {self.ex_readable_address}')
                print("Successfully decrypted!")

            except NameError:
                if hash(user_input) == ks_hash:
                    print(f'Your public address is: {self.ex_alphanumeric_address}')
                    print(f'Your readable address is: {self.ex_readable_address}')
                    print("Successfully decrypted!")
                else:
                    print(f'Decryption failed!, hash of input: {hash(user_input)} does not match hah of keystore: {ks_hash}')
            f.close()
        return self.is_new_wallet

    @staticmethod
    def get_ex_private_key(self):
        with open("source/lixur_keystore.txt", "r") as f:
            keystore_dict = eval(f.read())
            ks_cipher = b64decode(keystore_dict['cipher_text'].encode('utf-8'))
            ks_nonce = b64decode(keystore_dict['nonce'].encode('utf-8'))
            ks_tag = b64decode(keystore_dict['tag'].encode('utf-8'))
            ks_hash = keystore_dict['hash']

        with open("source/phrase.txt", "r") as f:
            user_input = f.read().replace(" ", "")

        if hashlib.sha256(user_input.encode("utf-8")).hexdigest() == ks_hash:
            cipher = AES.new(bytes(user_input, encoding='utf-8'), AES.MODE_EAX, ks_nonce)
            plaintext = cipher.decrypt(ks_cipher)
            cipher.verify(ks_tag)

            self.ex_private_key = eval(plaintext.decode('utf-8'))['_']
            return self.ex_private_key
        else:
            print(f"Decryption failed!, hash of input: {hashed_input} does not match hash of keystore: {ks_hash}")

    @staticmethod
    def get_ex_public_key(self):
        with open("source/lixur_keystore.txt", "r") as f:
            keystore_dict = eval(f.read())
            ks_cipher = b64decode(keystore_dict['cipher_text'].encode('utf-8'))
            ks_nonce = b64decode(keystore_dict['nonce'].encode('utf-8'))
            ks_tag = b64decode(keystore_dict['tag'].encode('utf-8'))
            ks_hash = keystore_dict['hash']

        with open("source/phrase.txt", "r") as f:
            user_input = f.read().replace(" ", "")

        if hashlib.sha256(user_input.encode("utf-8")).hexdigest() == ks_hash:
            cipher = AES.new(bytes(user_input, encoding='utf-8'), AES.MODE_EAX, ks_nonce)
            plaintext = cipher.decrypt(ks_cipher)
            cipher.verify(ks_tag)

            self.ex_public_key = eval(plaintext.decode('utf-8'))['__']
            return self.ex_public_key
        else:
            print(f"Decryption failed!, hash of input: {hashed_input} does not match the hash of keystore: {ks_hash}")

    @staticmethod
    def get_ex_alphanumeric_address(self):
        with open("source/lixur_keystore.txt", "r") as f:
            keystore_dict = eval(f.read())
            ks_cipher = b64decode(keystore_dict['cipher_text'].encode('utf-8'))
            ks_nonce = b64decode(keystore_dict['nonce'].encode('utf-8'))
            ks_tag = b64decode(keystore_dict['tag'].encode('utf-8'))
            ks_hash = keystore_dict['hash']

        with open("source/phrase.txt", "r") as f:
            user_input = f.read().replace(" ", "")

        if hashlib.sha256(user_input.encode("utf-8")).hexdigest() == ks_hash:
            cipher = AES.new(bytes(user_input, encoding='utf-8'), AES.MODE_EAX, ks_nonce)
            plaintext = cipher.decrypt(ks_cipher)
            cipher.verify(ks_tag)

            self.ex_public_key = eval(plaintext.decode('utf-8'))['__']
            self.ex_alphanumeric_address = sha256(self.ex_public_key).hexdigest()
            return self.ex_alphanumeric_address

    @staticmethod
    def get_ex_readable_address(self):
        with open("source/lixur_keystore.txt", "r") as f:
            keystore_dict = eval(f.read())
            ks_cipher = b64decode(keystore_dict['cipher_text'].encode('utf-8'))
            ks_nonce = b64decode(keystore_dict['nonce'].encode('utf-8'))
            ks_tag = b64decode(keystore_dict['tag'].encode('utf-8'))
            ks_hash = keystore_dict['hash']

        with open("source/phrase.txt", "r") as f:
            user_input = f.read().replace(" ", "")

        if hashlib.sha256(user_input.encode("utf-8")).hexdigest() == ks_hash:
            cipher = AES.new(bytes(user_input, encoding='utf-8'), AES.MODE_EAX, ks_nonce)
            plaintext = cipher.decrypt(ks_cipher)
            cipher.verify(ks_tag)

            self.ex_readable_address = eval(plaintext.decode('utf-8'))['___']
            return self.ex_readable_address
        else:
            print(f"Decryption failed!, hash of input: {hashed_input} does not match hash of keystore: {ks_hash}")

    @staticmethod
    def get_ex_address_pair(self):
        return self.get_ex_alphanumeric_address(self), self.get_ex_readable_address(self)