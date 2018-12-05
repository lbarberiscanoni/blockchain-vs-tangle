import pickle
import json
import time
import sys

ledger = str(sys.argv[1])

print(ledger)

with open('data/transactions.pkl','rb') as f:
	transactions = pickle.load(f)
	print("transactions loaded")

	i = 0
	for tx in transactions:
		if (ledger == "blockchain"): 
			if ((i % 500) == 0):
				
			requests.post("http://localhost:8000/new_transaction", json=tx)
		elif (ledger == "tangle"):
			requests.post("http://localhost:8000/new_transaction", json=tx)
		


		i += 0

