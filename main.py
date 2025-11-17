import threading
import time
from bank import Bank
from teller import Teller
from customer import Customer


def main():
	bank = Bank()

	tellers = [Teller(i, bank) for i in range(3)]
	for t in tellers:
		t.start()

	num_customers = 50
	customers = [Customer(bank) for i in range(num_customers)]

	for c in customers:
		c.start()

	for c in customers:
		c.join()

	bank.customer_queue.join()

	print('The bank closes for the day.')

if __name__ == '__main__':
	main()
