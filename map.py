import alphashape
import cartopy.crs as ccrs
import cartopy.feature as feature
from descartes import PolygonPatch
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd


class Map:

	def __init__(self):
		self.ax = plt.axes(projection=ccrs.TransverseMercator())
		self.ships = []

	# @.output	list of loaded ship ids
	#
	def list_ships(self):
		return self.ships

	def load_ships(self):

		self.ships = pd.read_hdf('ships.h5', 'df').values

	def draw_map(self):
		ax = self.ax
		ax.add_feature(feature.NaturalEarthFeature("physical", "ocean", "10m"))
		ax.add_feature(feature.NaturalEarthFeature("physical", "lakes", "10m"))
		ax.add_feature(
			feature.NaturalEarthFeature("cultural", "admin_0_boundary_lines_land", "10m", facecolor='none'),
			edgecolor='gray')

		# limit to Finnish sea area
		ax.set_extent([1800100, 3400100, 7800100, 8800100], crs=ccrs.Mercator())

		self.draw_measurement_area()
		return plt

	def plot_route(self, x, y, color='red'):
		plt.plot(x, y, color=color, linewidth=1, transform=ccrs.epsg(3067))

	def draw_measurement_area(self):
		area = self.get_measurement_area()
		self.ax.add_patch(
			patches.Rectangle(
				(area[0], area[2]), area[1] - area[0], area[3] - area[2],
				alpha=0.3, color='red', zorder=3, transform=ccrs.epsg(3067)))

	def draw_concave_hull(self, xy):
		#pts = [xy[vertice] for vertice in spatial.ConvexHull(xy).vertices]
		#pts = [xy[vertice] for vertice in alphashape.alphashape(xy, 2).vertices]

		# alpha-parameter can be removed to reoptimize alpha
		#pts = alphashape.optimizealpha(xy)
		pts = alphashape.alphashape(xy, 1.9846167135906253e-05)

		print(pts)
		#pts = alphashape.alphashape(xy, 2)

		# add 10 km buffer zone for error
		self.ax.add_patch(
			PolygonPatch(
				pts.buffer(10000),
				color='green', alpha=0.2, zorder=3, transform=ccrs.epsg(3067)))

	def get_measurement_area(self):
		#etrs xx yy
		return [340000, 380000, 6620000, 6650000]

	def route_in_area(self, route, area):

		if len(route['x']) == 0:
			return False

		#print("routessa pisteitä",len(route['x']))
		#print(route['x'])
		#print(route['y'])
		#print(area)

		for i in range(0, len(route['x']) - 1):
			if route['x'][i] > area[0] and route['x'][i] < area[1]:
				if route['y'][i] > area[2] and route['y'][i] < area[3]:
					return True

		return False
