from ships import Ships
from datetime import datetime

def format_date(ts):
	return datetime.fromtimestamp(int(ts)/1000).strftime('%Y-%m-%d %H:%M:%S')

LIMIT_TO_DATE = datetime(2018, 5, 2).timestamp() * 1000

ships = Ships()
ships.load_data("../ship-docs/AIS_2018-05_1.txt", LIMIT_TO_DATE)

# test case:

print("Amount of ship entries: ", len(ships.list_ships()))

SHIP_KEY = ships.list_ships()[2]

print("Listing ship with id: ", SHIP_KEY)
y = []
for x in ships.data[SHIP_KEY]:
	y.append(x)
#	print (format_date(x[0]) +" // " +str(x[1:3]))


for x in ships.transform(y):
	print("", x[0:2], format_date(x[2]))

ships.draw_map()