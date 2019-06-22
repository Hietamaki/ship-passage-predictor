import sys
from pyproj import Transformer, Proj
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from cartopy.io import shapereader
import cartopy.feature as feature

import numpy as np
import geopandas

#from datetime import datetime

class Ships:

	def __init__(self):
		self.data = {}

	# @.output	list of loaded ship ids
	#
	def list_ships(self):
		return list(self.data.keys())

	# @.input	filename of file that holds AIS data
	# @.output	dictionary
	#		{ ship_id: [
	#			[unixtime, lat, lon], [unixtime, lat, lon], ...] } 
	#

	def load_data(self, filename, limit_to_date = sys.maxsize):

		# data is in form:
		# shipid (unixtime lat lon) (unixtime lat lon) (unixtime lat lon) ... \n
		

		with open(filename) as file:

			for raw_line in file.readlines():

				line = raw_line.strip().split(' ')
				ship_id = line[0]

				locations = []

				for x in range(1, len(line), 3):

					unixtime = int(line[x])

					if unixtime > limit_to_date:
						#if (line[0] == "230992680"):
						#	print("line[x]:       %s >" % format_date(line[x]))
						#	print("LIMIT_TO_DATE: %s" % format_date(LIMIT_TO_DATE))
						break

					locations.append([float(line[x+1]), float(line[x+2]), unixtime])

				if locations:
					self.data[ship_id] = locations

	def transform(self, points):
		# projections from WSG 84 to TM35FIN(E,N)
		trans = Transformer.from_proj(Proj(init="epsg:4326"), Proj(init="epsg:3067"))

		res = []
		for pt in trans.itransform(points, time_3rd = True):
			res.append(pt)

		return res

	def draw_map(self):
		shpfilename = shapereader.natural_earth("10m", "physical", "land")
		#df = geopandas.read_file(shpfilename)
		poly = shapereader.Reader(shpfilename).geometries()
		#print(poly)

		ax = plt.axes(projection=ccrs.PlateCarree())
		#ax = plt.axes(projection=ccrs.epsg(3067))
		ax.add_geometries(poly, crs=ccrs.PlateCarree(), facecolor='none', edgecolor='0.5')
		#ax.set_extent([18, 32, 58, 65], crs=ccrs.PlateCarree())
		#ax.set_extent([18, 32, 58, 65], crs=ccrs.PlateCarree())
		ax.add_feature(feature.NaturalEarthFeature("physical", "ocean", "10m"))
		#ax.add_feature(feature.NaturalEarthFeature("physical", "land", "50m"))




		return plt