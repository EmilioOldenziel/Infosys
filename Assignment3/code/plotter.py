import boundingbox as bb
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from matplotlib.collections import PatchCollection
import matplotlib

import numpy as np


class Plotter:
	
	def __init__(self,kdtree,database,args):
		self.kdtree = kdtree
		self.db = database
		self.args = args
		#### LAB
		self.quadtree = None
		self.closest = None
		

	def create_patches():
		patches = []
		if rq is not None:
			patches.append(plt.Rectangle(rq.lower_left(),rq.width(),rq.height()))

		for r in bboxes[bboxdepth]:
			x = r.data[0,:]
			y = r.data[1,:]
			rect = plt.Rectangle((x[0],y[0]), x[1] - x[0], y[1] - y[0], ec="none",edgecolor='black')
			patches.append(rect)


		colors = np.linspace(0, 100, len(patches) + 1)
		collection = mpatches.PatchCollection(patches, cmap=plt.cm.jet, alpha=0.3)
		collection.set_edgecolor([0,0,0])
		collection.set_array(np.array(colors))
		
		return collection

	def plot(self):
		self.fig, self.ax = plt.subplots()

		if self.args.plot == "kdtree-bb":
			self.plot_tree()
	
		if self.args.plot == "storage":
			self.plot_storage()

		if self.quadtree is not None:
			self.plot_quadtree()

		if self.closest is not None:
			self.plot_closest_pair()
	
		plt.show()
	
	def plot_storage(self):
		index = []
		elements = []
		for elem in self.kdtree.storage:
			if "index" in elem:
				num_elem = 0
				if "elements" in  elem:
					num_elem = len(elem["elements"])
				index.append(elem["index"])
				elements.append(num_elem)
		
		plt.plot(index,elements)
		self.ax.set_xlabel("Storage index")
		self.ax.set_ylabel("# Elements")
		self.ax.set_title("Tree depth:" + str(self.kdtree.max_depth))


	def plot_tree(self):

		# 1: plot all datapoints
		keys = self.db.keys()
		data = np.asarray(self.db.query(keys))	
		
		# @todo change database info
		column = {"key":0,"x":1,"y":2}
		
		if self.args.quadlevel:
			column["quad"] = 3
			data = data[data[:,column["quad"]] < self.args.quadlevel]

		markersize = 0.5		
		if len(data) < 100:
			markersize = 4	

		plt.plot(data[:,column["x"]], data[:,column["y"]], 'ko', markersize=markersize)

		# 2: plot all boundingboxes/partitions
		bboxes = self.kdtree.partitions()
		patches = []

		for b in bboxes[self.args.bbox_depth]:
			rect = plt.Rectangle(b.lower_left(), b.width(),b.height(), ec="none",edgecolor='black')
			patches.append(rect)

		# 3: show range query
		if self.args.range_query:
			rq = bb.BoundingBox.from_matrix(np.matrix(self.args.range_query))
			patches.append(plt.Rectangle(rq.lower_left(),rq.width(),rq.height()))
			
			rkeys = self.kdtree.rquery(rq)
			NN = np.asarray(self.db.query(rkeys))
			plt.plot(NN[:,column["x"]], NN[:,column["y"]], 'rs', markersize=markersize + 4)	

			for point in NN:
				if rq.within(point[1],0):
					if rq.within(point[2],1):
						plt.plot([point[1]],[point[2]], 'bs', markersize=markersize + 4)	

		colors = np.linspace(0, 100, len(patches) + 1)
		collection = PatchCollection(patches, cmap=plt.cm.jet, alpha=0.3)
		collection.set_edgecolor([0,0,0])
		collection.set_array(np.array(colors))
		
		self.ax.add_collection(collection)

	def add_quadtree(self,quadtree):
		self.quadtree = quadtree
	

	def plot_quadtree(self):
		qt_depth = max(self.quadtree.quads.keys())
			
		patches = []
		for q in self.quadtree.quads[qt_depth]:
			rect = plt.Rectangle(q.lower_left(), q.width(),q.height())
			patches.append(rect)
		collection = PatchCollection(patches)
		collection.set_edgecolor([0,0,0])
		self.ax.add_collection(collection)

	def add_closest_query(self, query_point, closest_point):
		self.closest = { "query" : query_point, "closest": closest_point }
	
	def plot_closest_pair(self):
		plt.plot(self.closest["query"][0], self.closest["query"][1], 'X', markersize=5)
		plt.plot(self.closest["closest"][0], self.closest["closest"][1], 'P', markersize=5)
				


	
