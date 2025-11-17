import threading
import time
import random


class Customer(threading.Thread):
	_id_counter = 0
	_id_lock = threading.Lock()

	def __init__(self, bank):
		super().__init__()
		with Customer._id_lock:
			Customer._id_counter += 1
			self.customer_id = Customer._id_counter
		self.bank = bank
		self.transaction = None
		self.daemon = True
		
		self.teller_ready = threading.Event()
		self.ask_transaction = threading.Event()
		self.transaction_ready = threading.Event()
		self.transaction_done = threading.Event()
		self.transaction_type = None

	def run(self):
		self.transaction = random.choice(['Deposit', 'Withdrawal'])
		print(f"Customer {self.customer_id}: decides to perform {self.transaction}")

		print(f"Customer {self.customer_id}: waits before entering bank")
		wait_time = random.uniform(0, 0.1)  # 0-100 ms
		time.sleep(wait_time)
		print(f"Customer {self.customer_id}: finished waiting")

		print(f"Customer {self.customer_id}: goes to bank door")
		self.bank.door.acquire()
		print(f"Customer {self.customer_id}: enters bank")

		try:
			print(f"Customer {self.customer_id}: gets in line")
			self.bank.customer_queue.put(self)
			self.bank.customer_arrives.release()

			self.teller_ready.wait()
			print(f"Customer {self.customer_id}: selects teller")

			self.ask_transaction.wait()
			print(f"Customer {self.customer_id}: teller asks for transaction")

			self.transaction_type = self.transaction
			self.transaction_ready.set()
			print(f"Customer {self.customer_id}: tells teller {self.transaction}")

			self.transaction_done.wait()
			print(f"Customer {self.customer_id}: receives transaction completion")

		finally:
			self.bank.door.release()
			print(f"Customer {self.customer_id}: leaves bank")
