import requests
import time
import pickle
from pprint import pprint

state = True
tx_rate = []
while state:
	r1 = requests.get("http://localhost:8000/mine")
	print(r1.text)
	r2 = requests.get("http://localhost:8000/chain")
	response = r2.json()

	chain_length = 0
	for block in response["chain"]:
		chain_length += len(block["transactions"])
	print(chain_length)	

	#pprint(response["chain"])

	time.sleep(60 * 1)
	tx_rate.append(chain_length)
	if (chain_length >= 500000):
		state = False

with open("results/tx_history.pkl", "wb") as f:
	pickle.dump(tx_rate, f)
