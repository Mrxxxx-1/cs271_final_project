'''
Author: Mrx
Date: 2023-03-18 17:05:30
LastEditors: Mrx
LastEditTime: 2023-03-19 11:02:44
FilePath: \cs271_final_project\dictionary.py
Description: 

Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''
import random
import string
import os
from encryption import *

class Dictionary:
    def __init__(self, members, counter, client_id):
        self.id = self.generate_unique_id(counter)
        self.client_id = client_id
        self.public_key, self.private_key, self.member_keys = self.generate_key_pair(self.id, self.client_id)
        # self.member_keys = self.generate_member_keys(members)
        self.members = members
        self.log_entry = self.create_log_entry()
        
    
    def generate_unique_id(self,counter):
        pid = (os.getpid())
        return pid + counter
    
    def generate_key_pair(self, id, client_id):
        return generate_dictionary_key(members, id, client_id)
        
    # def generate_member_keys(self, members):
    #     member_keys = members
    #     return member_keys
    
    # def encrypt_key(self, private_key, public_key):
    #     # Use some encryption method to encrypt the private key with the public key
    #     encrypted_key = private_key + public_key # For demonstration purposes only, not secure
    #     return encrypted_key
    
    def create_log_entry(self):
        log_entry = {
            'id': self.id,
            'members': self.members,
            'public_key': self.public_key,
            'member_keys': self.member_keys
        }
        return log_entry
    
    def commit_log_entry(self):
        # Use some Raft implementation to commit the log entry and create the dictionary
        # For demonstration purposes only, just print the log entry
        print("Dictionary created:", self.log_entry)

# Example usage
members = [1, 2, 3]
dictionary = Dictionary(members, 111, 1)
dictionary.commit_log_entry()