'''
Author: Mrx
Date: 2023-03-18 17:27:35
LastEditors: Mrx
LastEditTime: 2023-03-18 23:57:02
FilePath: \cs271_final_project\keys_for_clients.py
Description: 

Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
import os

def generate_key_pair(client_id):
    # Define the directory where the keys will be stored
    client_id =str(client_id)
    KEY_DIR = "keys/" + client_id +'/'
    # Check if the directory for the keys exists, if not, create it
    if not os.path.exists(KEY_DIR):
        os.makedirs(KEY_DIR)

    # Generate the RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    # Serialize the keys to store them in a file
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Store the keys in files based on the client ID
    with open(KEY_DIR + client_id + "_private.pem", "wb") as f:
        f.write(private_key_bytes)
    with open(KEY_DIR + client_id + "_public.pem", "wb") as f:
        f.write(public_key_bytes)

    # Return the public key for the client
    return public_key
# client_id = ['A', 'B', 'C', 'D', 'E']
client_id = [1, 2, 3, 4, 5]
for item in client_id :
    public_key = generate_key_pair(item)
    print(item)