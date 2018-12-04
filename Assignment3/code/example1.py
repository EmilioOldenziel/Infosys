import numpy as np
import scipy.spatial as sp
import database as db
import kdtree as kdt


my_db =  db.Database()
my_db.insert_iterable([[1,1],[1,2],[4,5],[1,2],[3,4], [5,2.5], [10,1.2], [5,2.5], [10,1.2], [7,7], [5,3],[6,1], [3.5,4.5]])


partition = lambda x, index: np.argsort(x[:,index],axis=0)

keys = my_db.keys()
data = np.asarray(my_db.query(keys))


	
print(data)

def rec(mtrx, indices, depth, si, storage): 
	axis = depth % 2	
	order = np.array_split(partition(mtrx[indices,:],axis + 1),2)
	

	#print ("----------")
	#print (indices)
	#print (mtrx[order[0],:])
	#print (mtrx[order[1],:])

    
	storage[si-1]["index"] = si
	storage[si-1]["depth"] = depth
	storage[si-1]["axis"] = axis
	storage[si-1]["partition"] = mtrx[order[0][-1],axis + 1]
	storage[si-1]["elements"] = []
    


	if depth == 2:
		storage[si-1]["elements"] = indices
		return 

	rec(mtrx,[indices[x] for x in order[0]], depth + 1, si * 2, storage)
	rec(mtrx,[indices[x] for x in order[1]], depth + 1, si * 2 + 1, storage)


storage = [{} for x in range(data.shape[0])]
rec(data,[x for x in range(data.shape[0])],0,1,storage)

for x in storage:
	print(x)










#print(data)
#print(mydata)
#print(partition(mydata,1))
#print(np.split(partition(mydata,1),2))


