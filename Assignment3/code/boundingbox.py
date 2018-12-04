import numpy as np

class BoundingBox:
	"""
	A bounding box (shortened to bbox) is an area defined by the vectors x and y
	This class allows the user to be more flexible in case where bbox reductions
	induced by recursive algorithms.

	NOTICE the class does not test for invalid bboxes, (x_max < x_min)
	"""
	def __init__(self, min_x, max_x, min_y, max_y):
		"""
		Creates a BoundingBox

		:param min_x: minimum x value
		:param max_x: maximum x value
		:param min_y: minimum y value
		:param max_y: maximum y value

		:Example:
		>>> BoundingBox(0,1,2,4)
		"""
		self.data = np.array([[min_x, max_x],[ min_y, max_y]],np.float)

	def lower_left(self):
		"""
		Returns the lower left tuple
		:Example:
		>>> print(bbox.lower_left())
		<<< (0.0, 2.0)
		"""
		return (self.data[0,0],self.data[1,0])

	def width(self):
		"""
		Returns the bbox's width
		:Example:
		>>> print(bbox.width())
		<<< 1.0
		"""
		return self.data[0,1] - self.data[0,0]
	
	def height(self):
		"""
		Returns the bbox's height
		:Example:
		>>> print(bbox.height())
		<<< 2.0
		"""
		return self.data[1,1] - self.data[1,0]

	def within(self,value, axis):
		"""
		Tests wheter the given value on that axis is within/touches
		the boundingbox.

		:Example:
		>>> print(bbox.within(3,1))
		<<< True	
		""" 
		ax = self.data[axis,:]
		return ax[0]<= value and value <= ax[1]

	def partition(self,value, axis):
		"""
		Tests and returns wheter the given value falls inside of the
		partitions, frot the given axis.

		:Example:
		y:	min		max
			|		|
			|		|
            2       4
		               5
			return (2 < 5, 5 < 4)
		>>> print(bbox.partition(5,1))
		<<< (True, False)	
		""" 
		return (self.data[axis,0] <= value, value <= self.data[axis,1])

	def reduce_min(self,axis, value):
		"""
		Returns a reduced (in area) BoundingBox, by reducing
		the minimum side of an axis.

		:Example:
		>>> print(bbox.reduce_min(0,0.3))
		<<< [[ 0.3  1. ]
 			 [ 2.   4. ]]
		""" 
		bb = BoundingBox.from_matrix(self.data)
		bb.data[axis,0] = value
		return bb

	def reduce_max(self,axis, value):
		"""
		Returns a reduced (in area) BoundingBox, by reducing
		the maximum side of an axis.

		:Example:
		>>> print(bbox.reduce_max(0,0.3))
		<<< [[ 0.  0.3 ]
 			 [ 2.  4. ]]
		""" 
		bb = BoundingBox.from_matrix(self.data)
		bb.data[axis,1] = value
		return bb

	def reduce_min_by(self,axis, value):
		"""
		Returns a reduced (in area) BoundingBox, by reducing
		the minimum side of an axis.

		:Example:
		>>> print(bbox.reduce_min_by(0,0.3))
		<<< [[ 0.3  1. ]
			 [ 2.   4. ]]
		""" 
		bb = BoundingBox.from_matrix(self.data)
		bb.data[axis,0] += value
		return bb

	def reduce_max_by(self,axis, value):
		"""
		Returns a reduced (in area) BoundingBox, by reducing
		the maximum side of an axis.

		:Example:
		>>> print(bbox.reduce_max_by(0,0.3))
		<<< [[ 0.   0.7]
 			 [ 2.   4. ]]
		""" 
		bb = BoundingBox.from_matrix(self.data)
		bb.data[axis,1] -= value
		return bb

	def centroid(self):
		"""
		Returns the center of the BoundingBox

		:Example:
		>>> print(bbox.centroid())
		<<< [0.5, 3.0]

		""" 
		return [self.data[0,0] + self.width() / 2.0, self.data[1,0] + self.height() / 2.0]

	def __str__(self):
		"""
		Returns the string representation this class.

		:Example:
		>>> print(bbox)
		<<< [[ 0.  1.]
 			 [ 2.  4.]]
		""" 
		return str(self.data)

	@staticmethod	
	def from_matrix(data):
		"""
		Creates a BoundingBox from a numpy array/matrix type

		:Example:
		>>> print(BoundingBox.from_matrix(np.array([[0, 1],[ 2, 4]])))
		<<< [[ 0.  1.]
 			 [ 2.  4.]]
		""" 		
		return BoundingBox(data[0,0],data[0,1],data[1,0],data[1,1])
	
	@staticmethod
	def from_dataset(data, xindex = 1, yindex = 2):
		"""
		Creates a BoundingBox from a dataset a numpy array/matrix type

		:Example:
				     x  , y 
		>>> data = [[0  , 1],
					[0.5, 3],
					[2  , 4]]
		>>> print(BoundingBox.from_dataset(data))
		<<< [[ 0.  2.]
 			 [ 1.  4.]]
		""" 				
		minx = np.min(data[:,xindex],axis=0)
		maxx = np.max(data[:,xindex],axis=0)
		miny = np.min(data[:,yindex],axis=0)
		maxy = np.max(data[:,yindex],axis=0)

		return BoundingBox(minx,maxx,miny,maxy)

if __name__ == '__main__':

	bbox = BoundingBox(0,1,2,4)
	print(bbox.lower_left())
	print(bbox.width())
	print(bbox.height())
	print(bbox.within(3,1))
	print(bbox.partition(5,1))
	print(bbox.reduce_min(0,0.3))
	print(bbox.reduce_max(0,0.3))
	print(bbox.reduce_min_by(0,0.3))
	print(bbox.reduce_max_by(0,0.3))
	print(bbox.centroid())
	print(bbox)
	print(BoundingBox.from_matrix(np.array([[0, 1],[ 2, 4]])))

	data = np.array([[0, 1],[0.5,3],[ 2, 4]])
	print(data)
	print(BoundingBox.from_dataset(data,0,1))
	



