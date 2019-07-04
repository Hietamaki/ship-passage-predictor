from passage import Passage


class Ship:

	def __init__(self, id, x, y, time):
		self.id = id
		self.x = x
		self.y = y
		self.time = time
		self.passages = []

	# making data structure [passage: {x,y,time}]
	def create_passages(self):

		for passage_indices in self.detect_passages():

			#more testing
			if passage_indices[0] + 1 >= passage_indices[1]:
				print(passage_indices, " :error")
				continue

			passage = Passage(
				self.x[passage_indices[0]:passage_indices[1]],
				self.y[passage_indices[0]:passage_indices[1]],
				self.time[passage_indices[0]:passage_indices[1]]
			)

			self.passages.append(passage)

	# detecting start of passages to .passages[]
	# speed < 22.2 km/h
	# or
	# time > 1h
	def detect_passages(self):

		# 1h
		DT_LIMIT = 3600 * 2

		# count dt to previous observation > speed
		dt = []
		passages = []
		start_of_passage = 0
		end_of_passage = 0

		for i in range(1, len(self.x)):
			dt.append(self.time[i] - self.time[i - 1])

			if dt[-1] >= DT_LIMIT:
				passages.append((start_of_passage, i))
				start_of_passage = i+1
				#print(dt[-1]//60//60)

		return passages

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
