class StorageIndex:
	
	def __init__(self, index = 1):
		self.index = index

	def tree(self):
		return self.index

	def storage(self):
		return self.index - 1

	def left(self):
		return StorageIndex(self.index * 2)

	def right(self):
		return StorageIndex(self.index * 2 + 1)	

	
