from shapely import geometry

from passage import Passage


class Ship:

	def __init__(self, id, x, y, time):
		self.id = id
		self.x = x
		self.y = y
		self.time = time
		self.passages = []

		self.create_passages()

	# making data structure [passage: {x,y,time}]
	def create_passages(self):

		for passage_indices in self.detect_passages():

			#more testing
			if passage_indices[0] + 1 >= passage_indices[1]:
				#print(passage_indices, " :error")
				continue

			passage = Passage(
				self.x[passage_indices[0]:passage_indices[1]],
				self.y[passage_indices[0]:passage_indices[1]],
				self.time[passage_indices[0]:passage_indices[1]]
			)

			self.passages.append(passage)

	# detecting start of passages to .passages[]
	# speed <  MOVEMENT_DETECTION_MS
	# or
	# time > MAXIMUM_BLACKOUT_S
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

			# check if passage is started
			if start_of_passage >= 0:
				# lopetetaan passage jos ehdot täyttyy
				if time_passed >= MAXIMUM_BLACKOUT_S or self.get_speed(i) < MOVEMENT_DETECTION_MS:
					passages.append((start_of_passage, i))
					start_of_passage = -1
			else:
				# aloitetaan uusi passage jos ehdot täyttyy
				if time_passed < MAXIMUM_BLACKOUT_S and self.get_speed(i) > MOVEMENT_DETECTION_MS:
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

		# euclidean distance, not geodesic calculation
		# feels slow, but should be O(n)
		dist = geometry.Point(self.x[index], self.y[index]).distance(geometry.Point(self.x[index-1], self.y[index-1]))
		time_passed = self.time[index] - self.time[index-1]
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

	def get_node_index(self, time):

		NODE_SPACING_M = 10000

		#for passage.inpassag
		
		self.x / NODE_SPACING_M
