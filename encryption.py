'''
Author: Mrx
Date: 2023-03-18 17:19:59
LastEditors: Mrx
LastEditTime: 2023-03-19 12:52:13
FilePath: \cs271_final_project\encryption.py
Description: 

Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def generate_dictionary_key(clientlist, dic_id, client_id):
    client_id = str(client_id)
    dic_id = str(dic_id)
    KEY_DIR = "keys/" + client_id +'/'
    # Generate a new RSA key pair for the dictionary
    dictionary_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024
    )
    dictionary_public_key = dictionary_private_key.public_key()

    public_key_bytes = dictionary_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    private_key_bytes = dictionary_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    private_key = dic_id

    with open(KEY_DIR + dic_id + "_public.pem", "wb") as f:
        f.write(public_key_bytes)
    # client_private_key = load_private_key(client_id, client_id)
    # decrypt_private_key = decrypt_message(local_private_key_bytes, client_private_key)
    # print(decrypt_private_key)
    with open(KEY_DIR + dic_id + "_private.pem", "wb") as f:
        f.write(private_key_bytes)
    # private_key_bytes = str(private_key_bytes)

    # Encrypt the dictionary's private key for each member
    member_keys = {}
    for client in clientlist:
        client_public_key = load_public_key(client, client)
        # print(private_key_bytes)
        # private_key_bytes = 'fuck'
        # print(client_public_key)
        encrypted_private_key = encrypt_message(private_key, client_public_key)
        # encrypted_private_key = encrypt_message(private_key, client_public_key)
        member_keys[client] = encrypted_private_key
    key = {}

    key['dictionary_public_key'] = public_key_bytes
    key['member_keys'] = member_keys

    return public_key_bytes, private_key_bytes, member_keys

    # The encrypted private keys for each member can be sent to the corresponding member

    # The member can then decrypt their private key with their own private key


def store_dictionary_parameter(dic_id):
    pass
    # local_private_key_bytes = member_keys[int(client_id)]
    # print(local_private_key_bytes)
    # with open(KEY_DIR + dic_id + "_public.pem", "wb") as f:
    #     f.write(public_key_bytes)
    # # client_private_key = load_private_key(client_id, client_id)
    # # decrypt_private_key = decrypt_message(local_private_key_bytes, client_private_key)
    # # print(decrypt_private_key)
    # with open(KEY_DIR + dic_id + "_private.pem", "wb") as f:
    #     f.write(bytes(private_key_bytes))




# Define the directory where the keys are stored
# KEY_DIR = "keys/" + client_id +'/'

def load_private_key(client_id, file_name):
    client_id = str(client_id)
    file_name = str(file_name)
    # Load the private key from the file based on the client ID
    with open("keys/" + client_id + '/' + file_name + "_private.pem", "rb") as f:
        private_key_bytes = f.read()
        private_key = serialization.load_pem_private_key(
            private_key_bytes,
            password=None
        )
    return private_key

def load_public_key(client_id, file_name):
    client_id = str(client_id)
    file_name = str(file_name)
    # Load the public key from the file based on the client ID
    with open("keys/" + client_id + '/' + file_name + "_public.pem", "rb") as f:
        public_key_bytes = f.read()
        public_key = serialization.load_pem_public_key(
            public_key_bytes
        )
    return public_key

def encrypt_message(message, public_key):
    # Encrypt the message with the public key
    encrypted = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def decrypt_message(encrypted, private_key):
    # Decrypt the message with the private key
    decrypted = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')

# Example usage
# client_id = "client1"
# message = "Hello, world!"

# Load the keys
# private_key = load_private_key(client_id)
# public_key = load_public_key(client_id)

# Encrypt the message with the public key
# encrypted = encrypt_message(message, public_key)
# print("Encrypted message:", encrypted)

# Decrypt the message with the private key
# decrypted = decrypt_message(encrypted, private_key)
# print("Decrypted message:", decrypted)

# clientlist = ['A', 'B', 'C', 'D']
# clientlist = [1, 2, 3, 4, 5]
# key =  generate_dictionary_key(clientlist, 111, 1)
# print(key)