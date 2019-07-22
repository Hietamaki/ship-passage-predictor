from itertools import chain
from multiprocessing import Pool
import os
import sys

import pandas as pd
from pyproj import Proj, Transformer

import node
from ship import Ship

AIS_DATA_PATH = "../ship-docs/"
SHIPS_FILE_NAME = 'ships.h5'
NODES_FILE_NAME = 'nodes.h5'


def get_transformer(source_epsg=4326, epsg=3067):

	# projections from WSG 84 to TM35FIN(E,N)
	return Transformer.from_proj(
		Proj(init=f"epsg:{source_epsg}"),
		Proj(init=f"epsg:{epsg}"))

# pre-processing data
#
# @.input
#	filename of file that holds AIS data
#	epsg	coordiantes system to be used
#
# @.output	dictionary
#		{ ship_id: [
#			[unixtime, lat, lon], [unixtime, lat, lon], ...] }


def load_data(filename, epsg=3067, limit_to_date=253385798400000):

	# data is in form:
	# shipid (unixtime lat lon) (unixtime lat lon) (unixtime lat lon) ... \n

	ships = []
	print("Loading file", filename)
	transformer = get_transformer()

	with open(filename) as file:

		for raw_line in file.readlines():

			line = raw_line.strip().split(' ')
			ship_id = line[0]

			#locations = []
			x = []
			y = []
			time = []

			for i in range(1, len(line), 3):

				# ms to s
				unixtime = int(line[i]) // 1000

				if unixtime > limit_to_date:
					break

				x.append(float(line[i + 1]))
				y.append(float(line[i + 2]))
				time.append(unixtime)

			if x:
				tx, ty = transformer.transform(x, y)
				tx = [int(x) for x in tx]
				ty = [int(y) for y in ty]
				s = Ship(ship_id, tx, ty, time)
				ships.append(s)

	return ships


def convert_all_data():

	if (os.path.exists(SHIPS_FILE_NAME)):
		os.remove(SHIPS_FILE_NAME)

	files = []
	ships = []
	for r, d, f in os.walk(AIS_DATA_PATH):
		for file in f:
			if 'AIS_' in file and '.txt' in file:
				files.append(os.path.join(r, file))

	if sys.platform == 'linux':
		with Pool() as pool:
			ships = pool.map(load_data, files)
			pool.close()
			pool.join()
		ships = list(chain.from_iterable(ships))

		df = pd.Series(ships)
		df.to_hdf(SHIPS_FILE_NAME, 'df', mode='w')
	else:
		print("Single threaded, performance is slow")
		for f in files:
			ships = load_data(f)

			df = pd.Series(ships)
			df.to_hdf(SHIPS_FILE_NAME, 'df', mode='a')

	print("Saving", len(ships), "ships to database.")

	df = pd.Series(node.Node.list)
	df.to_hdf(NODES_FILE_NAME, 'df', mode='w')


convert_all_data()
#load_data(AIS_DATA_PATH + "AIS_2018-05_1.txt")
