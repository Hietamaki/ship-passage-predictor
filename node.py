import pandas as pd

import map
import ship
import util


class Node:
	SPACING_M = 10000

	list = {}

	@classmethod
	def load_all(cls):

		cls.list = pd.read_hdf('nodes.h5', 'df').values
		print("Loaded nodes",len(cls.list))

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
		self.passages = []
		self.cog = []
		self.speed = []
		self.label = []
		#self.list[id] = self

	def find_optimal_k(node):
		return 11

	def add_passage(self, passage, id):

		#if not self.list[self.id]:
		#	self.list[self.id] = []

		#calculate speed from
		#passage[0] passage[-1]
		#calculate cog from
		#print(passage)
		speed, course = util.get_velocity(passage[0], passage[-1])
		self.speed.append(speed)
		self.cog.append(course)
		self.passages.append(id)
		#print(Node.list[id].passages)

	#@classmethod
	#def initialize_all(cls):
#		cls.list = [Node(x) for x in range(0, 5000)]
#		print("Nodes initialized",len(Node.list))

	@classmethod
	def save_node_indices(cls, passage):

		area_boundaries = map.get_area_boundaries()
		max_x = cls.get_nodes_in_row()

		node_ids = {}
		prev_id = 0

		for i in range(0, len(passage.x) - 1):
			node_x = passage.x[i] // cls.SPACING_M
			node_y = (passage.y[i] - area_boundaries[2]) // cls.SPACING_M
			node_id = node_x + (node_y * max_x)

			if prev_id == 0:
				prev_id = node_id

			if (passage.y[i] < area_boundaries[2]):
				#print("Discarding node, y-coord out of bounds: ", passage.y[i])
				continue

			#print(node_x, node_y, node_id)
			if node_id not in node_ids:
				node_ids[node_id] = []

			node_ids[node_id].append((passage.x[i], passage.y[i], passage.time[i]))

			# in case there is only datapoint in previous node, add the next one
			if prev_id != node_id:

				if prev_id not in node_ids:
					print("Prev id missing",prev_id, node_id)
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

			cls.list[key].add_passage(node_ids[key], passage.id)

def generate_nodes():

	ship.Ship.load_all()
	for shp in ship.Ship.list:
		for passage in shp.passages:
			Node.save_node_indices(passage)
