'''
Author: Mrx
Date: 2023-02-28 10:41:21
LastEditors: Mrx
LastEditTime: 2023-03-17 08:28:35
FilePath: \cs271_final_project\raft_example.py
Description: 

Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''
# import asyncio
import random
import time

class RaftNode:
    def __init__(self, id, peers):
        self.id = id
        self.peers = peers
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.last_applied = 0
        self.state = 'follower'
        self.election_timeout = self.get_random_timeout()

    # def start(self):
    #     loop = asyncio.get_event_loop()
    #     loop.create_task(self.run())

    def start(self):
        while True:
            if self.state == 'follower':
                self.follower()
            elif self.state == 'candidate':
                self.candidate()
            elif self.state == 'leader':
                self.leader()

    def follower(self):
        time.sleep(self.election_timeout)
        self.state = 'candidate'
        print('Start leader election')
        print('Change state to candidate')

    def candidate(self):
        self.current_term += 1
        self.voted_for = self.id
        votes = 1

        for peer in self.peers:
            if peer != self.id:
                response = peer.request_vote(self.current_term, self.id, len(self.log), self.log[-1]['term'])
                if response['term'] > self.current_term:
                    self.current_term = response['term']
                    self.state = 'follower'
                    return
                if response['vote_granted']:
                    votes += 1

        if votes > len(self.peers) / 2:
            self.state = 'leader'
            self.next_index = {peer: len(self.log) + 1 for peer in self.peers}
            self.match_index = {peer: 0 for peer in self.peers}

    def leader(self):
        while True:
            for peer in self.peers:
                if peer != self.id:
                    prev_log_index = self.next_index[peer] - 1
                    prev_log_term = self.log[prev_log_index]['term'] if prev_log_index >= 0 else None
                    entries = self.log[self.next_index[peer]:]
                    response =peer.append_entries(self.current_term, self.id, prev_log_index, prev_log_term, entries, self.commit_index)
                    if response['term'] > self.current_term:
                        self.current_term = response['term']
                        self.state = 'follower'
                        return
                    if response['success']:
                        self.next_index[peer] += len(entries)
                        self.match_index[peer] = self.next_index[peer] - 1
                        if self.check_quorum(self.match_index[peer]):
                            self.commit_index = self.match_index[peer]

            time.sleep(3)

    def request_vote(self, term, candidate_id, last_log_index, last_log_term):
        if term < self.current_term:
            return {'term': self.current_term, 'vote_granted': False}

        if self.voted_for is None or self.voted_for == candidate_id:
            if last_log_index >= len(self.log) - 1 and self.log[last_log_index]['term'] == last_log_term:
                self.voted_for = candidate_id
                return {'term': self.current_term, 'vote_granted': True}

        return {'term': self.current_term, 'vote_granted': False}

    async def append_entries(self, term, leader_id, prev_log_index, prev_log_term, entries, leader_commit):
        if term < self.current_term:
            return {'term': self.current_term, 'success': False}

        if prev_log_index >= len(self.log) or (prev_log_term != self.log[prev_log_index]['term']):
            return {'term': self.current_term, 'success': False}
        for i, entry in enumerate(entries):
            index = prev_log_index + i + 1
            if index < len(self.log) and self.log[index]['term'] != entry['term']:
                self.log = self.log[:index]
            if index >= len(self.log):
                self.log.append(entry)

        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.log) - 1)

        return {'term': self.current_term, 'success': True}

    def get_random_timeout(self):
        return random.uniform(5, 10)

    def check_quorum(self, index):
        return sum(1 for i in self.match_index.values() if i >= index) > len(self.peers) / 2

if __name__ == '__main__' :
    list1 = [1, 2, 3]
    client1 = RaftNode(1, list1)
    client2 = RaftNode(2, list1)
    client3 = RaftNode(3, list1)
    client1.start()
    client2.start()
    client3.start()



# This implementation defines a `RaftNode` class that represents a single node in the Raft cluster. Each node has an ID, a list of peers, a current term, a voted-for candidate, a log of entries, a commit index, a last applied index, and a state (either 'follower', 'candidate', or 'leader'). 
# It also has a method for starting the node, which runs an infinite loop that executes the appropriate state-specific function (`follower()`, `candidate()`, or `leader()`) based on the current state.

# The `follower()` function simply waits for an election timeout to expire before transitioning to the `candidate` state. The `candidate()` function increments the current term, requests votes from all other nodes, and becomes the leader if it receives votes from a majority of nodes. 
# The `leader()` function sends heartbeat messages to all other nodes at regular intervals, updates its own log, and sends log entries to other nodes.

# The `request_vote()` and `append_entries()` functions are RPCs (Remote Procedure Calls) that are used by nodes to communicate with each other. `request_vote()` is used by candidates to request votes from other nodes, while `append_entries()` is used by leaders to send log entries to other nodes. 

# Overall, this is a simplified implementation of the Raft consensus algorithm, but it should give you a basic idea of how the algorithm works and how it can be implemented in Python using the `asyncio` library.
