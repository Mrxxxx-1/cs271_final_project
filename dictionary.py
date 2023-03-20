'''
Author: Mrx
Date: 2023-03-18 17:05:30
LastEditors: Mrx
LastEditTime: 2023-03-20 08:07:44
FilePath: \cs271_final_project\dictionary.py
Description: 

Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''
import random
import string
import os
from encryption import *
import json

class Dictionary:
    def __init__(self, members, counter, client_id):
        self.id = self.generate_unique_id(counter)
        self.client_id = client_id
        self.members = members
        self.public_key, self.private_key, self.member_keys = self.generate_key_pair(self. members, self.id, self.client_id)
        # self.member_keys = self.generate_member_keys(members)
        self.log_entry = self.create_log_entry()
        
    
    def generate_unique_id(self,counter):
        pid = (os.getpid())
        return pid + counter
    
    def generate_key_pair(self, members, id, client_id):
        return generate_dictionary_key(members, id, client_id)
        
    # def generate_member_keys(self, members):
    #     member_keys = members
    #     return member_keys
    
    # def encrypt_key(self, private_key, public_key):
    #     # Use some encryption method to encrypt the private key with the public key
    #     encrypted_key = private_key + public_key # For demonstration purposes only, not secure
    #     return encrypted_key
    
    def create_log_entry(self):
        data = {
            'dic_id': self.id,
            'members': self.members,
            'public_key': self.public_key.decode(),
            'member_keys': self.member_keys
        }
        log_entry = {
            'from': self.client_id,
            'type': 'create',
            'dic_id': self.id,
            'members': self.members,
            'data': data
        }
        return log_entry
    
    def commit_log_entry(self):
        # Use some Raft implementation to commit the log entry and create the dictionary
        # For demonstration purposes only, just print the log entry
        print("Dictionary created:", self.log_entry)


def dic_write(dic_file, id, client_id):
    KEY_DIR = "keys/" + client_id +'/'
    filename = KEY_DIR + str(id) + '.txt'
    public_key = load_public_key(client_id, str(id))
    dic_file = json.dumps(dic_file)
    encrypt_dic = encrypt_message(dic_file, public_key)
    with open(filename, 'wb') as f:
        f.write(encrypt_dic)
    print('write dic to %s' %(filename))
def dic_read(id, client_id):
    KEY_DIR = "keys/" + client_id +'/'
    filename = KEY_DIR + str(id) + '.txt'
    with open(filename, 'rb') as f:
        data = f.read()
    private_key = load_private_key(client_id, str(id))
    decrypt_data = decrypt_message(data, private_key)
    decrypt_data = json.loads(decrypt_data)
    print('read dic from %s' %(filename))
    return decrypt_data

# test case
# data = {'A':'test'}
# client_id = '1'
# dic_id = 11 
# dic_write(data, dic_id, client_id)
# print(dic_read(dic_id, client_id))
# data = {'B': 'test case'}
# dic_write(data, dic_id, client_id)
# print(dic_read(dic_id, client_id))

# Example usage
# members = [1, 2, 3]
# dictionary = Dictionary(members, 111, 1)
# dictionary.commit_log_entry()
