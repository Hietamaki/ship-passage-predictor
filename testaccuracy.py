import random

import constants as c
from database import load_list
from predict import predict_path, calculate_arrival
from map import Map
from util import format_date, random_color

import numpy as np
import matplotlib.pyplot as plt


def pick_random_passage(node, n):

	labeleds = [i for i in range(0, len(node.label)) if node.label[i]]
	size = len(labeleds) if len(labeleds) < n else n

	return random.sample(labeleds, size)


n_train = load_list(c.NODES_FILENAME)
n_test = load_list(c.TEST_NODES_FILENAME)

td = []
succeeds = 0

for n in n_test:

	# exclude rarer nodes to fix overrepresentation
	if n.reach_percentage() < 0.1 or len(n.passages) < 100:
		continue

	for i in pick_random_passage(n, 10):
		passage = n.passages[i]
		route = n.get_route(i)

		# pick random spot from passage.route
		# use 2 data points for calculation
		spot = random.randint(0, len(route) - 2)
		real_arrival = passage.enters_meas_area(route[spot + 1][2])

		predict_p, pred_parts = predict_path(n_train, route[spot], route[spot + 1])

		if predict_p == 0:
			continue
		predict_t = calculate_arrival(predict_p, route[spot], pred_parts)

		t = (predict_t - real_arrival) / 3600
		if abs(t) > 13:
			n.add_passage(passage, n.passage_i[i])
			#print("Already visited area")
			c = random_color()
			passage.plot(c)
			n.draw(c)
			Map.draw_circle(route[spot + 1][0], route[spot + 1][1], 2000, "red")
			#print(n.label[i])
			print(
				predict_t / 3600, real_arrival / 3600, "(",
				format_date(route[spot + 1][2]),
				format_date(passage.enters_meas_area()), ")")

		if abs(t) < 0.5:
			succeeds += 1

		#print(t)
		td.append(t)

print("Average time delta", np.mean(td))
text = "Predictions in 1 hour margin {0}%\n".format(int(succeeds / len(td) * 100))
text += "n=" + str(len(td))


def draw_chart(values):
	plt.hist(values, np.arange(-5, 5, step=0.5), density=False)
	plt.xlabel("hours")
	plt.ylabel("propability")
	plt.xticks(np.arange(-5, 6, step=1))
	#plt.yticks(np.arange(0, 1, step=0.2))
	plt.ticklabel_format(axis='x')
	plt.gca().set_aspect('auto', adjustable='datalim')
	#plt.text(0, .025, r'$\mu=100,\ \sigma=15$')
	# xy scale is dependant on data, bad practice
	plt.text(-5, 400, text)
	plt.show()


draw_chart(td)

#Map.draw()


# draw nn-passages for debug

# find testpassage from n_test and calculate real time of arrival
