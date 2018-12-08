import random
import pickle

#100k nodes
ledger = {i: 100 for i in range(100000) }

#500k transactions
transactions = []
for i in range(500000):
	transaction = {"sender": "", "receiver": "", "amount": ""}

	receiver, sender = random.sample(xrange(100000), 2)
	amount = ledger[sender] * (random.randint(1, 10) / float(100))

	transaction["receiver"] = receiver
	transaction["sender"] = sender
	transaction["amount"] = amount

	ledger[sender] = ledger[sender] - amount
	ledger[receiver] = ledger[receiver] + amount

	print(receiver, sender, amount)

	transactions.append(transaction)

with open('blockchain/transactions.pkl','w') as f:
    pickle.dump(transactions, f)

with open('tangle/transactions.pkl','w') as f:
    pickle.dump(transactions, f)