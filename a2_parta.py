
class HashTable:

	# You cannot change the function prototypes below.  Other than that
	# how you implement the class is your choice as long as it is a hash table

    def __init__(self, initial_capacity=32):
        # Initialize buckets and related attributes
        self.buckets = [[] for _ in range(initial_capacity)]
        self._capacity = initial_capacity
        self._size = 0  # Number of key-value pairs

    def hash(self, key):
        # Compute bucket index
        return hash(key) % self._capacity

    def insert(self, key, value):
        # Add key-value if key doesn't exist
        bucket_index = self.hash(key)
        for item in self.buckets[bucket_index]:
            if item[0] == key:
                return False
        self.buckets[bucket_index].append((key, value))
        self._size += 1
        # Resize if load factor exceeds 0.7
        if self._size / self._capacity > 0.7:
            self._resize()
        return True

    def modify(self, key, value):
        # Update value if key exists
        bucket_index = self.hash(key)
        for i, item in enumerate(self.buckets[bucket_index]):
            if item[0] == key:
                self.buckets[bucket_index][i] = (key, value)
                return True
        return False

    def remove(self, key):
        # Remove key-value if key exists
        bucket_index = self.hash(key)
        for i, item in enumerate(self.buckets[bucket_index]):
            if item[0] == key:
                del self.buckets[bucket_index][i]
                self._size -= 1
                return True
        return False

    def search(self, key):
        # Get value for key if it exists
        bucket_index = self.hash(key)
        for item in self.buckets[bucket_index]:
            if item[0] == key:
                return item[1]
        return None

    def _resize(self):
        # Double capacity and rehash all elements
        new_capacity = self._capacity * 2
        new_buckets = [[] for _ in range(new_capacity)]
        for bucket in self.buckets:
            for key, value in bucket:
                new_index = hash(key) % new_capacity
                new_buckets[new_index].append((key, value))
        self.buckets = new_buckets
        self._capacity = new_capacity

    def capacity(self):
        return self._capacity # Return number of buckets

    def __len__(self):
        return self._size # Return number of key-value pairs
