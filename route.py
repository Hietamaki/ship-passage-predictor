# helper functions to handle routes
# uses np.array(x, y, time)

import numpy as np

from constants import MEAS_AREA


def route_in_area(xy):
	''' returns
			(start index, end index)
				when in area
			False
				if doesn't cross area
	'''

	b = ((xy[0] > MEAS_AREA[0]) & (xy[0] < MEAS_AREA[1]) &
		 (xy[1] > MEAS_AREA[2]) & (xy[1] < MEAS_AREA[3]))
	
	nz = np.nonzero(b)[0]

	if nz.shape[0] == 0:
		return False

	# Sometimes exits meas area temporarily. This examination shows
	# it's not a huge issue.

	#if not np.array_equal(np.arange(nz[0], nz[-1] + 1), nz):
	#	map.Map.plot_route(xy[0].tolist(), xy[1].tolist(), random_color())
	#	print(np.arange(nz[0], nz[-1] + 1), nz)


	return (nz[0], nz[-1])


def is_in_area(x, y):
	return (
		x > MEAS_AREA[0] and x < MEAS_AREA[1] and
		y > MEAS_AREA[2] and y < MEAS_AREA[3])


def calculate_mean_route(passages):

	routes = []
	max_size = 0

	for passage in passages:

		if passage.reaches is False:
			continue

		# get part of routes in area
		routes.append(passage.route_in_meas_area())
		
		rx_len = len(routes[-1][0])

		if max_size < rx_len:
			max_size = rx_len

	# interpolate arrays to same size
	x_coords = np.arange(0, max_size+1)

	standardized_routes = []

	for r in routes:
		#print(max_size, np.linspace(0, max_size, len(r[0])))
		standardized_routes.append((
			np.interp(x_coords, np.linspace(0, max_size, len(r[0])), r[0]).astype(np.int32),
			np.interp(x_coords, np.linspace(0, max_size, len(r[1])), r[1]).astype(np.int32),
			np.interp(x_coords, np.linspace(0, max_size, len(r[2])), r[2]).astype(np.int32)))
		#print(r[0], "vs")
		#print(standardized_routes[-1][0])

	# calculate mean
	route = np.array(standardized_routes)

	return np.mean(route, axis=0)
