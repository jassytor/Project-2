import threading
import time
import random


class Teller(threading.Thread):
	def __init__(self, teller_id, bank):
		super().__init__()
		self.teller_id = teller_id
		self.bank = bank
		self.daemon = True

	def run(self):
		print(f"Teller {self.teller_id} []: ready to serve")
		
		while True:
			self.bank.customer_arrives.acquire()
			
			try:
				customer = self.bank.customer_queue.get_nowait()
			except Exception:
				continue

			print(f"Teller {self.teller_id} []: waiting for a customer")

			customer.assigned_teller = self.teller_id
			print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: serving a customer")
			customer.teller_ready.set()

			print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: asks for transaction")
			customer.ask_transaction.set()

			customer.transaction_ready.wait()
			txn_type = customer.transaction_type
			print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: handling {txn_type.lower()} transaction")

			if txn_type and txn_type.lower() == 'withdrawal':
				print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: going to the manager")
				self.bank.manager.acquire()
				try:
					print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: getting manager's permission")
					time.sleep(random.uniform(0.005, 0.03))  # 5-30 ms manager interaction
					print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: got manager's permission")
				finally:
					self.bank.manager.release()

			print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: going to safe")
			self.bank.safe.acquire()
			try:
				print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: enter safe")
				time.sleep(random.uniform(0.01, 0.05))
				print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: leaving safe")
			finally:
				self.bank.safe.release()

			print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: finishes {txn_type.lower()} transaction.")
			print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: wait for customer to leave.")
			customer.transaction_done.set()

			self.bank.customer_queue.task_done()
		
		print(f"Teller {self.teller_id} []: leaving for the day")
