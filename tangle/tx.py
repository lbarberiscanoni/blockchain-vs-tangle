import requests
from pprint import pprint
import time
from tqdm import tqdm

for i in tqdm(range(500000)):
	r = requests.post("http://localhost:8000/new_transaction", json={"sender": 1, "receiver": 2, "amount": 3})
	time.sleep(.05)