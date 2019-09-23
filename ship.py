import numpy as np

from passage import Passage


class Ship:

	def __init__(self, xyt):

		#sometimes there are duplicate values in data
		#so remove those to ease processing
		_, idx = np.unique(xyt, axis=1, return_index=True)
		self.xyt = xyt[:, np.sort(idx)]
		self.passages = []
		self.create_passages()
		#print("paslen", len(self.passages), len(self.xyt[0]))

	# detect and create Passage objects from timecoords
	def create_passages(self):

		for indices in self.detect_passages():

			# discard passages that have less than 3 data points
			if indices[0] + 1 >= indices[1]:
				continue

			passage = Passage(
				self.xyt[0, indices[0]:indices[1]],
				self.xyt[1, indices[0]:indices[1]],
				self.xyt[2, indices[0]:indices[1]],
				self
			)

			self.passages.append(passage)

	# @. output
	#	list of passage indexes in route
	#		[(start, end)]
	# 	start new passage if:
	#		   ship stays still or previous contact is over MAXIMUM_BLACKOUT_S
	def detect_passages(self):

		# 2h
		MAXIMUM_BLACKOUT_S = 3600 * 2
		# 2 m/s = ~3.9 knots
		MOVEMENT_DETECTION_MS = 2

		# count time_passed to previous observation > speed
		time_passed = []

		passages = []
		start_of_passage = 0

		time_passed = self.xyt[2, 1:] - self.xyt[2, 0:-1]

		ship_still = time_passed >= MAXIMUM_BLACKOUT_S
		lost_contact = self.get_speed() < MOVEMENT_DETECTION_MS

		for i, (still, nosig) in enumerate(zip(ship_still, lost_contact)):
			# check if passage is started
			if start_of_passage >= 0:
				# end passage
				if still or nosig:
					passages.append((start_of_passage, i))
					start_of_passage = -1
			else:
				# start passage
				if not still and not nosig:
					start_of_passage = i

		# close if passage is started
		if start_of_passage >= 0:
			passages.append((start_of_passage, self.xyt.shape[1]))

		return passages

	# @.input	self
	#			index of timeloc for which to calculate speed
	# @.output	speed in m/s
	#
	def get_speed(self):

		xyt_delta = self.xyt[:, 1:] - self.xyt[:, 0:-1]
		dist = np.linalg.norm(xyt_delta[0:2], axis=0)
		time_passed = xyt_delta[2]
		m_s = dist / time_passed

		return m_s
	'''
	# reacharea.py functions

	def get_route(self, start_time=0, end_time=253385798400000):
		range = self.get_range_by_time(start_time, end_time)

		return self.get_timecoords(range)

	# @.output	list of loaded ship ids
	#
	def get_timecoords(self, range):

		return {
			"x": self.x[range[0]:range[1]],
			"y": self.y[range[0]:range[1]],
			"time": self.time[range[0]:range[1]]
		}

	def get_range_by_time(self, start_time=0, end_time=253385798400000):

		range_start = -1
		range_end = len(self.x) - 1

		for i in range(0, len(self.x)):
			#print(self.time[i], "vs.")
			#print(end_time)

			if start_time > self.time[i]:
				continue
			elif end_time < self.time[i]:
				#print("Range ends", i)
				range_end = i - 1
				break
			elif range_start == -1:
				#print("Range starts", i)
				range_start = i

		return [range_start, range_end]
'''