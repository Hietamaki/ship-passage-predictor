import map
import util
from node import Node
from ship import Ship
import node as nd
import pandas as pd
import matplotlib.patches as patches
import predict
import cartopy.crs as ccrs


#nd.generate_nodes()
Node.load_all()
cn = nd.get_closest_node(320000,6620000)

print(cn, cn.x, cn.y)
cn.draw('white')

#nd.draw_reach_percentages()

#n = Node.get_node(2013)
#print(n.x)
#predict.predict_path(n)

#pl = Node.list[0]
k=0
m = map.Map.draw_map()
for n in Node.list:
	rp = n.reach_percentage()
	if rp > 0:
		color = (rp, 0, 1 - rp)
		if n.y < 6350000:
			print("Node:",n.x, n.y)
			for i in range(0, len(n.passages)):
				if n.label[i]:
					pas = n.passages[i]
					pas.plot()
					print(pas.ship.id, len(pas.x))
					for i in range(0, len(pas.time)):
						print(util.format_date(pas.time[i]), pas.x[i], pas.y[i])
		#color = (0, 1, 0)
			n.draw(color)
			print(n.x, n.y, rp, n.id, n.speed[i])
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
