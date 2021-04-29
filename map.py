# Draw functions for map visualizations
#
from alphashape import alphashape
from alphashape import optimizealpha
from descartes import PolygonPatch

import cartopy.crs as ccrs
import cartopy.feature as feature
#import cartopy.mpl.geoaxes.GeoAxes as geoaxes
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

from route import MEAS_AREA

import random;

class Map:
	print("Initializing Map class.")
	plt.figure(figsize=(16,16))
	ax = plt.axes(projection=ccrs.Mercator())
	plt.gcf().set_size_inches(18,8)
	
	print(ax)
	#ax = plt.axes(projection=ccrs.epsg(3067))
	@classmethod
	def init(cls):
		#https://stackoverflow.com/questions/52121498/matplotlib-matplotlibdeprecationwarning
		print("Initializing Map class instance.")
		#plt.figure(figsize=(16,16))
		#print(cls.ax)
		cls.ax = plt.axes(projection=ccrs.Mercator(), label=str(random.randint(0, 1000000)))
		cls.ax.set_xlabel("uniq label" + str(random.randint(0, 1000000)))
		cls.ax.set_ylabel("uniq label" + str(random.randint(0, 1000000)))
		#plt.gcf().set_size_inches(18,8)
		#plt.gcf().set_size_inches(28,18)


	@classmethod
	def draw(cls, title=False, cbar=False, cbar_steps=100, cmap="coolwarm"):
		cls.ax.add_feature(feature.NaturalEarthFeature("physical", "ocean", "10m"))
		cls.ax.add_feature(feature.NaturalEarthFeature("physical", "lakes", "10m"))
		cls.ax.add_feature(
			feature.NaturalEarthFeature(
				"cultural", "admin_0_boundary_lines_land", "10m", facecolor='none'),
			edgecolor='gray')

		# vasen oikea ala ylä
		# limit to Finnish sea area
		#cls.ax.set_extent([1800100, 3400100, 7600100, 8800100], crs=ccrs.Mercator())
		#cls.ax.set_extent([1800100, 3400100, 7800100, 9800100], crs=ccrs.Mercator())

		# limit to reach area
		cls.ax.set_extent([2180000, 3300000, 7900000, 8500000], crs=ccrs.Mercator())
		
		# vähän leveämpi, havainne ennustekuva
		#cls.ax.set_extent([2080000, 3300000, 7990000, 8500000], crs=ccrs.Mercator())
		cls.draw_area(MEAS_AREA, 'black')

		if cbar:
			levels = np.linspace(0, cbar, cbar_steps)
			img = plt.contourf([[0, 0], [0, 0]], levels=levels, cmap=cmap)
			plt.colorbar(img)

		if title:
			plt.title(title)

		return plt
		#return cls.ax

	@classmethod
	def plot_route(cls, x, y, color='red'):
		plt.gca().plot(x, y, color=color, linewidth=1, transform=ccrs.epsg(3067))

	@classmethod
	def draw_area(cls, area, color='red'):
		plt.gca().add_patch(
			patches.Rectangle(
				(area[0], area[2]), area[1] - area[0], area[3] - area[2],
				alpha=0.5, color=color, zorder=3, transform=ccrs.epsg(3067)))

	@classmethod
	def draw_circle(cls, x, y, radius, color):
		#https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.gca.html
		# cls.ax causing problem in ipython
		plt.gca().add_patch(patches.Circle(
			(x, y), radius,
			color=color, alpha=0.8, zorder=3, transform=ccrs.epsg(3067)))

	@classmethod
	def draw_concave_hull(cls, xy):
		#pts = [xy[vertice] for vertice in spatial.ConvexHull(xy).vertices]
		#pts = [xy[vertice] for vertice in alphashape.alphashape(xy, 2).vertices]

		# alpha-parameter can be removed to reoptimize alpha
		#print(optimizealpha(xy, max_iterations=100000))
		#pts = alphashape(xy, 2.2)
		print(len(xy))
		pts = alphashape(xy, 4.235604062127975e-05)

		#pts = alphashape(xy, 7.235604062127975e-06)
		#pts = alphashape(xy, 7.235604062127975e-06)
		#pts = alphashape(xy, 1.9846167135906253e-05)

		#pts = alphashape.alphashape(xy, 2)

		# add 10 km buffer zone for error
		plt.gca().add_patch(
			PolygonPatch(
				pts.buffer(10000),
				color='#de9752', alpha=0.5, zorder=3, transform=ccrs.epsg(3067)))


