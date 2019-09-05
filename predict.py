# - reach measurement area:
#	- (index laajemmaksi länteen?)
# - time of day featureksi
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.metrics import classification_report, confusion_matrix

import node
from util import get_velocity


def normalize_features(train_data, test_data):

	scaler = StandardScaler()
	scaler.fit(train_data)

	train_data = scaler.transform(train_data)
	test_data = scaler.transform(test_data)

	return train_data, test_data


#
# returns
#	most likely passages
#	how long it will take to arrive in h

def predict_path(nodes, start, end):

	m_s, cog = get_velocity(start, end)
	new_passage = np.array([np.sin(cog), np.cos(cog), m_s])
	new_passage = np.reshape(new_passage, (-1, 3))
	print(new_passage)

	# Node from start of path
	nod = node.get_closest_node(nodes, start[0], start[1])

	if not nod:
		print("Node not found?")
		return

	x_train, x_test = normalize_features(nod.get_features(True), new_passage)

	print("# training and predictions")
	nearest = NearestNeighbors(n_neighbors=nod.optimal_k)
	nearest.fit(x_train)

	# calculate mean from:
	dists, neighbors_id = nearest.kneighbors(x_test)

	passes = []
	exits = []
	passages = nod.getattr_reaching_passages("passages")
	exits_node = nod.getattr_reaching_passages("exits_node")
	for p_id in neighbors_id[0]:
		passes.append(passages[p_id])
		exits.append(exits_node[p_id])
	return passes, calculate_arrival(passes, exits)


#calculate average arrival time from passages and their start times from node
# return in h
def calculate_arrival(pas, exits):
	times = []

	for i in range(0, len(pas)):
		td = pas[i].enters_measurement_area() - exits[i]
		times.append(td)

	return np.average(times)/60/60


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
