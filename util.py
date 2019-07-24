from datetime import datetime
import random

import numpy as np
from shapely.geometry import Point

def format_date(ts):
	return datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')


def random_color():
	return (random.random(), random.random(), random.random())

# @.input	self
#			start timeloc
#			end timeloc for which to calculate velocity
# @.output	velocity in m/s, course
#
def get_velocity(start, end):

	# euclidean distance, not geodesic calculation
	# feels slow, but should be O(n)
	point1 = Point(start[0], start[1])
	point2 = Point(end[0], end[1])

	dist = point1.distance(point2)

	time_passed = end[2] - start[2]

	if start == end:
		print("Start is end")
		time_passed = 1
	elif time_passed < 1:
		print("get_speed(): trying to divide by", time_passed, "distance")
		time_passed = 1

	m_s = dist / time_passed
	course = np.arctan2(point2.x - point1.x, point2.y - point1.y)

	return m_s, course

#print(get_velocity((0, 0, 9), (1, 1, 1)))
