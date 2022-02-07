# Lixur uses the "Falcon 1024" post quantum, lattice-based cryptography.

# Sign function signs the private keys, usage -> sign(private_key, message)
# Verify function verifies the signature, usage -> verify(public_key, message, signature)
# Generate keypair function generates the public and private keys, usage -> generate_keypair()

from pqcrypto.sign.falcon_1024 import verify, generate_keypair, sign
from hashlib import sha256
import binascii

class KeyGen:
    def __init__(self):
        self.public_key, self.private_key = generate_keypair()  # Keys are in bytes
        self.address = KeyGen.generate_addresses(self)

    @staticmethod
    def generate_addresses(self, readable=None):
        self.addresses = ([])
        alphanumeric_address = sha256(self.public_key).hexdigest()
        self.addresses.append(alphanumeric_address)
        if readable == True:
            name = input("[+] Please type in a readable address for Lixur "
                         "(Note: Do not add .lxr at the end, as it will by default & this will be permanent): ")
            while name in self.addresses:
                print("[!] This address is already in use. Please try again.")
                name = input("[-] Please type in a readable address for Lixur "
                             "(Note: Do not add .lxr at the end, as it will by default & this will be permanent): ")
            else:
                readable_address = name.lower().replace(' ', '_') + ".lxr"
                self.addresses.append(readable_address)
        addresses = self.addresses
        return addresses

    @staticmethod
    def from_private_key(private_key):
        keygen = KeyGen()
        keygen.private_key = private_key
        keygen.public_key = private_key.verify()
        keygen.address = KeyGen.generate_address(keygen.public_key)
        return keygen

    @staticmethod
    def falcon_sign(private_key, message):
        signature = sign(private_key, message.encode('utf-8'))
        return signature

    @staticmethod
    def verify_signature(public_key, signature, message):
        return verify(public_key, signature, message.encode('utf-8'))

    @staticmethod
    def get_public_key(self):
        return self.public_key

    @staticmethod
    def get_private_key(self):
        return self.private_key

