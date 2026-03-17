# Distributed Dictionary

This project implements a small **distributed key–value dictionary** service using a simplified version of the **Raft** consensus protocol and **RSA-based encryption**.  
Multiple processes act as Raft nodes; each user/client runs a node plus a simple text UI to create and operate on encrypted shared dictionaries.

### Main components

- **`main.py`** – Client entrypoint and text UI.
  - Prompts for a numeric user ID (`1`–`5`).
  - Starts a local `RaftNode` in a background thread.
  - Provides commands to:
    - Create a shared dictionary with a set of members.
    - Put and get key–value pairs in a dictionary.
    - Print one or all local dictionaries.
    - Simulate link failures and process failures.
- **`raft.py`** – UDP-based Raft node.
  - Handles leader election, heartbeats, and log replication among 5 fixed processes.
  - Receives client requests from leaders and replicates them to followers.
- **`dictionary.py`** – Encrypted dictionary abstraction.
  - Wraps per-dictionary metadata (ID, members, encryption keys).
  - Reads/writes encrypted dictionary contents on disk.
- **`encryption.py`** – RSA key management and encryption helpers.
  - Generates dictionary keypairs.
  - Encrypts/decrypts data and per-member dictionary keys.
- **`keys_for_clients.py`** – One-time key generator.
  - Generates RSA keypairs for each client/user ID and stores them under `keys/<client_id>/`.

### Requirements

- **Python**: 3.10+ recommended.
- **Dependencies**:
  - `cryptography`

Install the dependency with:

```bash
pip install cryptography
```

### Initial setup

1. **Clone or download** this repository.
2. (Optional but recommended) **Create a virtual environment** and activate it.
3. **Install dependencies**:
   ```bash
   pip install cryptography
   ```
4. **Generate per-client keys** (run once):
   ```bash
   python keys_for_clients.py
   ```
   This will create a `keys/` directory with subdirectories `1`, `2`, `3`, `4`, `5` containing each client’s RSA keypair.

### Running the system

This project is designed to run **five processes**, each representing one participant in the Raft cluster.

1. Open **five terminals** on the same machine.
2. In each terminal, change into the project directory and run:
   ```bash
   python main.py
   ```
3. When prompted, enter a **unique user ID** from `1` to `5` in each terminal.
4. Once all five clients are running, one of them will eventually become the **leader**.

> Note: Host/IP and port mappings for Raft nodes and client UIs are currently fixed in `raft.py` and `main.py` (see `usertable` and `usertable2`).  
> By default the system uses `127.0.0.1` (localhost). To run across machines, set the environment variable `DD_HOST` to the host/IP you want peers to send to, and optionally `DD_BIND_HOST` for what address to bind locally (e.g. `0.0.0.0`).

### Example interaction (from a client terminal)

After `main.py` starts and the text menu appears, you can:

1. **Create a new shared dictionary**:
   - Choose the menu option to create a dictionary.
   - Provide a list of member IDs (e.g., `1 2 3`) so the dictionary is shared among those clients.
2. **Put a key–value pair**:
   - Use the `put` command with the dictionary ID, key, and value.
   - The leader logs this operation and replicates it to followers via Raft.
   - The value is stored **encrypted** on disk under `keys/<client_id>/<dic_id>.txt`.
3. **Get a value**:
   - Use the `get` command with the dictionary ID and key.
   - The client reads and decrypts the local dictionary file to show the value.
4. **Simulate failures**:
   - Use the `failLink` and `fixLink` options to break/repair links between processes.
   - Use `failProcess` to simulate a crashed process and observe Raft re-election.

Exact prompts and command formats are displayed in the `main.py` menu when you run the program.

### Design overview

- **Raft**:
  - Each client process runs its own `RaftNode` (`raft.py`).
  - Nodes communicate via UDP messages for:
    - `request_vote` / `request_vote_response`
    - `append_entries` (log replication)
    - `leader_heartbeat`
    - `commit` notifications.
  - Log entries represent dictionary operations (`create`, `put`, `get`).
- **Encryption**:
  - Each dictionary gets its own RSA keypair.
  - The dictionary’s private key (represented by its ID) is encrypted separately for each member using that member’s public key.
  - Dictionary contents (the key–value map) are encrypted with the dictionary public key before being written to disk.

This documentation focuses on how to run and understand the project; the code itself contains more details about message formats and internal state.*** End Patch``` }' to=functions.ApplyPatch פואassistant/Subthreshold to=functions.ApplyPatch ***!