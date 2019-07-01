import os

import pandas as pd
from pyproj import Proj, Transformer

from ship import Ship

AIS_DATA_PATH = "../ship-docs/"


def get_transformer(source_epsg=4326, epsg=3067):

	# projections from WSG 84 to TM35FIN(E,N)
	return Transformer.from_proj(Proj(init=f"epsg:{source_epsg}"), Proj(init=f"epsg:{epsg}"))

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

	#df = pd.Series()
	ships = []

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

				#locations.append([float(line[x+1]), float(line[x+2]), unixtime])
				x.append(float(line[i + 1]))
				y.append(float(line[i + 2]))
				time.append(unixtime)

			if x:
				tx, ty = transformer.transform(x, y)
				s = Ship(ship_id, tx, ty, time)
				ships.append(s)

				s.create_passages()

	df = pd.Series(ships)
	df.to_hdf('ships.h5', 'df')


def convert_all_data():
	for r, d, f in os.walk(AIS_DATA_PATH):
		for file in f:
			if '.txt' in file:
				load_data(os.path.join(r, file))


load_data(AIS_DATA_PATH + "AIS_2018-05_1.txt")
