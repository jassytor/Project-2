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
		self.assigned_teller = None
		
		self.teller_ready = threading.Event()
		self.ask_transaction = threading.Event()
		self.transaction_ready = threading.Event()
		self.transaction_done = threading.Event()
		self.transaction_type = None

	def run(self):
		self.transaction = random.choice(['Deposit', 'Withdrawal'])
		print(f"Customer {self.customer_id} []: wants to perform a {self.transaction.lower()} transaction")

		wait_time = random.uniform(0, 0.1)  # 0-100 ms
		time.sleep(wait_time)

		print(f"Customer {self.customer_id} []: going to bank.")
		self.bank.door.acquire()
		print(f"Customer {self.customer_id} []: entering bank.")

		try:
			print(f"Customer {self.customer_id} []: getting in line.")
			self.bank.customer_queue.put(self)
			self.bank.customer_arrives.release()
			
			print(f"Customer {self.customer_id} []: selecting a teller.")

			self.teller_ready.wait()
			teller_id = self.assigned_teller
			print(f"Customer {self.customer_id} [Teller {teller_id}]: selects teller")
			print(f"Customer {self.customer_id} [Teller {teller_id}] introduces itself")

			self.ask_transaction.wait()
			print(f"Customer {self.customer_id} [Teller {teller_id}]: asks for {self.transaction.lower()} transaction")

			self.transaction_type = self.transaction
			self.transaction_ready.set()

			self.transaction_done.wait()

			print(f"Customer {self.customer_id} [Teller {teller_id}]: leaves teller")

		finally:
			print(f"Customer {self.customer_id} []: goes to door")
			self.bank.door.release()
			print(f"Customer {self.customer_id} []: leaves the bank")
