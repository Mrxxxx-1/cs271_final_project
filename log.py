'''
Author: Mrx
Date: 2023-03-16 09:30:38
LastEditors: Mrx
LastEditTime: 2023-03-16 10:24:41
FilePath: \cs271_final_project\log.py
Description: 

Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''
import json

def logwrite(data, id):
    filename = 'log' + id + '.json'
    with open(filename, 'w') as f:
        json.dump(data, f)
    print('write log to %s' %(filename))
def logread(id):
    filename = 'log' + id + '.json'
    with open(filename, 'r') as f:
        data = json.load(f)
    print('read log from %s' %(filename))
    return data
# test case
# data = {'A':'test'}
# id = 'A'
# logwrite(data, id)
# print(logread(id))