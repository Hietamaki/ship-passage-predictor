import random

import constants as c
from database import load_list
from map import Map
import predict
from route import calculate_mean_route


def pick_random_passage(shipfile):

	testnode = random.choice(shipfile)

	if len(testnode.passages) < 1:
		print("Zero len", testnode)
		return

	testpassage = random.choice(testnode.passages)

	while testpassage.reaches is False:
		testnode = random.choice(shipfile)
		if len(testnode.passages) < 1:
			print("Zero len", testnode.passages)
			print(testnode.x)
			continue
		testpassage = random.choice(testnode.passages)
		print("Try again")

	return testpassage


def human_readable_time(time):
	return "{0} h {1} min".format((time // 60 // 60), (time // 60 % 60))


n_train = load_list(c.NODES_FILENAME)
n_test = load_list(c.TEST_NODES_FILENAME)

testpassage = pick_random_passage(load_list(c.TEST_NODES_FILENAME))

testpassage.plot()
Map.draw_circle(testpassage.x[0], testpassage.y[0], 3000, "orange")
real_arrival = testpassage.time[testpassage.reaches[0]] - testpassage.time[0]



predict_p, predict_t = predict.predict_path(
	n_train,
	(testpassage.x[0], testpassage.y[0], testpassage.time[0]),
	(testpassage.x[2], testpassage.y[2], testpassage.time[2]))

route = calculate_mean_route(predict_p)
Map.plot_route(route[0], route[1], "purple")

print(predict_t)
print("Real arrival", human_readable_time(real_arrival))
print("Predicted arrival", human_readable_time(predict_t))

Map.draw_map().show()

# find testpassage from n_test and calculate real time of arrival