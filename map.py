import sys
import cartopy.crs as ccrs
import cartopy.feature as feature
import matplotlib.pyplot as plt
from pyproj import Transformer, Proj
from ship import Ship


#from datetime import datetime

class Map:

	def __init__(self):
		self.ships = []

	# @.output	list of loaded ship ids
	#
	def list_ships(self):
		return self.ships

	# @.input	filename of file that holds AIS data
	# @.output	dictionary
	#		{ ship_id: [
	#			[unixtime, lat, lon], [unixtime, lat, lon], ...] } 
	#

	def load_data(self, filename, limit_to_date = 253385798400000):

		# data is in form:
		# shipid (unixtime lat lon) (unixtime lat lon) (unixtime lat lon) ... \n
		

		with open(filename) as file:

			for raw_line in file.readlines():

				line = raw_line.strip().split(' ')
				ship_id = line[0]

				#locations = []
				x = []
				y = []
				time = []

				for i in range(1, len(line), 3):

					unixtime = int(line[i])

					if unixtime > limit_to_date:
						break

					#locations.append([float(line[x+1]), float(line[x+2]), unixtime])
					x.append(float(line[i+1]))
					y.append(float(line[i+2]))
					time.append(unixtime)

				if x:
					self.ships.append(Ship(ship_id, x, y, time))

	def transform(self, points):
		# projections from WSG 84 to TM35FIN(E,N)
		trans = Transformer.from_proj(Proj(init="epsg:4326"), Proj(init="epsg:3067"))

		res = []
		for pt in trans.itransform(points, time_3rd = True):
			res.append(pt)

		return res

	def draw_map(self):
		
		ax = plt.axes(projection=ccrs.Mercator())
		ax.add_feature(feature.NaturalEarthFeature("physical", "ocean", "10m"))
		ax.add_feature(feature.NaturalEarthFeature("physical", "lakes", "10m"))
		ax.add_feature(
			feature.NaturalEarthFeature("cultural", "admin_0_boundary_lines_land", "10m", facecolor='none'),
			edgecolor='gray')

		# limit to Finnish sea area
		ax.set_extent([1800100,3400100, 7800100,9800100], crs=ccrs.Mercator())
		#ax.set_extent([18, 32, 58, 65], crs=ccrs.PlateCarree())
		#plt.axis([1800100,4300100, 7800100,10100100])

		return plt

	def plot_route(self, x, y):
		plt.plot(x, y, color='red', linewidth=1, transform=ccrs.Geodetic())