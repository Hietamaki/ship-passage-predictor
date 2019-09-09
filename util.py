from datetime import datetime
from random import random

import numpy as np


def format_date(ts):
	return datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')


def readable_time(time):

	time = int(time)
	s = ""

	if (time // 3600) == 0:
		s = "{0} s".format(time % 3600)

	return "{0} h {1} min {2}".format((time // 3600), (time // 60 % 60), s)


def random_color():
	return (random(), random(), random())


# @.input	self
#			start timeloc
#			end timeloc for which to calculate velocity
# @.output	velocity in m/s, course

def get_velocity(start, end):

	# euclidean distance, not geodesic calculation

	dist = distance(start, end)

	time_passed = end[2] - start[2]

	if start == end:
		#print("Start is end")
		time_passed = 1
	elif time_passed < 1:
		print("get_velocity(): trying to divide by", time_passed, "seconds")
		time_passed = 1

	m_s = dist / time_passed
	course = np.arctan2(end[0] - start[0], end[1] - start[1])

	return m_s, course


def distance(instance1, instance2):
	# if the instances are lists or tuples:
	instance1 = np.array(instance1[0:2])
	instance2 = np.array(instance2[0:2])

	return np.linalg.norm(instance1 - instance2)
