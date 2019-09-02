# Node
#

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

from route import AREA_BOUNDARIES
from map import Map
import ship
import util

NODES_FILE_NAME = 'nodes.h5'


class Node:
	SPACING_M = 10000

	list = {}

	@classmethod
	def load_all(cls):

		# this could be abstracted
		cls.list = pd.read_hdf('nodes.h5', 'df').values
		print("Loaded", len(cls.list), "nodes")

	@classmethod
	def get_nodes_in_row(cls):
		return (AREA_BOUNDARIES[1] // cls.SPACING_M)

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
		self.exits_node = []

		max_x = Node.get_nodes_in_row()

		self.x = id % max_x * Node.SPACING_M + (Node.SPACING_M / 2)
		self.y = (id // max_x) * Node.SPACING_M + 6100000 + (Node.SPACING_M / 2)

	# add passage to node and calculate speed and course inside node
	# @.in
	#	self
	#	passage
	#	part of passage (timecoords) that is in node
	#		[(x, y, t), (x, y, t)]
	def add_passage(self, passage, route):

		enter_point = route[0]
		exit_point = route[-1]

		if passage.reaches is False:
			self.label.append(False)
		else:
			time_to_measurement = passage.time[passage.reaches[0]] - enter_point[2]

			# is passage going to measurement area or coming from measurement area?
			if time_to_measurement < 0:
				# false if already exited measurement area
				self.label.append(False)
				#self.label.append(enter_point[2] < passage.time[passage.reaches[1]])
			else:
				# false if over 8 hours to measurement area
				self.label.append(time_to_measurement < (3600 * 8))

		speed, course = util.get_velocity(enter_point, exit_point)
		self.exits_node.append(exit_point[2]) # change to more exact later
		self.speed.append(speed)
		self.cog.append(course)
		self.passages.append(passage)

	def draw(self, color='red'):
		Map.draw_circle(self.x, self.y, self.SPACING_M // 2, color)

	# convert to ndarray
	def get_labels(self):
		return np.array(self.label)

	def get_features(self):

		# break course to x, y components
		features = np.array((np.sin(self.cog), np.cos(self.cog), self.speed))
		features = np.reshape(features, (-1, 3))

		return features

	def get_exit_times(self):

		times = []

		for i in range(0, len(self.label)):
			if self.label[i] is not False:
				times.append(self.exits_node[i])

		return times

	def get_passages_reaching_meas_area(self):

		passages = []

		for i in range(0, len(self.label)):
			if self.label[i] is not False:
				passages.append(self.passages[i])

		return passages

	def get_features_reaching_meas_area(self):

		cogs = []
		speeds = []

		for i in range(0, len(self.label)):
			if self.label[i] is not False:
				speeds.append(self.speed[i])
				cogs.append(self.cog[i])

		routes = np.array((np.sin(cogs), np.cos(cogs), speeds))
		routes = np.reshape(routes, (-1, 3))

		return routes

	def reach_percentage(self):
		k = 0
		for i in self.label:
			if i:
				k += 1

		return k / len(self.label)

	def find_optimal_k(self, scale=True):
		max_k = 25
		# k ei voi olla isompi kuin samplen koko. k-fold 5:llä k = sampleja * 4/5
		if 35 > len(self.passages):
			max_k = len(self.passages) // 5 * 4
			#print("Set Max K to", max_k)
		#print(len(self.passages))
		param_grid = {'n_neighbors': np.arange(1, max_k)}
		knn_gscv = GridSearchCV(
			KNeighborsClassifier(), param_grid,
			cv=5, n_jobs=-1)

		features = self.get_features()

		if scale:
			scaler = StandardScaler()
			scaler.fit(features)
			features = scaler.transform(features)

		knn_gscv.fit(features, self.get_labels())
		#print("Setting to", knn_gscv.best_params_, knn_gscv.best_score_)
		return knn_gscv.best_params_['n_neighbors'], knn_gscv.best_score_


# Generate nodes and find optimal k value for each
def generate_nodes(optimize_k=True):

	ship.Ship.load_all()
	for shp in ship.Ship.list:
		for passage in shp.passages:
			extract_passage_to_nodes(passage)

	# Remove if node has fewer than x samples
	removed_nodes = []
	for key, val in Node.list.items():
		if len(val.passages) < 20:
			#print("Del", key, len(val.passages))
			removed_nodes.append(key)

	for key in removed_nodes:
		del Node.list[key]

	# Optimize K
	if optimize_k:
		for n in Node.list.values():
			n.optimal_k, n.accuracy_score = n.find_optimal_k()
			#print("Scaling before & after:", n.find_optimal_k(False), n.optimal_k)

	print("Saving", len(Node.list), "nodes to local disk...")
	df = pd.Series(Node.list)
	df.to_hdf(NODES_FILE_NAME, 'df', mode='w')


def extract_passage_to_nodes(passage):

	nodes = {}
	prev_id = get_node_id(passage.x[0], passage.y[0])

	# associate every xy coordinate in passage to correct node
	for i in range(0, len(passage.x) - 1):
		node_id = get_node_id(passage.x[i], passage.y[i])

		if (node_id < 0):
			#print("Discarding node, node_id out of bounds: ", node_id)
			continue

		if node_id not in nodes:
			nodes[node_id] = []

		# add timecoord to specific node
		nodes[node_id].append((passage.x[i], passage.y[i], passage.time[i]))

		# in case there is only datapoint in previous node, add the next one
		if prev_id != node_id and prev_id != -1:

			if prev_id not in nodes:
				print("Prev id missing", prev_id, node_id)
				nodes[prev_id] = []

			# add timecoord to specific node
			nodes[prev_id].append((passage.x[i], passage.y[i], passage.time[i]))

		# if second last, add the last one
		if i == len(passage.x) - 2:
			nodes[node_id].append(
				(passage.x[i + 1], passage.y[i + 1], passage.time[i + 1]))

		prev_id = node_id

	# add passages to nodes
	for key in nodes:
		if key not in Node.list:
			Node.list[key] = Node(key)

		Node.list[key].add_passage(passage, nodes[key])


# return node_id based on coordinates
def get_node_id(x, y):

	max_x = Node.get_nodes_in_row()

	if x < 0:
		return -1

	if y < AREA_BOUNDARIES[2]:
		#print("Discarding node, y-coord out of bounds: ", passage.y[i])
		return -1

	node_x = x // Node.SPACING_M
	node_y = (y - AREA_BOUNDARIES[2]) // Node.SPACING_M

	node_id = node_x + (node_y * max_x)

	return node_id


def draw_reach_percentages(type_accuracy=False, limit=0):
	scores = []

	for n in Node.list:

		if type_accuracy:
			rp = 1 - n.accuracy_score

			if rp == 0:
				continue

			scores.append(n.accuracy_score)
		else:
			rp = n.reach_percentage()

			if rp < limit:
				continue

			scores.append(rp)

		if len(n.passages) < 20:
			continue

		color = (rp, 0, 1 - rp)
		n.draw(color)

	return scores


def get_closest_node(x, y):

	closest_dist = 9999999999999999
	closest_node = -1

	for node in Node.list:
		if closest_dist > util.distance((x, y), (node.x, node.y)):
			closest_dist = util.distance((x, y), (node.x, node.y))
			closest_node = node

	return closest_node
