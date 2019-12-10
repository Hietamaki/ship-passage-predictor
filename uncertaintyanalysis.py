import random
import numpy as np
import scipy
import matplotlib.pyplot as plt
import constants as c

from node import Node
from database import load_list
from map import Map
from predict import predict_going, going_preprocess
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors

nodes = load_list(c.NODES_FILENAME)

n = nodes[601]

def pick_random_passage(node, n):

	labeleds = [i for i in range(0, len(node.label))]
	size = len(labeleds) if len(labeleds) < n else n

	return random.sample(labeleds, size)

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

n.draw()
#print(n.rp)

#Map.draw()

#print(len(n.passages))
means = []
#for p in pick_random_passage(n, 50):
p = pick_random_passage(n, 1)[0]
route = n.get_route(p)
x_train, x_test, labels, k = going_preprocess(nodes, route[0], route[1])
nearest = NearestNeighbors(n_neighbors=k)
nearest.fit(x_train)
dists, neighbors_id = nearest.kneighbors(x_test)
print(neighbors_id[0])
print("A")
for i in range(0, 500):
	means.append(np.mean(np.random.choice(labels[neighbors_id[0]], n.reach_k)))
	


print(means)
print(mean_confidence_interval(means))
print(np.mean(means))
plt.hist(means, 20)
plt.show()