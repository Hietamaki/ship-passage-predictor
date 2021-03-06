from map import Map
from database import load_list

import node as nd
import route
from util import get_closest

import pandas as pd
import predict
import numpy as np

from constants import NODES_FILENAME, TEST_NODES_FILENAME

nodes = load_list(NODES_FILENAME)

x1 = (79323, 6431055, 1530041717)
x2 = (348298, 6620462, 1530070027)

#print(util.get_velocity(x1, x2))

#print(len(noude.passages))
x1 = (230846, 6598117, 0)
x2 = (235846, 6642117, 100)
pas, exits = predict.predict_path(nodes, x1, x2)
print("Arrives in", exits, "h")

noude = get_closest(nodes, x1[0], x1[1])
#predict.test_case(noude)
noude.draw('green')
#print(noude.accuracy_score, noude.optimal_k)

for p in pas:
	px, py, pt = p.route_in_meas_area()

	if len(px) == 0:
		continue

	c = "orange"

	if px[0] > px[-1]:
		c = "purple"
	#map.Map.plot_route(px, py, c)
	p.plot(c)
	Map.draw_circle(px[0], py[0], 1000, c)
	print(pt[0] - pt[-1])

p = route.calculate_mean_route(pas)
Map.plot_route(p[0], p[1], "red")

#print("Node average arrival time: ",noude.predict_arrival_time() / 60 / 60, "h")

scores = nd.draw_reach_percentages(nodes, limit=0.01)

#print("avg:", np.mean(scores), np.median(scores), np.std(scores))
#pl = Node.list[0]
#k = 0
Map.draw()
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
