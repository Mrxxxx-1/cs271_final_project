'''
Author: Mrx
Date: 2023-03-17 08:36:25
LastEditors: Mrx
LastEditTime: 2023-03-20 12:33:03
FilePath: \cs271_final_project\raft.py
Description: 

Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''
import socket
import threading
import json
import time
import random
import logging

# print("client")
usertable = {1 : 10882, 2 : 10884, 3 : 10886, 4 : 10888, 5 : 10900} 
user = { ('192.168.0.167', 10882) : 1, ('192.168.0.167', 10884) : 2, ('192.168.0.167', 10886) : 3, ('192.168.0.167', 10888) : 4, ('192.168.0.167', 10900) : 5}
faillink = {1 : 0, 2 : 0, 3 : 0, 4 : 0, 5 : 0}
userlist = [1, 2, 3, 4, 5]
usertable2 = {1 : 10782, 2 : 10784, 3 : 10786, 4 : 10788, 5 : 10700}
l_port = 10666
HOST = '192.168.0.167'

g_token = True
state = 'follower'
test = 0

class RaftNode:
    def __init__(self, id, peers):
        self.id = id
        self.peers = peers
        self.state = 'follower'
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = -1
        self.last_applied = -1
        self.next_index = {peer_id: len(self.log) for peer_id in self.peers}
        self.match_index = {peer_id: -1 for peer_id in self.peers}
        self.election_timeout = self.get_random_timeout()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((HOST, usertable[id]))
        self.socket.settimeout(0.1)

    def start(self):
        
        logging.info(f"Node {self.id}: Starting node")
        # print(f"Node {self.id}: Starting node")
        while g_token:
            if self.state == 'follower':
                self.follower()
            elif self.state == 'candidate':
                self.candidate()
            elif self.state == 'leader':
                self.leader()

    def follower(self):
        global state
        logging.info(f"Node {self.id}: Entering follower state")
        # print(f"Node {self.id}: Entering follower state")
        start_time = time.monotonic()
        while True:
            time.sleep(3)
            try:
                data, addr = self.socket.recvfrom(4096)
                message = json.loads(data.decode())
                if message['type'] == 'request_vote':
                    response = self.handle_request_vote(message['data'])
                    self.send_message(message['from'], 'request_vote_response', response)
                elif message['type'] == 'append_entries':
                    response = self.handle_append_entries(message['data'])
                    print('handling append entries from leader')
                    self.send_to_leader(message['from'], 'ack', response)
                elif message['type'] == 'leader_heartbeat':
                    self.handle_leader_heartbeat(message['data'])
                    start_time = time.monotonic()
                elif message['type'] == 'commit':
                    print('commit log entry')
                    pass
            except socket.timeout:
                if time.monotonic() - start_time > self.election_timeout:
                    logging.info(f"Node {self.id}: Timeout occurred")
                    self.state = 'candidate'
                    state = 'candidate'
                    break

    def candidate(self):
        global state
        logging.info(f"Node {self.id}: Entering candidate state")
        # print(f"Node {self.id}: Entering candidate state")
        self.current_term += 1
        self.voted_for = self.id
        votes_received = 1
        start_time = time.monotonic()
        for peer_id in self.peers:
            self.send_message(peer_id, 'request_vote', {
                'term': self.current_term,
                'candidate_id': self.id,
                'last_log_index': len(self.log) - 1,
                'last_log_term': self.log[-1]['term'] if self.log else -1,
            })
        while True:
            time.sleep(3)
            try:
                data, addr = self.socket.recvfrom(4096)
                message = json.loads(data.decode())
                if message['type'] == 'request_vote_response':
                    if message['data']['term'] > self.current_term:
                        self.current_term = message['data']['term']
                        self.state = 'follower'
                        state = 'follower'
                        break
                    elif message['data']['vote_granted']:
                        votes_received += 1
                        if votes_received > len(self.peers) / 2:
                            self.state = 'leader'
                            state = 'leader'
                            break
                elif message['type'] == 'append_entries':
                    response = self.handle_append_entries(message['data'])
                    self.send_to_leader(message['from'], 'ack', response)
                    if message['data']['term'] > self.current_term:
                        self.current_term = message['data']['term']
                        self.state = 'follower'
                        state = 'follower'
                        self.voted_for = message['data']['leader_id']
                        break
                elif message['type'] == 'leader_heartbeat':
                    self.handle_leader_heartbeat(message['data'])
                    start_time = time.monotonic()
                elif message['type'] == 'request_vote':
                    response = self.handle_request_vote(message['data'])
                    self.send_message(message['from'], 'request_vote_response', response)
                    if response['vote_granted'] ==True:
                        self.current_term = message['data']['term']
                        self.state = 'follower'
                        state = 'follower'
                        break
                    
            except socket.timeout:
                if time.monotonic() - start_time > self.election_timeout:
                    logging.info(f"Node {self.id}: Timeout occurred")
                    self.state = 'candidate'
                    state = 'candidate'
                    break
    
    def leader(self):
        logging.info(f"Node {self.id}: Entering leader state")
        # # print(f"Node {self.id}: Entering leader state")
        # self.next_index = {peer_id: len(self.log)+1 for peer_id in self.peers}
        # log_entry = {}
        # log_entry = {
        #     'term': self.current_term,
        #     'index': self.next_index,
        #     'type': 'leader_election',
        #     'data': self.id
        # }
        # self.log.append(log_entry)
        # self.commit_index += 1
        #     for peer_id in self.peers:
        #         # if self.next_index[peer_id] > 0:
        #         prev_log_index = self.next_index[peer_id] - 1
        #         prev_log_term = self.log[prev_log_index]['term'] if prev_log_index > 0 else -1
        #         entries = self.log[self.next_index[peer_id]:]
        #         # prev_log_index = None
        #         # prev_log_term = None
        #         # entries = 'entries'             
        #         self.send_message(peer_id, 'append_entries', {
        #             'term': self.current_term,
        #             'leader_id': self.id,
        #             'prev_log_index': prev_log_index,
        #             'prev_log_term': prev_log_term,
        #             'entries': entries,
        #             'leader_commit': self.commit_index,
        #         })
        t1 = threading.Thread(target=self.leader_heartbeat)
        t2 = threading.Thread(target=self.leader_append_entries)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def handle_request_vote(self, data):
        if data['term'] < self.current_term:
            return {'term': self.current_term, 'vote_granted': False}
        elif self.voted_for is None or self.voted_for == data['candidate_id']:
            last_log_index = len(self.log) - 1
            last_log_term = self.log[-1]['term'] if self.log else -1
            if data['last_log_index'] >= last_log_index and data['last_log_term'] >= last_log_term:
                self.voted_for = data['candidate_id']
                return {'term': self.current_term, 'vote_granted': True}
        return {'term': self.current_term, 'vote_granted': False}

    def handle_append_entries(self, data):
        if data['term'] < self.current_term:
            return {'term': self.current_term, 'success': False}
        elif len(self.log) < data['prev_log_index']:
        # elif len(self.log) <= data['prev_log_index'] or self.log[data['prev_log_index']]['term'] != data['prev_log_term']:
            return {'term': self.current_term, 'success': False}
        else:
            # already appended the log
            # self.log = self.log[:data['prev_log_index']+1] + data['entries']
            self.write_logfile(data['entries'])
            self.commit_index = min(data['leader_commit'], len(self.log)-1)
            return {'term': self.current_term, 'success': True}

    def handle_leader_heartbeat(self, data):
        self.current_term = data['term']

    def send_message(self, recipient_id, message_type, data):
        message = {
            'from': self.id,
            'type': message_type,
            'data': data,
        }
        # print(data)
        self.socket.sendto(json.dumps(message).encode(), (HOST, usertable[recipient_id]))
    
    def send_to_leader(self, recipient_id, message_type, data):
        message = {
            'from': self.id,
            'type': message_type,
            'data': data,
        }
        # print(data)
        self.socket.sendto(json.dumps(message).encode(), (HOST, l_port))
    
    def get_random_timeout(self):
        return random.uniform(6, 10)

    def sendreq(self,data, dest) :
        # if faillink[dest] == 0: 
        self.socket.sendto(data.encode('utf-8'), (HOST, usertable2[dest]))
        # else :
        #     print("Unable to connect to process %s" %(dest))

    def leader_heartbeat(self):
        while True:
            for peer_id in self.peers:          
                self.send_message(peer_id, 'leader_heartbeat', {
                    'term': self.current_term
                })
            time.sleep(3)
    
    def leader_append_entries(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((HOST, l_port))
        start_time = time.monotonic()
        majority = 1
        while True:
            try:
                data, addr = s.recvfrom(4096)
                message = json.loads(data.decode())
                print(message)
                if message['type'] == 'create' or message['type'] == 'put' or message['type'] == 'get':
                    majority = 1
                    print('send append entries RPC to all')
                    log_entry = {}
                    log_entry = {
                        'term': self.current_term,
                        'index': self.next_index,
                        'type': message['type'],
                        'data': message['data'],
                        'client': message['from']
                    }
                    self.write_logfile(log_entry)
                    for peer_id in self.peers:
                        # if self.next_index[peer_id] > 0:
                        prev_log_index = self.next_index[peer_id] - 1
                        prev_log_term = self.log[prev_log_index]['term'] if prev_log_index > 0 else -1
                        entries = self.log[self.next_index[peer_id]]
                        # prev_log_index = None
                        # prev_log_term = None
                        # entries = 'entries'             
                        self.send_message(peer_id, 'append_entries', {
                            'term': self.current_term,
                            'leader_id': self.id,
                            'prev_log_index': prev_log_index,
                            'prev_log_term': prev_log_term,
                            'entries': entries,
                            'leader_commit': self.commit_index,
                        })
                    pass
                if message['type'] == 'ack':
                    if message['data']['success']:
                        majority += 1
                        self.commit_index += 1
                        self.next_index[message['from']] += 1
                    if majority > len(self.peers) / 2:
                        for peer_id in self.peers:
                            data = json.dumps(entries)
                        for peer_id in self.peers:
                            # if self.next_index[peer_id] > 0:
                            prev_log_index = self.next_index[peer_id] - 1
                            prev_log_term = self.log[prev_log_index]['term'] if prev_log_index > 0 else -1
                            entries = []
                            # prev_log_index = None
                            # prev_log_term = None
                            # entries = 'entries'             
                            self.send_message(peer_id, 'commit', {
                                'term': self.current_term,
                                'leader_id': self.id,
                                'prev_log_index': prev_log_index,
                                'prev_log_term': prev_log_term,
                                'entries': entries,
                                'leader_commit': self.commit_index,
                            })
                        majority = -1
                    pass
            except socket.timeout:
                # if time.monotonic() - start_time > self.election_timeout:
                #     logging.info(f"Node {self.id}: Timeout occurred")
                #     self.state = 'candidate'
                #     state = 'candidate'
                #     break
                pass
    
    def write_logfile(self, message):
        self.log.append(message)
        self.commit_index += 1
        self.wlogfile(self.log)
        pass

    def wlogfile(self, log_entry):
        with open("log " + str(self.id) + '.txt', "w") as file:
            data = json.dumps(log_entry)
            file.write(data)
    def rlogfile(self):
        with open("log " + str(self.id) + '.txt', "r") as file:
            my_list = file.read()
            my_list = json.loads(my_list)
            return my_list

# if __name__ == '__main__' :
#     while True :
#         uid = input("Please input your userid : ")
#         uid = int(uid)
#         if usertable.get(uid) == None :
#             print("wrong userid!")
#             continue
#         break   
#     logging.basicConfig(level=logging.INFO)
#     list1 = userlist
#     list1.remove(uid)
#     node1 = RaftNode(uid, list1)
#     node2 = RaftNode(2, [1, 3])
#     node3 = RaftNode(3, [1, 2])
#     threading.Thread(target=node1.start).start()
#     threading.Thread(target=node2.start).start()
    # threading.Thread(target=node3.start).start()
    # node1 = RaftNode(1, userlist)
    # node1.test()
    # print(test)