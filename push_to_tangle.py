import requests
from pprint import pprint

for i in range(4):
	r = requests.post("http://localhost:8000/new_transaction", json={"sender": 1, "receiver": 2, "amount": 3})

r2 = requests.get("http://localhost:8000/mining")
print(r2)

r3 = requests.get("http://localhost:8000/tangle")
print(r3)