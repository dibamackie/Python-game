

class Stack:

	def __init__(self, cap=10):
		self.cap = cap
		self.stack = [None] * self.cap
		self.size = 0

	# resize function that will double the capacity of the stack and will copy each element into the new stack, and finally will update the reference to it.
	def _resize(self):
		new_capacity = self.cap * 2 
		new_stack = [None] * new_capacity  

		for i in range(self.size):
			new_stack[i] = self.stack[i]    
		self.stack = new_stack 
		self.cap = new_capacity  

	# helper function to see if the stack is full
	def is_full(self):
		return self.size >= self.cap	

	# will return the capacity of the stack
	def capacity(self):
		return self.cap

	# will check if the stack is full, if it is, it will resize it, otherwise, it will push the data into the last index and finally, it will increase its size by 1.
	def push(self, data):
		if self.is_full():
			self._resize()
		self.stack[self.size] = data
		self.size += 1
	
	# method will check if it is empty first and will throw and error if it is. Then size will decrease in order to access the last element of the stack.
	# item will hold the element to be removed and will be returned in the last statement. lastly, the popped element will be erased into None.
	def pop(self):
		if self.is_empty():
			raise IndexError('pop() used on empty stack')
		self.size -= 1
		item = self.stack[self.size]
		self.stack[self.size] = None

		return item

	# checks if the stack is empty, and will return the element on top. In order to address indexing, we must remove 1 from the size to access the last element.
	def get_top(self):
		if self.is_empty():
			return None
		return self.stack[self.size - 1]

	# check if the stack is empty
	def is_empty(self):
		return self.size == 0
	# helper function to get lenght of the stack.
	def __len__(self):
		return self.size


class Queue:


	def __init__(self, cap=10):
		self.cap = cap
		self.queue = [None] * cap
		self.size = 0
		self.front = 0
		self.back = 0

	# helper resize function to address size issues. Will double the current storage.
	# will copy and paste new elements into the new queue based on circular queue expression.
	def _resize(self):
		new_cap = self.cap * 2
		new_queue = [None] * new_cap
		for i in range(self.size):
			new_queue[i] = self.queue[(self.front + i) % self.cap]
		self.queue = new_queue
		self.front = 0
		self.back = self.size
		self.cap = new_cap

	# will return the capacity of the queue
	def capacity(self):
		return self.cap

	# will check if the queue has enough space, if it is at maximum capacity it will resize it.
	# will insert data in self.back index and will increase the size count of the queue.
	def enqueue(self, data):
		if self.size == self.cap:
			self._resize() 
		self.queue[self.back] = data
		self.back = (self.back + 1) % self.cap  
		self.size += 1  

	# this method will check if the queue is empty, if not, it will proceed to get the front element and set its data to None but before its contents will be stored in the item variable.
	# then the front pointer will be moved into the new front item and the size will be reduced by 1.
	def dequeue(self):
		if self.is_empty():
			raise IndexError('dequeue() used on empty queue')
		item = self.queue[self.front]
		self.queue[self.front] = None
		self.front = (self.front + 1) % self.cap
		self.size -= 1

		return item 

	#helper function to get the front element of the queue
	def get_front(self):
		if self.is_empty():
			return None
		return self.queue[self.front]

	#checks if the queue is empty
	def is_empty(self):
		return self.size == 0

	# length of the queue
	def __len__(self):
		return self.size



class Deque:

	def __init__(self, cap=10):
		self.cap = cap
		self.deque = [None] * cap
		self.size = 0
		self.front = 0
		self.back = 0

	# helper function that will resize the deque if the it has reached its maximum capacity.
	# the  function will create a new deque that will have the data from the original deque
	# and finally the reference to the new deque will be updated.
	def _resize(self):
		new_cap = self.cap * 2
		new_deque = [None] * new_cap
		for i in range(self.size):
			new_deque[i] = self.deque[(self.front + i) % self.cap]
		self.deque = new_deque
		self.front = 0
		self.back = self.size
		self.cap = new_cap

	#returns capacity of the deque
	def capacity(self):
		return self.cap

	# checks the deque maximum capacity and resizes if necessary
	# will get the front element and will insert the data into it
	# finally, the size of the deque will be increased by 1.
	def push_front(self, data):
		if self.size == self.cap:
			self._resize() 
		self.front = (self.front - 1) % self.cap  
		self.deque[self.front] = data
		self.size += 1  

	# checks the deque maximum capacity and resizes if necessary
	# will get the back element and will insert the data into it
	# finally, the size of the deque will be increased by 1.
	def push_back(self, data):
		if self.size == self.cap:
			self._resize()
		self.deque[self.back] = data
		self.back = (self.back + 1) % self.cap
		self.size += 1

	#checks if the deque if empty and throws an error if it is.
	#stores the front item of the deque and then removes its data.
	#adjust front deque item, reduces the deque size and returns the item removed.
	def pop_front(self):
		if self.is_empty():
			raise IndexError('pop_front() used on empty deque')
		item = self.deque[self.front]
		self.deque[self.front] = None
		self.front = (self.front + 1) % self.cap
		self.size -= 1
		return item
	
	#checks if the deque if empty and throws an error if it is.
	#stores the back item of the deque and then removes its data.
	#adjust back deque item, reduces the deque size and returns the item removed.
	def pop_back(self):
		if self.is_empty():
			raise IndexError('pop_back() used on empty deque')
		item = self.deque[(self.back - 1) % self.cap]
		self.deque[(self.back - 1) % self.cap] = None
		self.back = (self.back - 1) % self.cap
		self.size -= 1
		return item

	# returns the front item of the deque
	def get_front(self):
		if self.is_empty():
			return None
		return self.deque[self.front]

	#returns the back item of the deque
	def get_back(self):
		if self.is_empty():
			return None
		return self.deque[(self.back - 1 ) % self.cap]

	# funtion to check if the deque is empty
	def is_empty(self):
		return self.size == 0

	# function the retrive the length of the deque
	def __len__(self):
		return self.size

	#checks if k is out of range
	#then calculates the index starting from the front
	#returns the element at the current calculated index.
	def __getitem__(self, k):
		if k < 0 or k >= self.size:
			raise IndexError('Index out of range')
		current_index = (self.front + k) % self.cap

		return self.deque[current_index]