import threading
import queue


class Bank:
	"""Shared bank resources and synchronization primitives."""
	def __init__(self):
		self.door = threading.Semaphore(2)
		
		self.safe = threading.Semaphore(2)
		
		self.manager = threading.Semaphore(1)
		
		self.customer_queue = queue.Queue()
		
		self.available_tellers = queue.Queue()
		
		self.customer_arrives = threading.Semaphore(0)
		
		self.teller_available = threading.Semaphore(0)
