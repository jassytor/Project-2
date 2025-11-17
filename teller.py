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
		print(f"Teller {self.teller_id}: is ready to serve")
		
		while True:
			self.bank.customer_arrives.acquire()
			
			try:
				customer = self.bank.customer_queue.get_nowait()
			except Exception:
				continue

			print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: is ready")
			customer.teller_ready.set()

			print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: asks for transaction")
			customer.ask_transaction.set()

			customer.transaction_ready.wait()
			txn_type = customer.transaction_type
			print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: receives {txn_type}")

			if txn_type and txn_type.lower() == 'withdrawal':
				print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: goes to manager")
				self.bank.manager.acquire()
				try:
					print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: talks to manager")
					time.sleep(random.uniform(0.005, 0.03))  # 5-30 ms manager interaction
					print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: finishes with manager")
				finally:
					self.bank.manager.release()

			print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: goes to safe")
			self.bank.safe.acquire()
			try:
				print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: is in safe")
				time.sleep(random.uniform(0.01, 0.05))
				print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: leaves safe")
			finally:
				self.bank.safe.release()

			print(f"Teller {self.teller_id} [Customer {customer.customer_id}]: tells customer transaction is complete")
			customer.transaction_done.set()

			self.bank.customer_queue.task_done()
