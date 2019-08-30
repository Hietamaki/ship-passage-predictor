# - reach measurement area:
#	- (index laajemmaksi länteen?)
# - time of day featureksi
from datetime import datetime, timedelta
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix

from map import Map
from ship import Ship
import node
import util


def normalize_features(train_data, test_data):

	scaler = StandardScaler()
	scaler.fit(train_data)

	train_data = scaler.transform(train_data)
	test_data = scaler.transform(test_data)

	return train_data, test_data


#
# returns most likely passage and likelihood of reaching area

def predict_path(start, end):

	m_s, cog = util.get_velocity(start, end)
	new_passage = np.array([np.sin(cog), np.cos(cog), m_s])
	new_passage = np.reshape(new_passage, (-1, 3))
	print(new_passage)

	# Node from start of path
	nod = node.get_closest_node(start[0], start[1])

	if not nod:
		print("Node not found?")
		return

	x_train, x_test = normalize_features(nod.get_features(), new_passage)

	print("# training and predictions")
	classifier = KNeighborsClassifier(n_neighbors=nod.optimal_k)
	classifier.fit(x_train, nod.get_labels())

	# calculate mean from:
	#print(classifier.kneighbors())

	y_pred = classifier.predict(x_test)

	# evaluating the algorithm
	print("# evaluating the algorithm")
	print(y_pred)
	dists, neighbors_id = classifier.kneighbors(new_passage)

	passes = []
	for p_id in neighbors_id[0]:
		passes.append(nod.passages[p_id])

	return passes

	#print(confusion_matrix(y_test, y_pred))
	#print(classification_report(y_test, y_pred))
#print("Loading test case...")
#Ship.load_all()

#test_ship = Ship.list[1]
#pas = test_ship.passages[0]

#predict_path(pas.x, pas.y)


def calculate_mean_route(passages):

	routes = []
	max_size = 0

	for passage in passages:

		if passage.reaches is False:
			continue

		# get part of routes in area
		routes.append(passage.route_in_meas_area())
		'''
		rx, ry, rt = passage.route_in_meas_area()

		# interpolation to 1 min spacing
		nt = np.arange(rt[0], rt[-1], 60)
		nx = np.interp(nt, rt, rx).astype(np.int32)
		ny = np.interp(nt, rt, ry).astype(np.int32)

		routes.append((nx, ny, nt))
		'''
		rx_len = len(routes[-1][0])

		if max_size < rx_len:
			max_size = rx_len

	# interpolate arrays to same size
	x_coords = np.arange(0, max_size+1)

	standardized_routes = []

	for r in routes:
		print(max_size, np.linspace(0, max_size, len(r[0])))
		standardized_routes.append((
			np.interp(x_coords, np.linspace(0, max_size, len(r[0])), r[0]).astype(np.int32),
			np.interp(x_coords, np.linspace(0, max_size, len(r[1])), r[1]).astype(np.int32),
			np.interp(x_coords, np.linspace(0, max_size, len(r[2])), r[2]).astype(np.int32)))
		print(r[0], "vs")
		print(standardized_routes[-1][0])

	# calculate mean
	route = np.array(standardized_routes)

	return np.mean(route, axis=0)

def test_case(node_id=-1):
	#map = Map()

	# preprocess
	print("# preprocess")

	if node_id != -1:
		nlist = [node_id]
	else:
		nlist = node.Node.list

	for n in nlist:
		attributes = n.get_features()
		labels = n.get_labels()

		print(attributes.shape)
		print(len(attributes), len(labels))

		# train test split
		print("# train test split")

		x_train, x_test, y_train, y_test = train_test_split(
			attributes, labels, test_size=0.2)

		print(x_train.shape)

		# feature scaling
		print("# feature scaling")
		x_train, x_test = normalize_features(x_train, x_test)

		# training and predictions
		print("# training and predictions")
		knn = KNeighborsClassifier(n_neighbors=n.optimal_k)
		print(knn.n_neighbors)
		knn.fit(x_train, y_train)
		print(knn.score(x_train, y_train))

		y_pred = knn.predict(x_test)
		#print(y_pred)

		# evaluating the algorithm
		print("# evaluating the algorithm")

		print(confusion_matrix(y_test, y_pred))
		print(classification_report(y_test, y_pred))
