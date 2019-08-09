import map
import util
from node import Node
from ship import Ship
import node as nd
import pandas as pd
import matplotlib.patches as patches
import predict
import cartopy.crs as ccrs


#nd.generate_nodes(False)
Node.load_all()
noude = nd.get_closest_node(200846, 6558117)
noude.draw()
print(len(noude.passages))
#predict.test_case(noude)
xx = (58846, 61861, 64138)
yy = (6408117, 6411361, 6413779)
#predict.predict_path(xx, yy)

cn = nd.get_closest_node(58846, 6408117)

print(cn, cn.x, cn.y)
cn.draw('white')

#nd.draw_reach_percentages()

#n = Node.get_node(2013)
#print(n.x)
#predict.predict_path(n)

#pl = Node.list[0]
k = 0
m = map.Map.draw_map()
for n in Node.list:
	rp = n.reach_percentage()
	if rp > 0:
		color = (rp, 0, 1 - rp)
		if n.y < 6431000:
			print("Node:", n.x, n.y)
			for i in range(0, len(n.passages)):
				if not n.label[i]:
					continue
				if n.label[i] < (3600 * 8):
					pas = n.passages[i]
					pas.plot()
					passed = False
					print(map.route_in_area(pas.x, pas.y), "route_in_area")
					print("New Passage", pas.ship.id, len(pas.x), (n.label[i]//60/60), pas.reaches, util.format_date(pas.time[pas.reaches]))
					for i in range(1, len(pas.time)):
						start = (pas.x[i - 1], pas.y[i - 1], pas.time[i - 1])
						end = (pas.x[i], pas.y[i], pas.time[i])

						info_str = ""

						if map.is_in_area(end[0], end[1]):
							info_str = "<-- IN AREA"

						if not passed:
							if (end[0] > n.x and end[1] > n.y):
								passed = True
								info_str = "<-- Node is HERE"

						#if info_str:
						print(i, util.format_date(pas.time[i]), pas.x[i], pas.y[i], util.get_velocity(start, end), info_str)

						info_str = ""
		#color = (0, 1, 0)
			n.draw(color)
			k += 1
	#else:
	#	print("Nou")

print(k)
m.show()

#	if len(pl.passages) < len(n.passages):
#		pl = n

#print(pl.id, len(pl.passages))
#Ship.load_all()
#ship = Ship.list[13].passages[0]

#print(Node.list[0].label)
#print("Testing..", ship.x)
#print("Testing..", ship.reaches)

#predict.predict_path(ship.x, ship.y)
#predict.test_case(951)
