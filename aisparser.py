from itertools import chain
from multiprocessing import Pool
import os
import sys

import numpy as np
from pyproj import Proj, Transformer

from database import save_list
from ship import Ship


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
				s = Ship(np.array([tx, ty, time], dtype=np.int32))
				ships.append(s)
	return ships


def convert_all_data(path, destination_file):

	files = []
	ships = []
	for r, d, f in os.walk(path):
		for file in f:
			if 'AIS_' in file and '.txt' in file:
				files.append(os.path.join(r, file))

	if sys.platform == 'linux':
		with Pool() as pool:
			ships = pool.map(load_data, files)
			pool.close()
			pool.join()
		ships = list(chain.from_iterable(ships))

		save_list(destination_file, ships, 'w')
	else:
		if (os.path.exists(destination_file)):
			os.remove(destination_file)
		print("Single threaded, performance is slow")
		for f in files:
			ships = load_data(f)

			save_list(destination_file, ships, 'a')

	print("Saving", len(ships), "ships to database.")
