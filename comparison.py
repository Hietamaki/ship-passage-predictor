import random

import constants as c
from database import load_list
from map import Map
import predict
from route import calculate_mean_route
from util import readable_time


def pick_random_passage(nodefile):

	while True:
		testnode = random.choice(nodefile)
		rand = random.randint(0, len(testnode.passages) - 1)
		testpassage = testnode.passages[rand]

		if testnode.label[rand] is True:
			return testpassage


n_train = load_list(c.NODES_FILENAME)
n_test = load_list(c.TEST_NODES_FILENAME)

testpassage = pick_random_passage(n_test)

testpassage.plot()
Map.draw_circle(testpassage.x[0], testpassage.y[0], 3000, "yellow")
Map.draw_circle(testpassage.x[20], testpassage.y[20], 3000, "purple")
real_arrival = testpassage.enters_meas_area() - testpassage.time[2]
real_arrival2 = testpassage.enters_meas_area() - testpassage.time[22]

predict_p, predict_t = predict.predict_path(
	n_train,
	(testpassage.x[0], testpassage.y[0], testpassage.time[0]),
	(testpassage.x[1], testpassage.y[1], testpassage.time[1]))

predict2_p, predict2_t = predict.predict_path(
	n_train,
	(testpassage.x[20], testpassage.y[20], testpassage.time[20]),
	(testpassage.x[22], testpassage.y[22], testpassage.time[22]))

# draw nn-passages for debug

route = calculate_mean_route(predict_p)
route2 = calculate_mean_route(predict2_p)
Map.plot_route(route[0], route[1], "yellow")
Map.plot_route(route2[0], route2[1], "purple")

Map.draw_circle(testpassage.x[testpassage.reaches[0]], testpassage.y[testpassage.reaches[0]], 3000, "white")

print("Predicted arrival", readable_time(predict_t))
print("Real arrival", readable_time(real_arrival))
print("Predicted arrival2", readable_time(predict2_t))
print("Real arrival", readable_time(real_arrival2))

Map.draw_map().show()

# find testpassage from n_test and calculate real time of arrival