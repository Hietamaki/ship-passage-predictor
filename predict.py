#%matplotlib inline
from datetime import datetime
import itertools
from multiprocessing import Pool

from map import Map
import util
#%pylab inline
#LIMIT_TO_DATE = datetime(2018, 5, 8).timestamp()

map = Map()
map.load_ships()

# test case:

ships = map.list_ships()
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
plt = map.draw_map()

def draw_reach_area(day):
	starting_points = []
	count1 = 0
	count2 = 0
	for ship in ships:
		route = ship.get_route(
			datetime(2018, 5, 2 + day, 0).timestamp(),
			datetime(2018, 5, 3 + day, 0).timestamp())

		if len(route['x']) > 0:
			count1 += 1

		col = util.random_color()

		if map.route_in_area(route, map.get_measurement_area()):
			starting_points.append([route['x'][0], route['y'][0]])
			starting_points.append([route['x'][-1], route['y'][-1]])
			#map.plot_route(route['x'], route['y'], col)
			#for p in ship.passages:
			#	map.plot_route(p['x'], p['y'], col)
			#map.plot_route(ship.x, ship.y, util.random_color())
			count2 += 1

	
	print(f"Laivoja kaikkiaan {len(ships)}, {day}. päivänä {count1}, mittausalueelle ehtii {count2}")

	return starting_points

pool = Pool()
points = pool.map(draw_reach_area, [r for r in range(0, 29)])
#points = ([draw_reach_area(r) for r in range(0, 29)])

pool.close()
pool.join()
#points = draw_reach_area(range(0, 5))
#points += draw_reach_area(range(5, 10))
#points += draw_reach_area(range(10, 15))
#points += draw_reach_area(range(15, 20))

map.draw_concave_hull(list(itertools.chain.from_iterable(points)))
plt.show()
