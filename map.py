from datetime import timedelta
import itertools
from multiprocessing import Pool
import sys

import alphashape
import cartopy.crs as ccrs
import cartopy.feature as feature
from descartes import PolygonPatch
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pandas as pd


class Map:
	ax = plt.axes(projection=ccrs.Mercator())
	ships = []

	# @.output	list of loaded ship ids
	#
	@classmethod
	def list_ships(self):
		return self.ships

	@classmethod
	def load_ships(self):

		self.ships = pd.read_hdf('ships.h5', 'df').values

	@classmethod
	def draw_map(self):
		ax = self.ax
		ax.add_feature(feature.NaturalEarthFeature("physical", "ocean", "10m"))
		ax.add_feature(feature.NaturalEarthFeature("physical", "lakes", "10m"))
		ax.add_feature(
			feature.NaturalEarthFeature(
				"cultural", "admin_0_boundary_lines_land", "10m", facecolor='none'),
			edgecolor='gray')

		# limit to Finnish sea area
		ax.set_extent([1800100, 3400100, 7800100, 8800100], crs=ccrs.Mercator())

		self.draw_measurement_area()
		return plt

	@classmethod
	def plot_route(self, x, y, color='red'):
		plt.plot(x, y, color=color, linewidth=1, transform=ccrs.epsg(3067))

	@classmethod
	def draw_measurement_area(self):
		area = self.get_measurement_area()
		self.ax.add_patch(
			patches.Rectangle(
				(area[0], area[2]), area[1] - area[0], area[3] - area[2],
				alpha=0.3, color='red', zorder=3, transform=ccrs.epsg(3067)))

	@classmethod
	def draw_concave_hull(self, xy):
		#pts = [xy[vertice] for vertice in spatial.ConvexHull(xy).vertices]
		#pts = [xy[vertice] for vertice in alphashape.alphashape(xy, 2).vertices]

		# alpha-parameter can be removed to reoptimize alpha
		#pts = alphashape.optimizealpha(xy)
		pts = alphashape.alphashape(xy, 1.9846167135906253e-05)

		#pts = alphashape.alphashape(xy, 2)

		# add 10 km buffer zone for error
		self.ax.add_patch(
			PolygonPatch(
				pts.buffer(10000),
				color='green', alpha=0.2, zorder=3, transform=ccrs.epsg(3067)))

	@classmethod
	def get_measurement_area(self):
		#etrs xx yy
		return [340000, 380000, 6620000, 6650000]

	@classmethod
	def get_area_boundaries(self):
		#etrs xx yy
		return [0, 700000, 6450000, 6750000]

	@classmethod
	def route_in_area(self, route, area):

		if len(route['x']) == 0:
			return False

		for i in range(0, len(route['x']) - 1):
			if route['x'][i] > area[0] and route['x'][i] < area[1]:
				if route['y'][i] > area[2] and route['y'][i] < area[3]:
					return True

		return False

	@classmethod
	def draw_reach_area(self, start_date, end_date):
		dates = [r for r in pd.date_range(start_date, end_date)]

		# parallel processing for unix
		if sys.platform == 'posix':
			with Pool() as pool:
				points = pool.map(self.points_reaching_measurement_area, dates)
				pool.close()
				pool.join()
		else:
			points = [self.points_reaching_measurement_area(r) for r in dates]

			self.draw_concave_hull(list(itertools.chain.from_iterable(points)))

	@classmethod
	def points_reaching_measurement_area(map, date):
		starting_points = []
		count1 = 0
		count2 = 0

		for ship in map.ships:
			route = ship.get_route(
				date.timestamp(),
				(date + timedelta(days=1)).timestamp())

			if len(route['x']) > 0:
				count1 += 1

			#col = util.random_color()

			if map.route_in_area(route, map.get_measurement_area()):
				starting_points.append([route['x'][0], route['y'][0]])
				starting_points.append([route['x'][-1], route['y'][-1]])
				count2 += 1

		#print(
		#	f'Laivoja kaikkiaan {len(map.ships)}, {date}. päivänä {count1}, '
		#	f'mittausalueelle ehtii {count2}')

		return starting_points
