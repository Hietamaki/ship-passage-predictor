import numpy as np
import pandas as pd
from util import distance

import passage as psg


class Ship:

	list = []

	@classmethod
	def load_all(cls):

		cls.list = pd.read_hdf('ships.h5', 'df').values

	# @.output attributes, labels and indices of passages

	@classmethod
	def get_passages_as_table(cls):
		attributes = []
		labels = []
		indices = []
		x = []
		y = []

		for ship in cls.list:
			for passage in ship.passages:
				x += passage.x
				y += passage.y

				# repeating value reaches for every coordinate
				labels += [passage.reaches] * len(passage.x)
				indices += [passage.id] * len(passage.x)

		attributes = np.array([x, y])
		attributes = np.reshape(attributes, (-1, 2))
		labels = np.array(labels)

		return attributes, labels, indices

	def __init__(self, id, x, y, time):
		self.id = id
		self.x = x
		self.y = y
		self.time = time
		self.passages = []

		self.create_passages()

	# detect and create Passage objects from timecoords
	def create_passages(self):

		for passage_indices in self.detect_passages():

			# discard passages that have less than 3 data points
			if passage_indices[0] + 1 >= passage_indices[1]:
				continue

			passage = psg.Passage(
				self.x[passage_indices[0]:passage_indices[1]],
				self.y[passage_indices[0]:passage_indices[1]],
				self.time[passage_indices[0]:passage_indices[1]],
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

		for i in range(1, len(self.x)):
			time_passed = self.time[i] - self.time[i - 1]

			ship_still = time_passed >= MAXIMUM_BLACKOUT_S
			speed = get_speed(i)
			lost_contact = speed < MOVEMENT_DETECTION_MS
			#lost_contact = self.get_speed(i) < MOVEMENT_DETECTION_MS

			# check if passage is started
			if start_of_passage >= 0:
				# end passage
				if ship_still or lost_contact:
					passages.append((start_of_passage, i))
					start_of_passage = -1
			else:
				# start passage
				if not ship_still and not lost_contact:
					start_of_passage = i

		# close if passage is started
		if start_of_passage >= 0:
			passages.append((start_of_passage, len(self.x)))

		return passages

	# @.input	self
	#			index of timeloc for which to calculate speed
	# @.output	speed in m/s
	#
	def get_speed(self, index):

		dist = distance(
			(self.x[index - 1], self.y[index - 1]),
			(self.x[index], self.y[index]))

		time_passed = self.time[index] - self.time[index - 1]

		if time_passed < 1:
			print("get_speed(): trying to divide by", time_passed, "at index", index, "ship id", self.id)
			time_passed = 1

		m_s = dist / time_passed

		return m_s

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
