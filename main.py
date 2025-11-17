import threading
import time
from bank import Bank
from teller import Teller
from customer import Customer


def main():
	bank = Bank()

	# start 3 tellers with unique ids (0, 1, 2)
	tellers = [Teller(i, bank) for i in range(3)]
	for t in tellers:
		t.start()

	# create 50 customers with auto-generated unique ids
	num_customers = 50
	customers = [Customer(bank) for i in range(num_customers)]

	# start customers
	for c in customers:
		c.start()

	# wait for all customers to finish
	for c in customers:
		c.join()

	# wait until queue tasks are marked done
	bank.customer_queue.join()

	print('The bank closes for the day.')

if __name__ == '__main__':
	main()
