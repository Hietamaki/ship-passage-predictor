import constants as c
import database as db
from map import Map


nodes = db.load_list(c.NODES_FILENAME)

x1 = (79323, 6431055, 1530041717)
x2 = (348298, 6620462, 1530070027)

#print("Drawing reach percentages...")
#node.draw_reach_percentages(db.load_list(c.NODES_FILENAME), limit=0.95)

for n in nodes:
	rp = n.reach_acc
	color = (rp, 0, 1 - rp)
	if rp < 0.2:
		n.draw(color)

Map.draw()
