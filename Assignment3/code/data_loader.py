import os
from osgeo import ogr

class DataLoader:
	
	def load_shape_file(self,filename, database):

		shapefile = filename
		driver = ogr.GetDriverByName("ESRI Shapefile")
		dataSource = driver.Open(shapefile, 0)
		layer = dataSource.GetLayer()
	
		for feature in layer:
			center = feature.GetGeometryRef().Centroid()
			database.insert([center.GetX(), center.GetY()])

	def load_wiki_example_data(self,database):
		data = [[2,3], [5,4], [9,6], [4,7], [8,1], [7,2]]
		database.insert_iterable(data)

	def load(self,args, database):
		if args.filename:
			self.load_shape_file(args.filename, database)	
		else:
			self.load_wiki_example_data(database)
