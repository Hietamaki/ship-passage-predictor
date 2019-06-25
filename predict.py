from map import Map
from datetime import datetime

import cartopy.crs as ccrs

def format_date(ts):
	return datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')

LIMIT_TO_DATE = datetime(2018, 5, 8).timestamp()

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

ships = map.list_ships()
plt = map.draw_map()

#ship = ships[13]
#route = ship.get_route(datetime(2018, 5, 8).timestamp(), datetime(2018, 6, 8).timestamp())

#map.plot_route(route["x"], route["y"])

#print(route)

count1 = 0
count2 = 0
for ship in ships:
	route = ship.get_route(datetime(2018, 5, 2, 8).timestamp(), datetime(2018, 5, 2, 8, 30).timestamp())
	if len(route['x']) > 0:
		count1+=1
	if ship.in_area(route, map.get_measurement_area()):
		map.plot_route(ship.x, ship.y)
		count2+=1

print(f"Laivoja kaikkiaan {len(ships)}, klo 8:00-8:30 {count1}, mittausalueella {count2}")
plt.show()


#for x in map.transform(y):
#	pass
	#print("", x[0:2], format_date(x[2]))
