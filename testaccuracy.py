import random

import constants as c
from database import load_list
from predict import predict_path, calculate_arrival

import numpy as np


def pick_random_passage(node):

	while True:
		rand = random.randint(0, len(node.passages) - 1)
		#print(node.label[rand], rand, node)

		if bool(node.label[rand]) is True:
			return rand


n_train = load_list(c.NODES_FILENAME)
n_test = load_list(c.TEST_NODES_FILENAME)

td = []

for n in n_test:

	if n.reach_percentage() < 0.5:
		continue

	i = pick_random_passage(n)
	passage = n.passages[i]
	route = n.get_route(i)

	# pick random spot from passage.route
	# use 2 data points for calculation
	spot = random.randint(0, len(route) - 2)

	real_arrival = passage.enters_meas_area() - passage.time[spot + 1]

	predict_p, pred_parts = predict_path(n_train, route[spot], route[spot + 1])

	if predict_p == 0:
		continue
	predict_t = calculate_arrival(predict_p, route[spot], pred_parts)


	t = (predict_t - real_arrival) / 3600
	print(t)

	td.append(t)

print("Average time delta", np.mean(td))


# draw nn-passages for debug

# find testpassage from n_test and calculate real time of arrival
