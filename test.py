from node import Node
from ship import Ship
import node as nd
import pandas as pd

import predict

#nd.generate_nodes()
Node.load_all()
#pl = Node.list[0]

#for n in Node.list:
#	if len(pl.passages) < len(n.passages):
#		pl = n

#print(pl.id, len(pl.passages))
#Ship.load_all()
#ship = Ship.list[13].passages[0]

#print(Node.list[0].label)
#print("Testing..", ship.x)
#print("Testing..", ship.reaches)

#predict.predict_path(ship.x, ship.y)
predict.test_case()
