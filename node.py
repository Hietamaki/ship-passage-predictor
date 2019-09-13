# Node
#

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

from map import Map
import util

from constants import SPACING_M, NODES_IN_ROW


class Node:
	def __init__(self, id):
		self.id = id
		self.passages = []
		self.cog = []
		self.speed = []
		self.label = []
		self.exits_node = []
		self.route = []
		self.arrival = []

		self.x = id % NODES_IN_ROW * SPACING_M + (SPACING_M / 2)
		self.y = (id // NODES_IN_ROW) * SPACING_M + 6100000 + (SPACING_M / 2)

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
			time_to_measurement = passage.enters_meas_area(enter_point[2])

			# is passage going to measurement area or coming from measurement area?
			if time_to_measurement < 0:
				# false if already exited measurement area
				# converting to bool from numpy.bool
				self.label.append(bool(enter_point[2] <= passage.time[passage.reaches[1]]))
			else:
				# false if over 8 hours to measurement area
				self.label.append(time_to_measurement < (3600 * 8))

		speed, course = util.get_velocity(enter_point, exit_point)
		self.exits_node.append(exit_point[2])  # change to more exact later
		self.speed.append(speed)
		self.cog.append(course)
		self.passages.append(passage)

		# time of arrival from exiting node to meas area
		if self.label[-1] is not False:
			self.arrival.append(passage.enters_meas_area(exit_point[2]))

		self.route.append(np.array(route))
		# experimental, more memory efficient would be to just save indexes
		# nodes.h5: 234M before, 415M after, with np.array 347M

	def draw(self, color='red'):
		Map.draw_circle(self.x, self.y, SPACING_M // 2, color)

	# convert to ndarray
	def get_labels(self):
		return np.array(self.label)

	# getting features of passages in node
	# reaching_only=True will return paths that only reach
	# measurement area, used for non-supervised learning
	#
	def get_features(self, reaching_only=False):

		cog = self.cog
		speed = self.speed

		if reaching_only:
			cog = self.getattr_reaching_passages("speed")
			speed = self.getattr_reaching_passages("cog")

		# break course to x, y components
		features = np.array((np.sin(cog), np.cos(cog), speed))
		features = np.reshape(features, (-1, 3))

		return features

	def getattr_reaching_passages(self, what):

		attrs = []

		for i in range(0, len(self.label)):
			if self.label[i] is not False:
				attr = getattr(self, what)
				attrs.append(attr[i])

		return attrs

	def reach_percentage(self):
		k = 0
		for i in self.label:
			if i:
				k += 1

		return k / len(self.label)

	# Return arrival time in seconds
	# not used
	def predict_arrival_time(self):
		p1 = self.getattr_reaching_passages("passages")
		p2 = self.getattr_reaching_passages("exits_node")
		times = []

		for i in range(0, len(p1)):
			td = p1[i].enters_measurement_area() - p2[i]
			times.append(td)

		# next only calculate from nearest neighbours
		return np.average(times)

	# find optimal k for
	# 1) place and time prediction
	# 2) going to area prediction
	def find_optimal_k(self, scale=True):

		features = self.get_features(True)
		label = self.arrival

		f_train, f_test, l_train, l_test = train_test_split(
			features, label, test_size=0.2)

		if len(features) < 3:
			return 0, 0

		#return 5, 1 # debug option
		max_k = 25
		if len(f_train) < max_k:
			max_k = len(f_train)
		# k ei voi olla isompi kuin samplen koko. k-fold 5:llä k = sampleja * 4/5
		#if 35 > len(self.passages):
		#	max_k = len(self.passages) // 5 * 4
			#print("Set Max K to", max_k)

		means = []

		for test in f_test:

		for k in np.arange(1, max_k + 1):
			means.append(np.average(f_train[0:k]))

		print(means)
		print("Real", l_test)
		print(util.find_nearest(means, l_test[0]))

		array = np.asarray(array)
    	idx = (np.abs(array - value)).argmin()
    	means[idx]

		#if scale:
		#	scaler = StandardScaler()
		#	scaler.fit(features)
		#	features = scaler.transform(features)

		#print("Setting to", knn_gscv.best_params_, knn_gscv.best_score_)
		return util.find_nearest(means, l_test[0]), 0


def draw_reach_percentages(node_list, type_accuracy=False, limit=0):
	scores = []

	for n in node_list:

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


def get_closest_node(node_list, x, y):

	closest_dist = 9999999999999999
	closest_node = -1

	for node in node_list:
		if closest_dist > util.distance((x, y), (node.x, node.y)):
			closest_dist = util.distance((x, y), (node.x, node.y))
			closest_node = node

	return closest_node
