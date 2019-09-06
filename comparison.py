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
	real_arrival = 99999990

	while testpassage.reaches is False and bool(real_arrival > (3600 * 8)):

		testnode = random.choice(shipfile)
		if len(testnode.passages) < 1:
			print("Zero len", testnode.passages)
			print(testnode.x)
			continue
		testpassage = random.choice(testnode.passages)

		if testpassage.reaches is not False:
			real_arrival = testpassage.enters_meas_area() - testpassage.time[0]
			print(real_arrival/3600)
		print("Try again ", testpassage.reaches, real_arrival / 3600)
	print("RRRR ", real_arrival / 3600)

	return testpassage


def human_readable_time(time):
	return "{0} h {1} min".format((time // 60 // 60), (time // 60 % 60))


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

# draw nn-passages

route = calculate_mean_route(predict_p)
route2 = calculate_mean_route(predict2_p)
Map.plot_route(route[0], route[1], "yellow")
Map.plot_route(route2[0], route2[1], "purple")

Map.draw_circle(testpassage.x[testpassage.reaches[0]], testpassage.y[testpassage.reaches[0]], 3000, "white")

print("Predicted arrival", human_readable_time(predict_t))
print("Real arrival", human_readable_time(real_arrival))
print("Predicted arrival2", human_readable_time(predict2_t))
print("Real arrival", human_readable_time(real_arrival2))

Map.draw_map().show()

# find testpassage from n_test and calculate real time of arrival