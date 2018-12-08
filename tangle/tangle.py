from hashlib import sha256
import json
import time
import random

from flask import Flask, request
import requests
import networkx as nx
import pickle
from tqdm import tqdm
import matplotlib.pyplot as plt

#has to be 5, 50, 500, 50000, 500000
sample_size = int(sys.argv[1])

class Node:

    def __init__(self, index, first_prior, second_prior, sender, receiver, amount, timestamp):
        self.index = index
        self.first_prior = first_prior
        self.second_prior = second_prior
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp
        self.nonce = 0

    def compute_hash(self):

        graph = json.dumps(self.__dict__, sort_keys=True)

        return sha256(graph.encode()).hexdigest()

class Network:

    # proof_of_work_difficulty of our PoW algorithm
    proof_of_work_difficulty = 1

    def __init__(self):

        self.graph = nx.DiGraph()
        self.tips = []
        self.leaves = []

        self.genesis()

    def genesis(self):
        #adding genesis node
        self.graph.add_node(0)  

        for i in range(4):
            node = Node(i, 0, 0, "a", "b", 1, time.time())
            node.hash = i
            self.leaves.append(i)
            self.graph.add_edge(i, 0)

        self.leaves = [x for x in self.graph.nodes() if self.graph.in_degree(x)==0]

    def add_new_node(self, node, proof): 
        node.hash = proof

        #print(node.index, self.graph[node.index])

        self.graph.add_edge(node.index, node.first_prior)
        self.graph.add_edge(node.index, node.second_prior)

        #print(node.index, self.graph[node.index])

    def proof_of_work(self, node):

        node.nonce = 0

        computed_hash = node.compute_hash()

        while not computed_hash.startswith('0' * Network.proof_of_work_difficulty):
            node.nonce += 1
            computed_hash = node.compute_hash()

        return computed_hash

    def mine(self, tx):

        first_prior, second_prior = random.sample(self.leaves, 2)

        new_node = Node(index=tx["index"], first_prior=first_prior, second_prior=second_prior, sender=tx["sender"], receiver=tx["receiver"], amount=tx["amount"], timestamp=tx["timestamp"])

        proof = self.proof_of_work(new_node)

        self.add_new_node(new_node, proof)

#the network to manage the ledgering and mining process

app = Flask(__name__)

tangle = Network()

peers = set()

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()

    tx_data["timestamp"] = time.time()
    tx_data["index"] = len(tangle.graph.nodes) + 1

    tangle.tips.append(tx_data)
    tangle.graph.add_node(tx_data["index"])

    return "Success", 201

@app.route('/mining', methods=['GET'])
def mining():

    for tip in tangle.tips:
        tangle.mine(tip)

    tangle.tips = []

    tangle.leaves = [x for x in tangle.graph.nodes() if tangle.graph.in_degree(x)==0]

    # for x in tangle.graph.nodes():
    #     print(x, "out degree", tangle.graph.out_degree(x), "in degree", tangle.graph.in_degree(x))

    return "Success", 201

@app.route('/tangle', methods=['GET'])
def eval_the_tangle():

    return str(len(tangle.graph.nodes) - 5)

@app.route('/main', methods=['GET'])
def main():
    with open('transactions.pkl','rb') as f:
        transactions = pickle.load(f)
        print("transactions loaded")
        i = 0
        for tx in tqdm(transactions[0:sample_size]):

            tx["timestamp"] = time.time()
            tx["index"] = len(tangle.graph.nodes) + 1

            tangle.tips.append(tx)
            tangle.graph.add_node(tx["index"])

            if ((i % 5) == 0):
                requests.get("http://localhost:8000/mining")
            i += 1

    #drawing it for fun
    nx.draw(tangle.graph, pos=nx.spring_layout(tangle.graph), node_color='blue', node_size=5)
    plt.savefig("test@" + str(sample_size) + ".png")

    return("hello")

app.run(debug=True, port=8000)




