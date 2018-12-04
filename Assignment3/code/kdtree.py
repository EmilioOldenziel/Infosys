import numpy as np
import math
import boundingbox as bb
import database as db
import storageindex as si
import balancedtreefunctions as btf

class KDTree:
	"""
	A kd tree implementation.

	The KDTree is initialized with a Database and a set of options,
	and is constructed as follows:
	
	:Example:
	>>> data = [[2,3], [5,4], [9,6], [4,7], [8,1], [7,2]]
	>>> database = db.Database(["x","y"])
	>>> database.insert_iterable(data)
	>>> tree = KDTree(database,{"max-depth":3})

	the supported options are:
		1. max-depth    : the maximum tree depth
		2. max-elements : maximum amount of elements in leave nodes
		incase depth is not sufficient for max-elements, the depth is recalculated

	the tree is internally stored in an array containing the following information:
	>>> for node in tree.storage:
	>>>		print(node)
	<<< {'index': 1, 'depth': 0, 'partition': 5, 'axis': 0}
	<<<	{'index': 2, 'depth': 1, 'partition': 4, 'axis': 1}
	<<< {'index': 3, 'depth': 1, 'partition': 2, 'axis': 1}
	<<< {'index': 4, 'depth': 2, 'elements': array([1, 2]), 'axis': 0}
	<<<	{'index': 5, 'depth': 2, 'elements': array([4]), 'axis': 0}
	<<<	{'index': 6, 'depth': 2, 'elements': array([5, 6]), 'axis': 0}
	<<<	{'index': 7, 'depth': 2, 'elements': array([3]), 'axis': 0}	
	
		where
			index		: is the node's binary tree index (breadth first)
			depth 		: is the depth of the node
			partition	: on what value the space was partitioned
			elements	: the keys stored in this node (unique key in Database)
			axis		: the current axis (is depth % dimension)
	"""
	def __init__(self, db, options):
		"""
		Create a new KDTree instance.
		:param db		: Database with fields x,y
		:param options	: options for configuring the KDTree

		:Example:
		>>>	tree = KDTree(database,{"max-depth":3})
		"""
		keys = db.keys()
		data = np.asarray(db.query(keys))
		treef= btf.BalancedTreeFunctions

		if "max-depth" in options:
			self.max_depth = options["max-depth"]
		else:
			self.max_depth = treef.tree_depth(len(data))
		
		if "max-elements" in options:
			max_elem_depth = treef.tree_depth_max_leave_elements(len(data),options["max-elements"])
			if self.max_depth < max_elem_depth:
				self.max_depth = max_elem_depth
			
		self.partition = lambda x, index: np.argsort(x[:,index],axis=0)

		storage_size = int(math.pow(2,self.max_depth)-1)

		self.storage = storage = [{} for x in range(storage_size)]	

		self.traverse(data)

		self.bb = bb.BoundingBox.from_dataset(data,db.fields()["x"],db.fields()["y"])				  
	
	def bounding_box(self):
		"""
		Returns the Minimum BoundingBox (MBR) of the KDTree
		
		:Example:
		>>> print(tree.bounding_box())
		<<< [[ 2.  9.]
 			 [ 1.  7.]]
		"""
		return self.bb

	def traverse(self,mtrx, depth = 0, sidx = si.StorageIndex()): 
		"""
		Internal used method for creating the QuadTree.

		This method will be called recursively until the maximum depth
		is reached. In every step it will split the data along a certain
		axis into two equal sized (median) partitions.

		Technically the partion function only needs to be called once,
		but is done repeatedly for clarity.
		"""
		axis = depth % 2		
        
		self.storage[sidx.storage()]["index"] = sidx.tree()
		self.storage[sidx.storage()]["depth"] = depth
		self.storage[sidx.storage()]["axis"] = axis		
    	
		# if no more splitting, store ids from the matrix
		if len(mtrx) == 1 or depth + 1 == self.max_depth:
			self.storage[sidx.storage()]["elements"] = mtrx[:,0]
		else:
			# order the matrix, and partition
			order = np.array_split(self.partition(mtrx,axis + 1),2)			
			self.storage[sidx.storage()]["partition"] = mtrx[order[0][-1],axis + 1]
			self.traverse(mtrx[order[0],:], depth + 1, sidx.left())
			self.traverse(mtrx[order[1],:], depth + 1, sidx.right())
	
	def partitions(self):
		"""
		Returns a dictionary containing lists of BoundingBoxes.
		{
			0 : [ 1 x BoundingBox]
			1 : [ 2 x BoundingBox]
			2 : [ 4 x BoundingBox]
		}

			where the key represents the depth, and the collection of BoundingBoxes
			make up the entire space containing this KDTree
		
		:Example:
		>>> for k,v in tree.partitions().items():
		>>>		print(k,len(v))
		<<< (0, 1)
		<<< (1, 2)
		<<< (2, 4)
		"""
		bounding_boxes = {}
		sidx = si.StorageIndex()
		self.traverse_partition(0,sidx,bounding_boxes,self.bb)
		return bounding_boxes
	
	def traverse_partition(self,depth, sidx, bboxes, box):
		"""
		Internal method used for collecting the bounding boxes per depth

		This method will be called recursively until all the BoundingBoxes
		have been collected.
		"""
		if depth not in bboxes:
			bboxes[depth] = []
			
		bboxes[depth].append(box)

		if "index" in self.storage[sidx.storage()]:			
			axis = depth % 2

			# there was further partitioning
			if "partition" in self.storage[sidx.storage()]:
				
				left_box = box.reduce_max(axis,self.storage[sidx.storage()]["partition"])
				right_box = box.reduce_min(axis,self.storage[sidx.storage()]["partition"])
			
				self.traverse_partition(depth + 1, sidx.left(), bboxes, left_box)
				self.traverse_partition(depth + 1, sidx.right(), bboxes, right_box)

			else:		
				return
	
	def rquery(self,bbox = [], sidx = si.StorageIndex()):
		"""
		Returns a list of unique keys that fell within the provided BoundingBox.
		
		:param bbox: the current BoundingBox that will be searched
		:param sidx: helper class for Binary Tree traversal
		
		>>> bbox = bb.BoundingBox(1,2,1,2)
		>>>	print(tree.rquery(bbox))		
		<<< [1, 2]
		
		>>> print(database.query(tree.rquery(bbox)))
		<<< [[1, 2, 3], [2, 5, 4]]		
		"""
		if "elements" in self.storage[sidx.storage()]:
			return self.storage[sidx.storage()]["elements"]
	
		else:
			axis = self.storage[sidx.storage()]["axis"]
			partition = self.storage[sidx.storage()]["partition"]
			lr = bbox.partition(partition,axis)

			boxes = []
			if lr[0]:
				boxes.extend(self.rquery(bbox,sidx.left()))
			if lr[1]:
				boxes.extend(self.rquery(bbox,sidx.right()))

		return boxes
		
	def closest(self, point, sidx = si.StorageIndex()):

		if "elements" in self.storage[sidx.storage()]:
			return self.storage[sidx.storage()]["elements"]
		else: 
			axis = self.storage[sidx.storage()]["axis"]
			partition = self.storage[sidx.storage()]["partition"]
	
			leaf_points = []
			if point[axis] < partition: 
				leaf_points.extend(self.closest(point, sidx.left()))
			else: 
				leaf_points.extend(self.closest(point, sidx.right()))

		return leaf_points


if __name__ == '__main__':
		
	data = [[2,3], [5,4], [9,6], [4,7], [8,1], [7,2]]
	database = db.Database(["x","y"])
	database.insert_iterable(data)	

	tree = KDTree(database,{"max-depth":3})
	for node in tree.storage:
		print(node)

	print(tree.bounding_box())

	for k,v in tree.partitions().items():
		print(k,len(v))
	
	bbox = bb.BoundingBox(1,2,1,2)
	print(tree.rquery(bbox))
	print (database.query(tree.rquery(bbox)))

	print("closest")
	print(tree.closest([7,2]))