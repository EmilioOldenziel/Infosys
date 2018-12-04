class Database:
	"""
	An minimal database implementation, with the focus on storing 
	matrices.	
	"""
	def __init__(self, fields):
		"""
		Create a new Database instance.
		:param fields: a list containing the field names

		:Example:
		>>> db = Database(["x","y","quad-lvl"])
		"""
		self.db = {}
		self.fields_ = {"key" : 0}
		for field in fields:
			self.fields_[field] = len(self.fields_)

		self.unique_key = 0
		self.num_fields = len(self.fields_) - 1 
	
	def fields(self):
		"""
		Returns the Database's field list
		
		:Example:
		>>> db.fields()
		<<< {'key': 0, 'quad-lvl': 3, 'x': 1, 'y': 2}
		"""
		return self.fields_
		

	def insert(self,record):
		"""
		Insert's a record into the database and return's
		unique key.
		
		:param record: a list containing the fields value in order
											

		:Example:
		>>> print(db.insert([1,2]))
		<<< 1
	
		>>> print(db.insert([1,2,3]))
		<<< 2
		"""
		if len(record) > self.num_fields:
			raise ValueError('This record contains has invalid length.')
		
		record.extend([0 for x in range(self.num_fields - len(record))])

		self.unique_key += 1	
		record.insert(0,self.unique_key)	
		self.db[self.unique_key] = record
		
		return self.unique_key

	def insert_iterable(self, records):
		"""
		Inserts a record collection into the database and return's
		the corresponding list of unique keys.
		
		:param record: a collection of records, see insert(self,record)
											
		:Example:
		>>> print(db.insert_iterable([[2,3],[3,4,5]]))
		<<< [3, 4]
		"""
		return [ self.insert(record) for record in records]

	def query(self, key):
		"""
		Returns a list of records in order of the requested keys.
		The first field of each record corresponds to the unique key.
		
		:param key: a collection or a single key

		:Example:
		>>> db.query(2)
		<<< [2, 1, 2, 3]

		>>> db.query([2, 4])
		<<< [[2, 1, 2, 3], [4, 3, 4, 5]]
		"""
		if isinstance(key,int):
			if key in self.db:
				return self.db[key]
			return None
		try:
			return [self.db[k] for k in key if k in self.db] 
		except ValueError:
			pass

		return None

	def keys(self):
		"""
		Returns all the unique keys

		:Example:
		>>> print(db.keys())
		<<< [1, 2, 3, 4]
		"""
		return [x for x in self.db.keys()]

	def update(self,key,index,value):
		"""
		Updates a value for a field given the key 

		:param key	: unique key 
		:param index: index in the field to update
		:param value: the new value

		:Example:
		>>> db.update(1,0,9)
		"""
		self.db[key][index] = value
	
	def update_field(self,key,field,value):
		"""
		Updates a value for a field given the key 

		:param key	: unique key 
		:param field: the field to updated
		:param value: the new value

		:Example:
		>>> db.update_field(1,"x",9)
		"""
		self.update(key,self.fields_[field],value)

if __name__ == '__main__':

	# 1 creating a database with the following fields in order:	
	db = Database(["x","y","quad-lvl"])
		
	print("Creating a database")	
	for name,index in db.fields().items():
		print("name: %s Index: %i" % (name,index))

	# adding contents
	print("Adding contents")	
	db.insert([1,2])
	db.insert([1,2,3])
	db.insert_iterable([[2,3],[3,4,5]])

	db.update_field(1,"x",9)
	db.update(1,2,10)
	for record in db.query(db.keys()):
		print ("record", record)

	





 
	
