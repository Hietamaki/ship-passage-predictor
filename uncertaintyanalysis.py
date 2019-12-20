import random
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import constants as c

from node import Node
from database import load_list, save_list
from map import Map
from predict import predict_going, going_preprocess
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

nodes = load_list(c.NODES_FILENAME)
tnodes = load_list(c.TEST_NODES_FILENAME)

#n = nodes[11]
#for i, na in enumerate(nodes):
#	print(i, na.reach_k, na.reach_percentage())

def pick_random_passage(node, n):

	labeleds = [i for i in range(0, len(node.label))]
	size = len(labeleds) if len(labeleds) < n else n

	return random.sample(labeleds, size)

def mean_confidence_interval(data, confidence=0.95):
	return stats.t.interval(confidence, len(data)-1, loc=np.mean(data), scale=stats.sem(data))

#n.draw()

#print(n.rp)

#Map.draw()

def get_route_ci(nodes, route):
	means = []
	x_train, x_test, labels, k = going_preprocess(nodes, route[0], route[1])
	nearest = NearestNeighbors(n_neighbors=k)
	nearest.fit(x_train)
	dists, neighbors_id = nearest.kneighbors(x_test)
	#print(neighbors_id, n.get_k())
	#print("A",labels[neighbors_id[0], n.reach_k])

	for i in range(0, 100):
		means.append(np.mean(np.random.choice(labels[neighbors_id[0]], n.get_k())))

	#print(means)

	sum = np.sum(means)

	if sum == 0:
		return 0
	elif sum == len(means):
		return 1

	ci = mean_confidence_interval(means)
	if ci[0] < 0.5 and ci[1] < 0.5:
		return 0
	elif ci[0] > 0.5 and ci[1] > 0.5:
		return 1
	else:
		print(ci)
		return -1
#print(len(n.passages))
#for p in pick_random_passage(n, 50):

#results = {}

for i, n in enumerate(tnodes):

	results = []

	if n.reach_percentage() == 0:
		continue
	#p = pick_random_passage(n, 1)[0]
	for p in range(0, len(n.passages)):
		going = get_route_ci(nodes, n.get_route(p))
		#if going is not -1:
		#if n.id not in results:
		#	results[n.id] = []
		results.append(going)

	#print(nodes_going[n.id], going)
	n.uncertainty = np.array(results)
	print(i,"of", len(tnodes), "Results:", len(results), "of", len(n.passages), np.sum(results) / len(results))

	#print(np.mean(means))
save_list(c.TEST_NODES_FILENAME, tnodes, "w")
#plt.hist(means, 20)


#plt.show()