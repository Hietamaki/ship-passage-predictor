# - reach measurement area:
#	- (index laajemmaksi länteen?)
# - time of day featureksi
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.metrics import classification_report, confusion_matrix

from map import Map
import node
from util import get_velocity, distance


def normalize_features(train_data, test_data):

	if len(train_data) < 1:
		print("Train data is empty!")

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

	# Node from start of path
	nod = node.get_closest_node(nodes, start[0], start[1])

	if not nod:
		print("Node not found?")
		return 0, 0

	if nod.reach_percentage == 0:
		print("No passages reaching meas zone.")
		return 0, 0

	if nod.time_k == 0:
		print("K=0, no routes reaching.")
		return 0, 0

	x_train, x_test = normalize_features(nod.get_features(True), new_passage)

	k = nod.time_k

	#if k > len(x_test):
	#	#print(k, len(x_test))
	#	k = len(x_test)

	nearest = NearestNeighbors(n_neighbors=k)
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
	return passes, calculate_arrival(passes, start)


# calculate average arrival time from passages and their start times
# from node at point
def calculate_arrival(passages, point):
	times = []

	# either
	# 1) add correction how long it takes from observation to node exit
	# 2) from each passage take point that is closest to the observation
	#	 and use that time

	# from passage start index to point index ~(only inside node to increase perf)
	# dist(point, pas) <- get smallest index from x,y -> use time

	for pas in passages:
		smallest = 99999999999999
		smallest_j = -1009

		for j in range(0, len(pas.x) - 1):
			dist = distance(
				(pas.x[j], pas.y[j]),
				(point[0], point[1]))

			if dist < smallest:
				smallest = dist
				smallest_j = j

			#Map.draw_circle(pas.x[j], pas.y[j], 1000, "red")
		#print("Smallest J is", smallest_j)

		#Map.draw_circle(pas.x[smallest_j], pas.y[smallest_j], 1000, "orange")

		td = pas.enters_meas_area() - pas.time[smallest_j]
		times.append(td)

	#print(td)
	#Map.draw_circle(point[0], point[1], 1000, "blue")

	return int(np.average(times))


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
