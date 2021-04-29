from datetime import timedelta
import itertools
from multiprocessing import Pool
import sys

import pandas as pd

import route
import ship as sh
import constants as c
import database as db
import numpy as np
import pandas as pd

from route import route_in_area
from map import Map
from alphashape import alphashape
from descartes import PolygonPatch

#nodes = db.load_list(c.NODES_FILENAME)
ships = db.load_list(c.SHIPS_FILENAME)

def draw_reach_area(start_date, end_date):
	dates = [r for r in pd.date_range(start_date, end_date)]

	# parallel processing for unix
	if sys.platform == 'linux':
		print(sys.platform)
		with Pool() as pool:
			points = pool.map(points_reaching_measurement_area, dates)
			pool.close()
			pool.join()
	else:
		points = [points_reaching_measurement_area(r) for r in dates]

	Map.draw_concave_hull(list(itertools.chain.from_iterable(points)))


def points_reaching_measurement_area(date):
	print(date)
	starting_points = []
	count1 = 0
	count2 = 0

	for ship in ships:
		route = ship.get_route(
			date.timestamp(),
			(date + timedelta(days=1)).timestamp())

		if len(route[0]) > 0:
			count1 += 1
			#print(route)

		#col = util.random_color()

		if route_in_area(route[0], route[1]) is not False:
			starting_points.append([route[0][0], route[1][0]])
			starting_points.append([route[0][-1], route[1][-1]])
			count2 += 1

	#print(
	#	f'Laivoja kaikkiaan {len(map.list)}, {date}. päivänä {count1}, '
	#	f'mittausalueelle ehtii {count2}')
	#print(starting_points)
	return starting_points

