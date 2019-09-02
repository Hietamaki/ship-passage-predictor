import map
import util
from node import Node
from ship import Ship
import node as nd

import pandas as pd
import predict
import numpy as np

x1 = (79323, 6431055, 1530041717)
x2 = (348298, 6620462, 1530070027)

#print(util.get_velocity(x1, x2))
Node.load_all()
#print(len(noude.passages))
x1 = (210846, 6598117, 0)
x2 = (215846, 6642117, 100)
pas = predict.predict_path(x1, x2)

noude = nd.get_closest_node(x1[0], x1[1])
predict.test_case(noude)
noude.draw('green')
print(noude.accuracy_score, noude.optimal_k)

for p in pas:
	px, py, pt = p.route_in_meas_area()

	if len(px) == 0:
		continue

	c = "orange"

	if px[0] > px[-1]:
		c = "purple"
	#map.Map.plot_route(px, py, c)
	p.plot(c)

p = predict.calculate_mean_route(pas)

px = p[0]
py = p[1]
ptime = p[2]

print("Passage:")
print(px, py, ptime)
#print(ptime, px)
#interped = np.arange(ptime[0], ptime[-1], 60)
#x3 = np.interp(interped, ptime, px).astype(np.int32)
#y3 = np.interp(interped, ptime, py).astype(np.int32)
#print(len(x3), len(px))
#print(x3, len(px))

map.Map.plot_route(px, py, "pink")
#for t in p.time:
#	print((x2 - t) / 60)
#	x2 = t

#p.plot()

#m = map.Map.draw_map()
#m.show()
#pas.reaches_measurement_area()

#cn = nd.get_closest_node(58846, 6408117)

#print(cn, cn.x, cn.y)
#cn.draw('white')

#nd.draw_reach_percentages()

#n = Node.get_node(2013)
#print(n.x)
#predict.predict_path(n)

#scores = nd.draw_reach_percentages(limit=0.01)

#print("avg:", np.mean(scores), np.median(scores), np.std(scores))
#pl = Node.list[0]
#k = 0
m = map.Map.draw_map()
m.show()
'''
for n in Node.list:
	rp = n.reach_percentage()
	if rp > 0.0:

#		color = (rp, 0, 1 - rp)
#		n.draw(color)
#		k += 1

		#if map.is_in_area(n.x, n.y):# < 9996431000:
		#print("Node:", n.x, n.y, len(n.passages), rp)

		#for i in range(0, len(n.passages)):
		#	if n.passages[i].reaches is False:

		#		n.passages[i].plot(util.random_color())
		#		print(map.route_in_area(n.passages[i].x, n.passages[i].y))

			#if n.label[i] > 0:
			#	continue
			#if n.label[i] < (3600 * 8):
				print(n.label[i])
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
					#print(i, pas.time[i], util.format_date(pas.time[i]), pas.x[i], pas.y[i], util.get_velocity(start, end), info_str)

					info_str = ""
					'''

#print(k)
#m.show()

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
