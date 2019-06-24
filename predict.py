from map import Map
from datetime import datetime

import cartopy.crs as ccrs

def format_date(ts):
	return datetime.fromtimestamp(int(ts)/1000).strftime('%Y-%m-%d %H:%M:%S')

LIMIT_TO_DATE = datetime(2018, 5, 3).timestamp() * 1000

map = Map()
map.load_data("../ship-docs/AIS_2018-05_1.txt")#, LIMIT_TO_DATE)

# test case:

print("Amount of ship entries: ", len(map.list_ships()))

#SHIP_KEY = map.list_ships()[15]

#print(f"Details of ship (id: {SHIP_KEY})")

y = []
x = []

#for ship in map.list_ships()
#	y.append(i[1])
#	x.append(i[0])
#	print (format_date(i[2]) +" // " +str(i[0:2]))

ship = map.list_ships()[13]

plt = map.draw_map()
route = ship.get_route(0, LIMIT_TO_DATE)
print(route["x"])
map.plot_route(route["x"], route["y"])

plt.show()


#for x in map.transform(y):
#	pass
	#print("", x[0:2], format_date(x[2]))
