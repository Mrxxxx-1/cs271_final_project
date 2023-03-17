import hashlib
# import raft

class ReplicatedLog:

    def __init__(self, client_id):
        self.log = []
        self.term = 0
        self.index = -1
        self.client_id = client_id
        self.members = []
        self.public_key = None
        self.private_keys = {}

    def add_member(self, client_id):
        self.members.append(client_id)

    def set_public_key(self, public_key):
        self.public_key = public_key

    def encrypt_private_key(self, client_id):
        private_key = self.private_keys[client_id]
        # encrypt private key with the member's public key
        # and return the encrypted version

    def add_private_key(self, client_id, private_key):
        self.private_keys[client_id] = private_key

    def create_dictionary(self, dictionary_id):
        entry = {
            "type": "create",
            "term": self.term,
            "index": self.index + 1,
            "dictionary_id": dictionary_id,
            "member_ids": self.members,
            "public_key": self.public_key,
            "private_keys": {client_id: self.encrypt_private_key(client_id) for client_id in self.members}
        }
        self.append_entry(entry)

    def put(self, dictionary_id, key, value):
        entry = {
            "type": "put",
            "term": self.term,
            "index": self.index + 1,
            "dictionary_id": dictionary_id,
            "client_id": self.client_id,
            "key": key,
            "value": value
        }
        self.append_entry(entry)

    def get(self, dictionary_id, key):
        entry = {
            "type": "get",
            "term": self.term,
            "index": self.index + 1,
            "dictionary_id": dictionary_id,
            "client_id": self.client_id,
            "key": key
        }
        self.append_entry(entry)

    def append_entry(self, entry):
        if len(self.log) == 0:
            entry["previous_hash"] = None
        else:
            previous_entry = self.log[-1]
            previous_hash = hashlib.sha256(str(previous_entry).encode()).hexdigest()
            entry["previous_hash"] = previous_hash
        hash = hashlib.sha256(str(entry).encode()).hexdigest()
        entry["hash"] = hash
        self.log.append(entry)
        self.index += 1

    def verify_entry(self, entry):
        if len(self.log) == 0:
            return True
        else:
            previous_entry = self.log[-1]
            previous_hash = hashlib.sha256(str(previous_entry).encode()).hexdigest()
            return previous_hash == entry["previous_hash"]

    def replicate_log(self, other_clients):
        for entry in self.log:
            for client in other_clients:
                if client.verify_entry(entry):
                    client.log.append(entry)
                    client.index += 1

    def get_value(self, dictionary_id, key):
        for entry in reversed(self.log):
            if entry["dictionary_id"] == dictionary_id and entry["type"] == "put" and entry["key"] == key:
                return entry["value"]
        return None

    def apply_entry(self, entry):
        if entry["type"] == "create":
            self.add_member(self.client_id)
            self.set_public_key(entry["public_key"])
            self.add_private_key(self.client_id, entry["private_keys"][self.client_id])
        elif entry["type"] == "put":
            if entry["dictionary_id"] == "my_dict":
                value = self.decrypt_value(entry["value"])
                self.my_dict[entry["key"]]
