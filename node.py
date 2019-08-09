import numpy as np
import pandas as pd
import matplotlib.patches as patches
import cartopy.crs as ccrs
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

import map
import ship
import util

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
				node_ids[node_id].append(
					(passage.x[i + 1], passage.y[i + 1], passage.time[i + 1]))

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

	def find_optimal_k(self, scale=True):
		max_k = 25
		# k ei voi olla isompi kuin samplen koko. k-fold 5:llä k = sampleja * 4/5
		if 35 > len(self.passages):
			max_k = len(self.passages) // 5 * 4
			#print("Set Max K to", max_k)
		#print(len(self.passages))
		param_grid = {'n_neighbors': np.arange(1, max_k)}
		knn_gscv = GridSearchCV(KNeighborsClassifier(), param_grid, cv=5)

		features = self.get_features()

		if scale:
			scaler = StandardScaler()
			scaler.fit(features)
			features = scaler.transform(features)

		knn_gscv.fit(features, self.get_labels())
		#print("Setting to", knn_gscv.best_params_, knn_gscv.best_score_)
		return knn_gscv.best_params_['n_neighbors']

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
			# todo discard if already exited measure area
			if time_to_measurement < -1:
				self.label.append(False)
			else:
				self.label.append(time_to_measurement < (3600 * 8))

	def draw(self, color='red'):
		map.Map.ax.add_patch(patches.Circle(
			(self.x, self.y), self.SPACING_M // 2,
			color=color, alpha=0.8, zorder=3, transform=ccrs.epsg(3067)))

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


# Generate nodes and find optimal k value for each
def generate_nodes(optimize_k=True):

	ship.Ship.load_all()
	for shp in ship.Ship.list:
		for passage in shp.passages:
			Node.add_info_from_passage(passage)

	# Remove if node has fewer than x samples
	removed_nodes = []
	for key, val in Node.list.items():
		if len(val.passages) < 10:
			#print("Del", key, len(val.passages))
			removed_nodes.append(key)

	for key in removed_nodes:
		del Node.list[key]

	# Optimize K
	if optimize_k:
		for n in Node.list.values():
			n.optimal_k = n.find_optimal_k(True)
			#print("Scaling before & after:", n.find_optimal_k(False), n.optimal_k)

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
					print(i.id, len(i.passages), (i.reach_percentage() * 100), "%")
					i.draw(c)
					c = 'green'

	m.show()


def get_closest_node(x, y):

	closest_dist = 9999999999999999
	closest_node = -1

	for node in Node.list:
		if closest_dist > util.distance((x, y), (node.x, node.y)):
			closest_dist = util.distance((x, y), (node.x, node.y))
			closest_node = node

	return closest_node
