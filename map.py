# Draw functions for map visualizations
#
#from alphashape import alphashape
import cartopy.crs as ccrs
import cartopy.feature as feature
#from descartes import PolygonPatch
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

from route import MEAS_AREA


class Map:
	ax = plt.axes(projection=ccrs.Mercator())
	#ax = plt.axes(projection=ccrs.epsg(3067))

	@classmethod
	def draw(cls, title=False, cbar=False, cbar_steps=100, cmap="coolwarm"):
		ax = cls.ax
		ax.add_feature(feature.NaturalEarthFeature("physical", "ocean", "10m"))
		ax.add_feature(feature.NaturalEarthFeature("physical", "lakes", "10m"))
		ax.add_feature(
			feature.NaturalEarthFeature(
				"cultural", "admin_0_boundary_lines_land", "10m", facecolor='none'),
			edgecolor='gray')

		# limit to Finnish sea area
		#ax.set_extent([1800100, 3400100, 7600100, 8800100], crs=ccrs.Mercator())
		# limit to reach area
		ax.set_extent([2180000, 3300000, 7900000, 8500000], crs=ccrs.Mercator())

		cls.draw_area(MEAS_AREA, 'green')

		if cbar:
			levels = np.linspace(0, cbar, cbar_steps)
			img = plt.contourf([[0, 0], [0, 0]], levels=levels, cmap=cmap)
			plt.colorbar(img, boundaries=[10, 20, 100, 200])

		if title:
			plt.title(title)
		plt.show()
		return plt

	@classmethod
	def plot_route(cls, x, y, color='red'):
		cls.ax.plot(x, y, color=color, linewidth=1, transform=ccrs.epsg(3067))

	@classmethod
	def draw_area(cls, area, color='red'):
		cls.ax.add_patch(
			patches.Rectangle(
				(area[0], area[2]), area[1] - area[0], area[3] - area[2],
				alpha=0.3, color=color, zorder=3, transform=ccrs.epsg(3067)))

	@classmethod
	def draw_circle(cls, x, y, radius, color):
		cls.ax.add_patch(patches.Circle(
			(x, y), radius,
			color=color, alpha=0.8, zorder=3, transform=ccrs.epsg(3067)))

	@classmethod
	def draw_concave_hull(cls, xy):
		#pts = [xy[vertice] for vertice in spatial.ConvexHull(xy).vertices]
		#pts = [xy[vertice] for vertice in alphashape.alphashape(xy, 2).vertices]

		# alpha-parameter can be removed to reoptimize alpha
		#pts = alphashape.optimizealpha(xy)
		pts = alphashape.alphashape(xy, 1.9846167135906253e-05)

		#pts = alphashape.alphashape(xy, 2)

		# add 10 km buffer zone for error
		cls.ax.add_patch(
			PolygonPatch(
				pts.buffer(10000),
				color='green', alpha=0.2, zorder=3, transform=ccrs.epsg(3067)))

