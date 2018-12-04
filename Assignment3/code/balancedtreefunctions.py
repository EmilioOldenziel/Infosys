import math

class BalancedTreeFunctions:
	
	@staticmethod	
	def tree_depth(num):		
		return int(math.ceil(math.log(num,2)))

	@staticmethod
	def tree_depth_max_leave_elements(total_size,max_in_leave):
		pw_size = 2 ** BalancedTreeFunctions.tree_depth(total_size)

		depth = 1
		while pw_size > max_in_leave:
			pw_size = pw_size >> 1
			depth += 1

		return depth

			


		
		
