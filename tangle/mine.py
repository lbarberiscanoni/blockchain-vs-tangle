import requests
import time
import pickle
from pprint import pprint

state = True
tx_rate = []
while state:
	r1 = requests.get("http://localhost:8000/mining")
	print(r1.text)
	r2 = requests.get("http://localhost:8000/tangle")
	response = r2.text

	print(response)	

	#pprint(response["chain"])

	time.sleep(60 * 1)
	tx_rate.append(response)
	if (response >= 500000):
		state = False

with open("results/tx_history.pkl", "wb") as f:
	pickle.dump(tx_rate, f)
