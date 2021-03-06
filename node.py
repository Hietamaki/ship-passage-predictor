# Node
#
import warnings
warnings.filterwarnings('once')

import numpy as np
from sklearn.metrics import make_scorer, matthews_corrcoef
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

from map import Map
from predict import predict_path, calculate_arrival
from util import get_xyt, get_velocity

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
		self.rp = -1
		self.uncertainty = []

		self.x = id % NODES_IN_ROW * SPACING_M + (SPACING_M / 2)
		self.y = (id // NODES_IN_ROW) * SPACING_M + 6100000 + (SPACING_M / 2)

	# add passage to node and calculate speed and course inside node
	# @.in
	#	self
	#	passage
	#	part of passage (timecoords) that is in node
	#		[(x, y, t), (x, y, t)]
	def add_passage(self, passage, route):

		node_enter = get_xyt(passage, route[0])
		node_exit = get_xyt(passage, route[-1])

		if passage.reaches is False:
			self.label.append(False)
		else:
			time_to_measurement = passage.enters_meas_area(node_enter[2])

			# is passage going to measurement area or coming from measurement area?
			if time_to_measurement < 0:
				# false if already exited measurement area
				# converting to bool from numpy.bool
				measurement_exit_t = passage.time[passage.reaches[1]]
				self.label.append(bool(node_enter[2] <= measurement_exit_t))
			else:
				# false if over 8 hours to measurement area
				self.label.append(time_to_measurement < (3600 * 8))

		speed, course = get_velocity(node_enter, node_exit)
		self.speed.append(speed)
		self.cog.append(course)
		self.passages.append(passage)
		self.passage_i.append((route[0], route[-1]))

		# time of arrival from exiting node to meas area
		if self.label[-1] is not False:
			self.arrival.append(passage.enters_meas_area(node_exit[2]))

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
			cog = self.getattr_reaching_passages("cog")
			speed = self.getattr_reaching_passages("speed")

		# break course to x, y components
		features = np.array((cog, speed))
		features = np.reshape(features.T, (-1, 2))

		return features

	def getattr_reaching_passages(self, what):

		attrs = []

		for i in range(0, len(self.label)):
			if self.label[i] is not False:
				attr = getattr(self, what)
				attrs.append(attr[i])

		return attrs

	def reach_percentage(self):

		if self.rp == -1:
			k = 0
			for i in self.label:
				if i:
					k += 1

			self.rp = k / len(self.label)

		return self.rp

	def get_k(self):
		if self.reach_k == -1:
			return 1
		else:
			return self.reach_k

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

	def get_route(self, i, reach_only=False):
		# impelement
		pi = self.passage_i
		pa = self.passages
		if reach_only:
			pi = self.getattr_reaching_passages("passage_i")
			pa = self.getattr_reaching_passages("passages")

		start, end = pi[i]
		array = []

		for j in range(start, end + 1):
			array.append(get_xyt(pa[i], j))
		return array

	def find_reach_k(self, scale=True):

		if self.reach_percentage() == 0 or self.reach_percentage() == 1:
			return -1, -1, -1
		max_k = 25
		# k ei voi olla isompi kuin samplen koko. k-fold 5:ll?? k = sampleja * 4/5
		if 35 > len(self.passages):
			max_k = len(self.passages) // 5 * 4
			#print("Set Max K to", max_k)
		#print(len(self.passages))
		param_grid = {'n_neighbors': np.arange(1, max_k)}

		#def my_scorer(y_true, y_pred):
		#	return np.count_nonzero(y_true == y_pred) / y_true.shape[0]

		scorer = make_scorer(matthews_corrcoef)

		with warnings.catch_warnings(record=True) as w:
			warnings.simplefilter("ignore")
			
			knn_gscv = GridSearchCV(
				KNeighborsClassifier(), param_grid,
				cv=10, n_jobs=-1, scoring=scorer)

			#UndefinedMetricWarning: F-score is ill-defined and being set to 0.0 due to no predicted samples.

			features = self.get_features()
			#print(features)

			print("RP for node", self.id, "is", self.reach_percentage())

			if scale:
				scaler = StandardScaler()
				scaler.fit(features)
				features = scaler.transform(features)

			#print(features)
			optimize_a = True

			if optimize_a:
				best_k = []
				weight = []
				best_score = []

				print("Node scaled. Calculating weight.")

				for w in np.arange(0, 1.1, 0.1):
					weighted_features = (w, 1 - w) * features
					#print(w, "Weighted features: ", weighted_features)
					knn_gscv.fit(weighted_features, self.get_labels())
					best_k.append(knn_gscv.best_params_['n_neighbors'])
					weight.append(w)
					best_score.append(knn_gscv.best_score_)

				print("Node weighted, scores: ", best_score)
				print("Best Ks: ", best_k)
				print("Best weight: ", weight)

				best_score = np.array(best_score)
				i = best_score.argmax()
				#print("Setting to", knn_gscv.best_params_, knn_gscv.best_score_)
				print("Best score:", best_score[i], "index", i)
				print("Best K and a combination:", best_k[i], np.round(weight[i],2))
				print("\n")
				print("\n")

				return best_k[i], np.round(weight[i], 2), best_score[i]
			else:
				knn_gscv.fit(features, self.get_labels())
				return knn_gscv.best_params_['n_neighbors'], 0.5, knn_gscv.best_score_

	# find optimal k for
	# 1) place and time prediction
	# 2) going to area prediction
	def find_time_k(self, scale=True):

		features = self.get_features(True)
		label = self.arrival

		if len(features) < 3:
			# nodesta ei l??hde v??h. kolmea reitti?? mittausalueelle
			return 0, 0

		#f_train, f_test, l_train, l_test = train_test_split(
		#	features, label, test_size=0.2)

		max_k = 25
		if len(features) < max_k:
			max_k = len(features)

		all_ks = []

		for i in range(0, len(features)):
			means = []
			route = self.get_route(i, True)
			#print(route[i][0], route[i][1])
			#testidatalle tee predict path k max_k:lla
			if len(route) < 2:
				print("hups", route)
				route.append(route[0])
			pas, part = predict_path(self.parent.values(), route[0], route[1], max_k)

			if not pas:
				return 0, 0

			#sitten k??y l??pi mill?? k:n arvolla p????see l??himm??ksi todellista
			#print(eta, l_test[i])

			# toista parittomat k arvot 1 - max_k
			for k in np.arange(1, max_k + 1, 2):
				means.append(calculate_arrival(pas[0:k], route[0], part[0:k]))
				#print(k, means)

			#katso mit?? k:n arvoa on eniten

			#print(find_nearest(means, l_test[i]))

			array = np.asarray(means)
			idx = (np.abs(array - label[i])).argmin() * 2 + 1

			all_ks.append(idx)
		#means[idx]

		#print(all_ks, np.argmax(np.bincount(all_ks)))
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

	Map.draw()
	return scores
