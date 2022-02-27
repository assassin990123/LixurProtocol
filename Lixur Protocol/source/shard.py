from pqcrypto.sign.falcon_1024 import verify, generate_keypair, sign
from hashlib import sha256

public_key, private_key = generate_keypair()  # Keys are in bytes
print("Public key:", public_key)
print("Private key:", private_key)

def sign_tx(public_key, private_key, message):
    signature = sign(private_key, message.encode('utf-8'))
    try:
        x = verify(public_key, message.encode('utf-8'), signature)
        assert x
        hashed_signature = sha256(signature).hexdigest()
    except AssertionError:
        print("[!] Signature verification failed. Invalid or non-existent signature")
    return hashed_signature
print(sign_tx(public_key, private_key, "Hello Wd"))
