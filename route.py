# helper functions to handle routes
# uses np.array(x, y, time)

import numpy as np

from constants import MEAS_AREA


# interpolates entered route to minute intervals
def get_minute_interpolation():
	'''
	rx, ry, rt = passage.route_in_meas_area()

	# interpolation to 1 min spacing
	nt = np.arange(rt[0], rt[-1], 60)
	nx = np.interp(nt, rt, rx).astype(np.int32)
	ny = np.interp(nt, rt, ry).astype(np.int32)

	routes.append((nx, ny, nt))
	'''
	return


# return enters_i and end_i when in area or False if doesn't cross area
def route_in_area(x, y):

	enters_i = False

	if len(x) == 0:
		return False

	for i in range(0, len(x) - 1):
		if (x[i] > MEAS_AREA[0] and x[i] < MEAS_AREA[1] and
			y[i] > MEAS_AREA[2] and y[i] < MEAS_AREA[3]):

			if enters_i is False:
				enters_i = i

		elif enters_i:
			return enters_i, i

	if enters_i is not False:
		return enters_i, len(x) - 1
	else:
		return False


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
