from datetime import datetime
import random

from shapely.geometry import Point

def format_date(ts):
	return datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')


def random_color():
	return (random.random(), random.random(), random.random())

	# @.input	self
	#			index of timeloc for which to calculate speed
	# @.output	velocity in m/s, course
	#
	def get_velocity(self, point1, point2):

		# euclidean distance, not geodesic calculation
		# feels slow, but should be O(n)
		point1 = Point(point1.x, point1.y)
		point2 = Point(point2.x, point2.y)
		dist = point1.distance(point2)

		time_passed = point1.time - point2.time

		if time_passed < 1:
			print("get_speed(): trying to divide by", time_passed, "distance", dist)
			time_passed = 1

		m_s = dist / time_passed
		course = 1

		return m_s, course