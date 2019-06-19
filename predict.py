import sys
from datetime import datetime

print (datetime.utcfromtimestamp(1))

boats = {}

with open("../ship-docs/AIS_2018-05_1.txt") as f:

	raw_line = True

	while raw_line:
		raw_line = f.readline()
		line = raw_line.strip().split(' ')

		locations = []

		for x in range(1, len(line), 3):
			locations.append(line[x:x+3])

		boats[line[0]] = locations

	#print(boats)

BOAT_KEY = boats.keys()[2]

print(BOAT_KEY)
#print(boats[boats.keys()[2]])

for x in boats[BOAT_KEY]:
	print (str(datetime.utcfromtimestamp(int(x[0])/1000)) +" // " +str(x[1:3]))