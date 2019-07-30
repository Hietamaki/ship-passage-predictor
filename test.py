import map
from node import Node
from ship import Ship
import node as nd
import pandas as pd
import matplotlib.patches as patches
import predict
import cartopy.crs as ccrs

print(Node.get_nodes_in_row())
nd.generate_nodes()
Node.load_all()
#nd.draw_reach_percentages()

#n = Node.get_node(2013)
#print(n.x)
#predict.predict_path(n)

#pl = Node.list[0]
m = map.Map.draw_map()
for n in Node.list:
	rp = n.reach_percentage()
	color = (rp, 0, 1 - rp)
	if rp == 0:
		color = (0, 1, 0)
	print(n.x, n.y)
	n.draw(color)
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
