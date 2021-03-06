# - reach measurement area:
#	- (index laajemmaksi länteen?)
# - time of day featureksi
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.metrics import classification_report, confusion_matrix

#from map import Map
from util import get_velocity, distance, get_closest


def normalize_features(train_data, test_data = False):

	#if len(train_data) < 1:
	#		print("Train data is empty!")

	scaler = StandardScaler()
	scaler.fit(train_data)

	train_data = scaler.transform(train_data)

	if test_data is not False:
		test_data = scaler.transform(test_data)

	return train_data, test_data


def center_cogs(cogs, center_cog):
	fcog = cogs - (center_cog + np.pi)
	fcog = fcog % (2 * np.pi)
	return fcog - np.pi

def new_passage(cog, speed):
	new_passage = np.array((cog, speed))
	return np.reshape(new_passage.T, (-1, 2))

def feature_preparation(nod, cog=0, m_s=0, k=-1, alpha=True):

	features = nod.get_features()
	features = np.reshape(features.T, (2, -1))
	fcog = features[0]
	fspeed = features[1]

	if len(features) < 1:
		print("No passages reaching meas zone.")
		return 0, 0

	#def to_rad(angle):
	#	return (angle + np.pi) % (2 * np.pi) - np.pi

	# reshape cog so that new_passage is at center
	fcog = center_cogs(fcog, cog)

	features = np.array((fcog, fspeed))
	features = np.reshape(features.T, (-1, 2))

	new_pas = new_passage(0, m_s)
	x_train, x_test = normalize_features(features, new_pas)

	# get optimized k
	if k == -1:
		k = nod.reach_k

	# if k not optimized (node in out of reach area or in measurement area)
	if k == -1:
		k = 1
		#huonompi tulos vaikka ei pitäisi olla väliä?
		#if nod.reach_percentage() == 1:
		#	return [True]
		#else:
		#	return [False]
	elif alpha:
		x_train = x_train * (nod.alpha, 1 - nod.alpha)
		x_test = x_test * (nod.alpha, 1 - nod.alpha)

	return x_train, x_test, nod.get_labels(), k

	#print("K=", k, "alpha=",nod.alpha)

def predict_going(nodes, start, end, k=-1, permutate=False, alpha=True):

	m_s, cog = get_velocity(start, end)

	# Node from start of path
	nod = get_closest(nodes, start[0], start[1])

	if not nod:
		print("Node not found?")
		return 0, 0

	x_train, x_test, labels, k =  feature_preparation(nod, cog, m_s, k, alpha)

	nearest = KNeighborsClassifier(n_neighbors=k)

	if permutate:
		nearest.fit(x_train, np.random.permutation(labels))
	else:
		nearest.fit(x_train, labels)
	return nearest.predict(x_test)

#
# returns
#	most likely passages
#	how long it will take to arrive in h

def predict_path(nodes, start, end, k=-1):

	m_s, cog = get_velocity(start, end)
	new_passage = np.array([np.sin(cog), np.cos(cog), m_s])
	new_passage = np.reshape(new_passage, (-1, 3))

	# Node from start of path
	nod = get_closest(nodes, start[0], start[1])

	if not nod:
		print("Node not found?")
		return 0, 0

	features = nod.get_features(True)

	if len(features) < 1:
		print("No passages reaching meas zone.")
		return 0, 0

	#if nod.time_k == 0:
	#	print("K=0, no routes reaching.")
	#	return 0, 0

	x_train, x_test = normalize_features(features, new_passage)

	if k == -1:
		k = nod.time_k

	if k == 0:
		print("K=0", len(x_train), "entries")
		k = 1
	#if k > len(x_test):
	#	#print(k, len(x_test))
	#	k = len(x_test)

	nearest = NearestNeighbors(n_neighbors=k)
	nearest.fit(x_train)

	# calculate mean from:
	dists, neighbors_id = nearest.kneighbors(x_test)

	passes = []
	part = []
	passages = nod.getattr_reaching_passages("passages")
	passage_i = nod.getattr_reaching_passages("passage_i")
	for p_id in neighbors_id[0]:
		passes.append(passages[p_id])
		part.append(passage_i[p_id])
	return passes, part


# calculate average arrival time from passages and their start times
#	passages
#	point				from node at point
#	i_limit (tuple)		limit to part of passage
def calculate_arrival(passages, point, i_limit=-1):
	times = []

	# set limits to sizes of passages if not limited
	if i_limit == -1:
		i_limit = [(0, len(passage.x) - 1) for passage in passages]

	# either
	# 1) add correction how long it takes from observation to node exit
	# 2) from each passage take point that is closest to the observation
	#	 and use that time

	# from passage start index to point index ~(only inside node to increase perf)
	# dist(point, pas) <- get smallest index from x,y -> use time

	for pas, limit in zip(passages, i_limit):
		smallest = 99999999999999
		smallest_j = -1009

		for j in range(limit[0], limit[1]):
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


def test_case(nlist):

	# preprocess
	print("# preprocess")

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
