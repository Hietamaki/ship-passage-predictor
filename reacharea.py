from datetime import timedelta
import itertools
from multiprocessing import Pool
import sys

import pandas as pd

import route
import ship as sh

def draw_reach_area(start_date, end_date):
	dates = [r for r in pd.date_range(start_date, end_date)]

	# parallel processing for unix
	if sys.platform == 'linux':
		with Pool() as pool:
			points = pool.map(points_reaching_measurement_area, dates)
			pool.close()
			pool.join()
	else:
		points = [points_reaching_measurement_area(r) for r in dates]

		Map.draw_concave_hull(list(itertools.chain.from_iterable(points)))


def points_reaching_measurement_area(date):
	starting_points = []
	count1 = 0
	count2 = 0

	for ship in sh.Ship.list:
		route = ship.get_route(
			date.timestamp(),
			(date + timedelta(days=1)).timestamp())

		if len(route['x']) > 0:
			count1 += 1

		#col = util.random_color()

		if route.route_in_area(route['x'], route['y']) is not False:
			starting_points.append([route['x'][0], route['y'][0]])
			starting_points.append([route['x'][-1], route['y'][-1]])
			count2 += 1

	#print(
	#	f'Laivoja kaikkiaan {len(map.list)}, {date}. päivänä {count1}, '
	#	f'mittausalueelle ehtii {count2}')

	return starting_points
