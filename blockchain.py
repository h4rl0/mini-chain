import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

DIFFICULTY = 4


class Blockchain:
    def __init__(self):
        self.chain = [self.make_genesis()]
        self.pending_transactions = []
        self.nodes = set()

    @staticmethod
    def make_genesis():
        return {
            "index": 1,
            "timestamp": 0,
            "transactions": [],
            "previous_hash": "0",
            "nonce": 0,
        }

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash_block(block):
        encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    @staticmethod
    def meets_difficulty(block):
        return Blockchain.hash_block(block).startswith("0" * DIFFICULTY)

    def add_transaction(self, sender, recipient, amount):
        self.pending_transactions.append(
            {"sender": sender, "recipient": recipient, "amount": amount}
        )
        return self.last_block["index"] + 1

    def mine_block(self):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": list(self.pending_transactions),
            "previous_hash": self.hash_block(self.last_block),
            "nonce": 0,
        }
        while not self.meets_difficulty(block):
            block["nonce"] += 1

        self.pending_transactions = []
        self.chain.append(block)
        return block

    def register_node(self, address):
        netloc = urlparse(address).netloc
        if netloc:
            self.nodes.add(netloc)

    def is_valid_chain(self, chain):
        if not chain or chain[0] != self.make_genesis():
            return False

        for previous, current in zip(chain, chain[1:]):
            if current["previous_hash"] != self.hash_block(previous):
                return False
            if not self.meets_difficulty(current):
                return False
        return True

    def resolve_conflicts(self):
        best_chain = None
        best_length = len(self.chain)

        for node in self.nodes:
            try:
                response = requests.get(f"http://{node}/chain", timeout=5)
            except requests.RequestException:
                continue

            if response.status_code != 200:
                continue

            data = response.json()
            if data["length"] > best_length and self.is_valid_chain(data["chain"]):
                best_length = data["length"]
                best_chain = data["chain"]

        if best_chain:
            self.chain = best_chain
            return True
        return False


app = Flask(__name__)
CORS(app)
node_id = uuid4().hex
blockchain = Blockchain()


@app.get("/chain")
def full_chain():
    return jsonify({"chain": blockchain.chain, "length": len(blockchain.chain)}), 200


@app.post("/transactions/new")
def new_transactions():
    data = request.get_json(silent=True) or {}
    required = ("sender", "recipient", "amount")
    if not all(key in data for key in required):
        return jsonify({"error": "Need sender, recipient and amount"}), 400

    index = blockchain.add_transaction(
        data["sender"], data["recipient"], data["amount"]
    )
    return jsonify({"message": f"Transaction will be added to block {index}"}), 201


@app.get("/mine")
def mine():
    blockchain.add_transaction(sender="NETWORK", recipient=node_id, amount=1)
    block = blockchain.mine_block()
    return jsonify({"message": "New block mined", **block}), 200


@app.post("/nodes/register")
def register_nodes():
    data = request.get_json(silent=True) or {}
    nodes = data.get("nodes")
    if not nodes:
        return jsonify({"error": "Send a list of node URLs"}), 400

    for address in nodes:
        blockchain.register_node(address)

    return jsonify(
        {"message": "Nodes added", "all_nodes": sorted(blockchain.nodes)}
    ), 201


@app.get("/nodes/resolve")
def resolve():
    replaced = blockchain.resolve_conflicts()
    message = "Our chain was replaced" if replaced else "Our chain is authoritative"
    return jsonify({"message": message, "chain": blockchain.chain}), 200


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000, type=int)
    args = parser.parse_args()
    app.run(host="127.0.0.1", port=args.port)
