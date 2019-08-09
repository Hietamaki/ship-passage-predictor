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


def predict_path(x, y):

	new_passage = np.array([x, y])
	new_passage = np.reshape(new_passage, (-1, 2))

	# Node from start of path
	nod = node.get_closest_node(x[0], y[0])

	if not nod:
		print("Node not found?")
		return

	x_train, x_test = normalize_features(nod.get_features(), new_passage)

	print("# training and predictions")
	classifier = KNeighborsClassifier(n_neighbors=nod.optimal_k)
	classifier.fit(x_train, nod.get_labels())

	# calculate mean from:
	print(classifier.kneighbors())

	y_pred = classifier.predict(x_test)

	# evaluating the algorithm
	print("# evaluating the algorithm")
	print(y_pred)
	return y_pred

	#print(confusion_matrix(y_test, y_pred))
	#print(classification_report(y_test, y_pred))
#print("Loading test case...")
#Ship.load_all()

#test_ship = Ship.list[1]
#pas = test_ship.passages[0]

#predict_path(pas.x, pas.y)


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
