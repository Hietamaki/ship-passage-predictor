import pandas as pd

import map
import util


class Node:
	SPACING_M = 10000

	list = []

	@classmethod
	def load_all(cls):

		cls.list = pd.read_hdf('nodes.h5', 'df').values

	@classmethod
	def get_nodes_in_row(cls):
		area_boundaries = map.Map.get_measurement_area()
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
		self.list.append(self)
		self.passages = []
		self.cog = []
		self.speed = []
		self.label = []

	def find_optimal_k(node):
		return 11

	def add_passage(self, passage, id):

		if not self.list[self.id]:
			self.list[self.id] = []

		#calculate speed from
		#passage[0] passage[-1]
		#calculate cog from
		#print(passage)
		speed, course = util.get_velocity(passage[0], passage[-1])
		self.speed.append(speed)
		self.cog.append(course)
		self.passages.append(id)


Node.list = [Node(x) for x in range(0, 5000)]