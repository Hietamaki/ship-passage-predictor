# Correct way to do bootstrap confidence interval analysis
# Old version was using "arbitrary test data"

#

#eli käytetään koko OPETUSDATAA

#käydään jokainen solmu läpi:
#	jokainen opetusdatan X läpi:
#		alkuperäinen otos k näytettä
#		bootstarp otokset, eli uudelleenarvotaan vain alkper otos k näytettä
#		bootstrap otoksista otetaan ka.
#		järjestetään pienemmistä isoimpaan
#		lasketaan sitten niistä 95% luottamusväli.
#		tallennetaan X:ään 0, 1 tai -1		

import random
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import constants as c

from node import Node
from database import load_list, save_list
from map import Map
from predict import new_passage, center_cogs, feature_preparation
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

BOOTSTRAP_SAMPLES = 200

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

def find_train_node(test_node):
	for n in nodes:
		if n.x == test_node.x and n.y == test_node.y:
			return n

def get_uncertainty(x_train, x_test, y_train, y_test, k):



	nearest = NearestNeighbors(n_neighbors=k)
	x_train = center_cogs(x_train, np.array([0, x_test[1]]));
	nearest.fit(x_train)

	dists, neighbors_id = nearest.kneighbors(new_passage(x_test[0], 0))

	means = []
	#print(neighbors_id, n.get_k())
	#print("A",labels[neighbors_id[0], n.reach_k])
	alkper = labels[neighbors_id[0]]
	alkper_ka = np.mean(alkper)
	#print(alkper)

	for i in range(0, BOOTSTRAP_SAMPLES):
		means.append(np.mean(np.random.choice(alkper, k)) - alkper_ka)

	#print(alkper_ka + np.sort(means))

	#summ = np.sum(means)
	#print(summ)

	#if sum == 0:
	#	return 0
	#elif sum == len(means):
	#	return 1

	ci_l = np.quantile(means, 0.025) + alkper_ka
	ci_u = np.quantile(means, 0.975) + alkper_ka
	#print(alkper_ka + ci_l, alkper_ka + ci_u)
	#print(alkper_ka)
	if ci_l <= 0.5 and ci_u <= 0.5:
		return 0, alkper_ka
	elif ci_l >= 0.5 and ci_u >= 0.5:
		return 1, alkper_ka
	else:
		return -1, alkper_ka
#print(len(n.passages))
#for p in pick_random_passage(n, 50):

#results = {}

for i, test_node in enumerate(tnodes):

	train_node = find_train_node(test_node)
	#if i < 171:
	#	continue
	if not train_node:
		print("Train node is missing. ID: ", test_node.id, "XY:",test_node.x, test_node.y, "Passages:", len(test_node.passages))
		continue
	#print(train_node.id, test_node.id)

	results = []
	results_pred = []

	x_train, x_test, labels, k = feature_preparation(train_node, alpha=False)
	x_test, null, y_test, null2 = feature_preparation(test_node, alpha=False)

	if train_node.reach_percentage() == 0:
		# Certainly 0 so basically n.uncertainty = [0,0,0,...]
		continue
	#p = pick_random_passage(n, 1)[0]
	for p in range(0, len(x_test)):
		going = get_uncertainty(
			x_train,
			x_test[p],
			labels,
			y_test[p],
			k)
		#if going is not -1:
		#if n.id not in results:
		#	results[n.id] = []
		results.append(going[0])
		results_pred.append(going[1])
		
	#print(nodes_going[n.id], going)
	#print(n.uncertainty)
	#print(results)
	test_node.uncertainty = np.array(results)
	test_node.uncertainty_pred = np.array(results_pred)
	print(i,"of", len(nodes), "Results:", len(results), "of", len(x_train), np.sum(results) / len(results))
	#break
	#print(np.mean(means))
save_list(c.TEST_NODES_FILENAME, tnodes, "w")
#plt.hist(means, 20)


#plt.show()