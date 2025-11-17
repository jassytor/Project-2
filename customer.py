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
		
		# Events for synchronization with assigned teller
		self.teller_ready = threading.Event()
		self.ask_transaction = threading.Event()
		self.transaction_ready = threading.Event()
		self.transaction_done = threading.Event()
		self.transaction_type = None

	def run(self):
		# 1. Decide transaction at random: Deposit or Withdrawal
		self.transaction = random.choice(['Deposit', 'Withdrawal'])
		print(f"Customer {self.customer_id} []: wants to perform a {self.transaction.lower()} transaction")

		# 2. Wait between 0-100ms before entering bank
		wait_time = random.uniform(0, 0.1)  # 0-100 ms
		time.sleep(wait_time)

		# 3. Enter the bank (door semaphore allows max 2 customers at a time)
		print(f"Customer {self.customer_id} []: going to bank.")
		self.bank.door.acquire()
		print(f"Customer {self.customer_id} []: entering bank.")

		try:
			# 4. Get in line (add self to queue and signal teller)
			print(f"Customer {self.customer_id} []: getting in line.")
			self.bank.customer_queue.put(self)
			self.bank.customer_arrives.release()
			
			print(f"Customer {self.customer_id} []: selecting a teller.")

			# 5. Wait for teller to signal ready
			self.teller_ready.wait()
			teller_id = self.assigned_teller
			print(f"Customer {self.customer_id} [Teller {teller_id}]: selects teller")
			print(f"Customer {self.customer_id} [Teller {teller_id}] introduces itself")

			# 6. Wait for teller to ask for transaction
			self.ask_transaction.wait()
			print(f"Customer {self.customer_id} [Teller {teller_id}]: asks for {self.transaction.lower()} transaction")

			# 7. Tell the teller the transaction
			self.transaction_type = self.transaction
			self.transaction_ready.set()

			# 8. Wait for teller to complete the transaction
			self.transaction_done.wait()

			print(f"Customer {self.customer_id} [Teller {teller_id}]: leaves teller")

		finally:
			# 9. Leave the bank through the door (release door semaphore)
			print(f"Customer {self.customer_id} []: goes to door")
			self.bank.door.release()
			print(f"Customer {self.customer_id} []: leaves the bank")
