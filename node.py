# Node
#

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

from map import Map
from predict import predict_path, calculate_arrival
from util import get_xyt, get_velocity, distance

from constants import SPACING_M, NODES_IN_ROW


class Node:
	def __init__(self, id, parent_list):
		self.id = id
		self.parent = parent_list
		self.passages = []
		self.cog = []
		self.speed = []
		self.label = []
		self.passage_i = []
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

		enter_point = get_xyt(passage, route[0])
		exit_point = get_xyt(passage, route[-1])

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

		speed, course = get_velocity(enter_point, exit_point)
		self.speed.append(speed)
		self.cog.append(course)
		self.passages.append(passage)
		self.passage_i.append((route[0], route[-1]))

		# time of arrival from exiting node to meas area
		if self.label[-1] is not False:
			self.arrival.append(passage.enters_meas_area(exit_point[2]))

		#self.route.append(np.array(route))
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

	def get_route(self, i):
		# impelement
		start, end = self.passage_i[i]
		array = []

		for j in range(start, end + 1):
			array.append(get_xyt(self.passages[i], j))
		return array

	# find optimal k for
	# 1) place and time prediction
	# 2) going to area prediction
	def find_time_k(self, scale=True):

		print("Finding K for node (xy", self.x, self.y, ")")

		features = self.get_features(True)
		label = self.arrival

		if len(features) < 3:
			# nodesta ei lähde väh. kolmea reittiä mittausalueelle
			return 0, 0

		f_train, f_test, l_train, l_test = train_test_split(
			features, label, test_size=0.2)

		max_k = 25
		if len(f_train) < max_k:
			max_k = len(f_train)

		all_ks = []

		for i in range(0, len(f_test)):
			means = []
			route = self.get_route(i)
			#print(route[i][0], route[i][1])
			#testidatalle tee predict path k max_k:lla
			if len(route) < 2:
				print("hups", route)
				route.append(route[0])
			pas, part = predict_path(self.parent.values(), route[0], route[1], max_k)

			if not pas:
				return 0, 0

			#sitten käy läpi millä k:n arvolla pääsee lähimmäksi todellista
			#print(eta, l_test[i])

			# toista parittomat k arvot 1 - max_k
			for k in np.arange(1, max_k + 1, 2):
				means.append(calculate_arrival(pas[0:k], route[0], part[0:k]))
				#print(k, means)

			#katso mitä k:n arvoa on eniten

			#print(find_nearest(means, l_test[i]))

			array = np.asarray(means)
			idx = (np.abs(array - l_test[i])).argmin()

			all_ks.append(idx)
		#means[idx]

		#print(all_ks)
		return np.argmax(np.bincount(all_ks)), 0

		#if scale:
		#	scaler = StandardScaler()
		#	scaler.fit(features)
		#	features = scaler.transform(features)

		#print("Setting to", knn_gscv.best_params_, knn_gscv.best_score_)


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
