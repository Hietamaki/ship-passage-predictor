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
		print("Loaded nodes", len(cls.list))

	@classmethod
	def get_nodes_in_row(cls):
		area_boundaries = map.get_measurement_area()
		return (area_boundaries[1] // cls.SPACING_M)

	# @.output dictionary of nodes {id: [x, y]}

	@classmethod
	def get_nodes(cls):
		return {
			123: [1, 2],
			345: [3, 4]}

		#area = Map.get_measurement_area()

		#for i in len()
		# cl.SPACING_M

	def __init__(self, id):
		self.id = id
		self.passage_ids = []
		self.cog = []
		self.speed = []
		self.label = []

	def find_optimal_k(node):
		return 11

	def add_passage(self, passage, id, label):

		#if not self.list[self.id]:
		#	self.list[self.id] = []

		#calculate speed from
		#passage[0] passage[-1]
		#calculate cog from
		#print(passage)
		speed, course = util.get_velocity(passage[0], passage[-1])
		self.speed.append(speed)
		self.cog.append(course)
		self.passage_ids.append(id)
		self.label.append(label)
		self.x = passage[0][0]
		self.y = passage[0][1]
		#print(Node.list[id].passage_ids)

	#@classmethod
	#def initialize_all(cls):
#		cls.list = [Node(x) for x in range(0, 5000)]
#		print("Nodes initialized",len(Node.list))

	@classmethod
	def save_node_indices(cls, passage):

		node_ids = {}
		prev_id = get_node_id(passage.x[0], passage.y[0])

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
			if prev_id != node_id:

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

			cls.list[key].add_passage(node_ids[key], passage.id, passage.reaches)

	@classmethod
	def get_node(cls, id):
		for nod in cls.list:
			if nod.id == id:
				return nod

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
			Node.save_node_indices(passage)

	df = pd.Series(Node.list)
	df.to_hdf(NODES_FILE_NAME, 'df', mode='w')
	print("Saving", len(Node.list), "nodes to database.")


# return node_id based on coordinates
def get_node_id(x, y):

	area_boundaries = map.get_area_boundaries()
	max_x = Node.get_nodes_in_row()

	node_x = x // Node.SPACING_M
	node_y = (y - area_boundaries[2]) // Node.SPACING_M

	if (y < area_boundaries[2]):
		#print("Discarding node, y-coord out of bounds: ", passage.y[i])
		return -1

	node_id = node_x + (node_y * max_x)

	return node_id

def draw_reach_percentages():
	Node.load_all()
	m = map.Map.draw_map()

	for i in Node.list:
		if len(i.passage_ids) > 100:
			#print(i.id, len(i.passage_ids), int(i.reach_percentage() * 100) , "%")
			c = (i.reach_percentage(), 0, 1 - i.reach_percentage())
			print(c)
			map.Map.ax.add_patch(patches.Circle((i.x, i.y), 5000, alpha=0.75, color=c, zorder=3, transform=ccrs.epsg(3067)))
			i.reach_percentage()

	m.show()