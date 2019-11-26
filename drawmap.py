from matplotlib import cm

import constants as c
import database as db
from map import Map


def ToNearest(n, to_nearest):
	x = (n + (to_nearest / 2)) % to_nearest
	return n + 0.1 - x

nodes = db.load_list(c.NODES_FILENAME)

x1 = (79323, 6431055, 1530041717)
x2 = (348298, 6620462, 1530070027)

#print("Drawing reach percentages...")
#node.draw_reach_percentages(db.load_list(c.NODES_FILENAME), limit=0.95)

colormap = "RdYlGn"
cmap = cm.get_cmap(colormap)

for n in nodes:

	# To nearest 0.2
	rp = ToNearest(n.reach_acc, 0.2)

	#if rp > 1:
	#print(n.reach_acc,"-", x, "=", rp)
	if n.reach_acc < 1:
		n.draw(cmap(rp + 0.1))

Map.draw("Epävarmuustarkastelu", 1, 6, cmap=colormap)
