#%matplotlib inline
from datetime import datetime, timedelta

from map import Map
import util
#%pylab inline
#LIMIT_TO_DATE = datetime(2018, 5, 8).timestamp()

map = Map()
map.load_ships()

# test case:

ships = map.list_ships()

for p in ships[0].passages:
	print(len(p.x))
	p.interpolate()
'''
for i in ships[0].time:
	print (util.format_date(i))

route = ships[13].get_route(datetime(2018, 5, 8).timestamp(), datetime(2018, 6, 8).timestamp())
map.plot_route(route["x"], route["y"])
print(route)

ships[13].create_passages()
'''
'''
for p in ships[2].passages:
	map.plot_route(p['x'], p['y'], util.random_color())
for passage in range(0, len(ships[13].passages)):

	map.plot_route(ship.x[passage, ])

	passage
'''
#from_whence = datetime(2018, 5, 2, 0).timestamp()
'''
for ship in ships:
	r = ship.get_route(from_whence)

	if len(r['x']) > 0:
		starting_points.append([r['x'][0], r['y'][0]])
'''
#plt = map.draw_map()

#map.draw_reach_area("2018-05-01", "2018-05-20")

#plt.show()
