#%matplotlib inline
from datetime import datetime

from map import Map
import util
#%pylab inline
#LIMIT_TO_DATE = datetime(2018, 5, 8).timestamp()

map = Map()
map.load_ships()

# test case:

ships = map.list_ships()

#for i in ships[0].time:
#	print (util.format_date(i))

#route = ships[13].get_route(datetime(2018, 5, 8).timestamp(), datetime(2018, 6, 8).timestamp())
#map.plot_route(route["x"], route["y"])
#print(route)

#ships[13].create_passages()
plt = map.draw_map()

#for p in ships[2].passages:
#	map.plot_route(p['x'], p['y'], util.random_color())
#for passage in range(0, len(ships[13].passages)):

#	map.plot_route(ship.x[passage, ])

	#passage


count1 = 0
count2 = 0
for ship in ships:
	route = ship.get_route(datetime(2018, 5, 2, 8).timestamp(), datetime(2018, 5, 2, 16, 0).timestamp())
	if len(route['x']) > 0:
		count1+=1

	col = util.random_color()
	
	if map.route_in_area(route, map.get_measurement_area()):
		for p in ship.passages:
			map.plot_route(p['x'], p['y'], col)
		#map.plot_route(ship.x, ship.y, util.random_color())
		count2+=1
print(f"Laivoja kaikkiaan {len(ships)}, klo 8:00-8:30 {count1}, mittausalueella {count2}")


plt.show()

