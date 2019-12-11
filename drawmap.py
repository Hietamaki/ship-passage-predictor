from matplotlib import cm
import numpy as np

import constants as c
import database as db
from map import Map

t = 3


def reach_acc(x): return x.reach_acc < 1

attrib = "reach_acc"
label = "Epävarmuustarkastelu"
check = reach_acc
scale = 1

def reach_k(x): return x.reach_k > 0

if t == 2:
	attrib = "reach_k"
	label = "Optimoitu K"
	check = reach_k
	scale = c.MAX_K

if t == 3:
	attrib = "alpha"
	label = "Optimoitu painotuskerroin (suunta=1, nopeus=0)"
	scale = 1

def ToNearest(n, to_nearest):
	x = (n + (to_nearest / 2)) % to_nearest
	return np.around(n + 0.1 - x, 2)

nodes = db.load_list(c.NODES_FILENAME)

x1 = (79323, 6431055, 1530041717)
x2 = (348298, 6620462, 1530070027)

#print("Drawing reach percentages...")
#node.draw_reach_percentages(db.load_list(c.NODES_FILENAME), limit=0.95)

colormap = "RdYlGn"
cmap = cm.get_cmap(colormap)
values = []

for n in nodes:

	attrib_value = getattr(n, attrib)

	# To nearest 0.2
	rp = ToNearest(attrib_value / scale, 0.2)

	# (0.8, 1) same color
	if rp == 1:
		rp -= 0.2

	if getattr(n, attrib) > -1:
		values.append(attrib_value)
		print(attrib_value)
		n.draw(cmap(rp + 0.1))

print(values)
print(np.mean(values))
Map.draw(label, scale, 6, cmap=colormap)
