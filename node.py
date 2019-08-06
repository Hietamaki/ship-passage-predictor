import numpy as np
import pandas as pd

import map
import ship
import util
import matplotlib.patches as patches
import cartopy.crs as ccrs

NODES_FILE_NAME = 'nodes.h5'


class Node:
	SPACING_M = 10000

	list = {}

	@classmethod
	def load_all(cls):

		cls.list = pd.read_hdf('nodes.h5', 'df').values
		print("Loaded", len(cls.list), "nodes")

	@classmethod
	def get_nodes_in_row(cls):
		area_boundaries = map.get_area_boundaries()
		return (area_boundaries[1] // cls.SPACING_M)

	@classmethod
	def add_info_from_passage(cls, passage):

		node_ids = {}
		prev_id = get_node_id(passage.x[0], passage.y[0])

		# go through every xy coordinate in passage
		for i in range(0, len(passage.x) - 1):
			node_id = get_node_id(passage.x[i], passage.y[i])

			if (node_id < 0):
				#print("Discarding node, node_id out of bounds: ", node_id)
				continue

			#print(node_x, node_y, node_id)
			if node_id not in node_ids:
				node_ids[node_id] = []

			node_ids[node_id].append((passage.x[i], passage.y[i], passage.time[i]))

			# in case there is only datapoint in previous node, add the next one
			if prev_id != node_id and prev_id != -1:

				if prev_id not in node_ids:
					print("Prev id missing", prev_id, node_id)
					node_ids[prev_id] = []

				#print("prev_id != node_id")
				node_ids[prev_id].append((passage.x[i], passage.y[i], passage.time[i]))

			if i == len(passage.x) - 2:
				#print("yolo")
				node_ids[node_id].append((passage.x[i+1], passage.y[i+1], passage.time[i+1]))

			prev_id = node_id

		for key in node_ids:
			if key not in cls.list:
				cls.list[key] = Node(key)

			cls.list[key].add_passage(node_ids[key], passage)

	@classmethod
	def get_node(cls, id):
		for nod in cls.list:
			if nod.id == id:
				return nod

	def __init__(self, id):
		self.id = id
		self.passages = []
		self.cog = []
		self.speed = []
		self.label = []

		max_x = Node.get_nodes_in_row()

		self.x = id % max_x * Node.SPACING_M
		self.y = (id // max_x) * Node.SPACING_M + 6100000

	def find_optimal_k(node):
		return 11

	def add_passage(self, route, passage):

		#if not self.list[self.passage]:
		#	self.list[self.passage] = []

		#calculate speed from
		#route[0] route[-1]
		#calculate cog from
		#print(route)
		speed, course = util.get_velocity(route[0], route[-1])
		self.speed.append(speed)
		self.cog.append(course)
		self.passages.append(passage)

		if passage.reaches is False:
			self.label.append(False)
		else:
			time_to_measurement = passage.time[passage.reaches] - route[0][2]
			#print(abs(time_to_measurement) < (3600 * 8))
			# todo discard if already exited msrarae
			self.label.append(abs(time_to_measurement) < (3600 * 8))

	def draw(self, color='red'):
		map.Map.ax.add_patch(patches.Circle(
			(self.x, self.y), 5000, color=color, alpha=0.8, zorder=3, transform=ccrs.epsg(3067)))

	# convert to ndarray
	def get_labels(self):
		return np.array(self.label)

	def get_features(self):
		features = np.array((self.cog, self.speed))
		features = np.reshape(features, (-1, 2))

		return features

	def get_passage_indices(self):
		return np.array(self.indices)

	def reach_percentage(self):
		
		k = 0
		for i in self.label:
			if i:
				k += 1

		return k / len(self.label)


def generate_nodes():

	ship.Ship.load_all()
	for shp in ship.Ship.list:
		for passage in shp.passages:
			Node.add_info_from_passage(passage)

	print("Saving", len(Node.list), "nodes to local disk...")
	df = pd.Series(Node.list)
	df.to_hdf(NODES_FILE_NAME, 'df', mode='w')


# return node_id based on coordinates
def get_node_id(x, y):

	area_boundaries = map.get_area_boundaries()
	max_x = Node.get_nodes_in_row()

	if x < 0:
		return -1
	
	if y < area_boundaries[2]:
		#print("Discarding node, y-coord out of bounds: ", passage.y[i])
		return -1

	node_x = x // Node.SPACING_M
	node_y = (y - area_boundaries[2]) // Node.SPACING_M


	node_id = node_x + (node_y * max_x)

	return node_id

def draw_reach_percentages():
	Node.load_all()
	m = map.Map.draw_map()
	for i in Node.list:
		if len(i.passages) > 100 and i.reach_percentage() > 0:
			c = (i.reach_percentage(), 0, 1 - i.reach_percentage())
			for x in range(0, len(i.passages)):
				psg = i.passages[x]
				if psg.x[0] > 430000 and psg.y[0] > 6750000:
					print(i.x, i.y, i.id)
					print(psg.x[0], psg.y[0])
					if i.label[x]:
						print("Juu", i.label[x])
					psg.plot()
					print(i.id, len(i.passages), (i.reach_percentage() * 100) , "%")
					i.draw(c)
					c = 'green'

	m.show()
