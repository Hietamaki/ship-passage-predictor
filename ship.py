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
				self,
				self.xyt[:, indices[0]:indices[1]]
			)

			self.passages.append(passage)

	# @. output
	#	list of passage indexes in route
	#		[(start, end)]
	# 	start new passage if:
	#		   ship stays still or previous contact is over MAXIMUM_BLACKOUT_S
	def detect_passages(self):

		# count time_passed to previous observation > speed
		passages = []
		passage_started = 0

		for i, active in enumerate(self.when_active()):
			if passage_started >= 0:
				# end passage if ship is not active
				if not active:
					passages.append((passage_started, i))
					passage_started = -1
			elif active:
				# start passage
				passage_started = i

		if passage_started >= 0:
			# end unfinished passage
			passages.append((passage_started, self.xyt.shape[1]))

		return passages

	# @.input	self
	# @.output	return indices when ship is active
	#
	def when_active(self):

		# 2h
		MAXIMUM_BLACKOUT_S = 3600 * 2
		# 2 m/s = ~3.9 knots
		MOVEMENT_DETECTION_MS = 2

		# calculate ship movement
		xyt_delta = self.xyt[:, 1:] - self.xyt[:, 0:-1]

		dist = np.linalg.norm(xyt_delta[0:2], axis=0)
		speed = dist / xyt_delta[2]

		ship_still = xyt_delta[2] >= MAXIMUM_BLACKOUT_S
		lost_contact = speed < MOVEMENT_DETECTION_MS
		
		return ~(ship_still | lost_contact)

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