from hashlib import sha256
import json
import time

from flask import Flask, request
import requests
import pickle
from tqdm import tqdm

import sys

#has to be 5, 50, 500, 50000, 500000
sample_size = int(sys.argv[1])

#size of the batch for mining, 500 for non-trivial amounts, 5 if we are testing super low tx #s to avoid errors
batch_size = int(sys.argv[2])

class Block:
    def __init__(self, index, transactions, timestamp, oldHash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = oldHash
        self.nonce = 0

    def compute_hash(self):

        block_string = json.dumps(self.__dict__, sort_keys=True)

        return sha256(block_string.encode()).hexdigest()



class Blockchain:
    # proof_of_work_difficulty of our PoW algorithm
    proof_of_work_difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.block_size = 250
        self.window = self.block_size * 4

        #making the genesis block
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()

        self.chain = [genesis_block]

    def add_block(self, block, proof):

        previous_hash = self.chain[-1].hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        if previous_hash == block.previous_hash:
            if Blockchain.is_valid_proof(block, proof):
                block.hash = proof
                self.chain.append(block)

                return True
            else:
                return False
        else:
            return False

    def proof_of_work(self, block):

        block.nonce = 0

        computed_hash = block.compute_hash()

        while not computed_hash.startswith('0' * Blockchain.proof_of_work_difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the proof_of_work_difficulty criteria.
        """

        validHash = block_hash == block.compute_hash()
        proof_of_work_criteria = block_hash.startswith('0' * Blockchain.proof_of_work_difficulty)

        return (validHash and proof_of_work_criteria)

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block.hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result


    def mine(self):

        if not self.unconfirmed_transactions:
            return False

        last_block = self.chain[-1]

        new_block = Block(index=last_block.index + 1, transactions=self.unconfirmed_transactions, timestamp=time.time(), oldHash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []

        for peer in peers:
            requests.post("http://{}/add_block".format(peer), data=json.dumps(new_block.__dict__, sort_keys=True))

        return new_block.index










#the network to manage the ledgering and mining process

app = Flask(__name__)

blockchain = Blockchain()

peers = set()




def consensus():

    #not proud of this lol
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)

    for node in peers:
        response = requests.get('http://{}/chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']

        #automatically go for the longest chain 
        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()

    required_fields = ["sender", "receiver", "amount"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid data", 404

    tx_data["timestamp"] = time.time()

    blockchain.add_new_transaction(tx_data)

    return "Success", 201


@app.route('/chain', methods=['GET'])
def get_chain():
    # make sure we've the longest chain
    consensus()
    chain_sequence = []
    for block in blockchain.chain:
        chain_sequence.append(block.__dict__)

    return json.dumps({"length": len(chain_sequence),
                       "chain": chain_sequence})

@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    return "Block #{} is mined.".format(result)

@app.route('/add_block', methods=['POST'])
def validate_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"], block_data["transactions"], block_data["timestamp", block_data["previous_hash"]])

    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201

@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)

@app.route("/main")
def main():
    with open('transactions.pkl','rb') as f:
        transactions = pickle.load(f)
        print("transactions loaded")

        i = 0
        for tx in tqdm(transactions[0: sample_size]):
            tx["timestamp"] = time.time()

            blockchain.add_new_transaction(tx)

            if ((i % batch_size) == 0):
                requests.get("http://localhost:8000/mine")
            i += 1

    return "all transactions loaded"



app.run(debug=True, port=8000)
