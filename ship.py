import sys

class Ship:

	def __init__(self, id, x, y, time):
		self.id = id
		self.x = x
		self.y = y
		self.time = time
		self.passages = []

	# making data structure [passage: {x,y,time}]
	def create_passages(self):

		previous_beginning = 0

		for beginning in self.detect_passages():
			
			passage = {
				'x': self.x[previous_beginning:beginning],
				'y': self.y[previous_beginning:beginning],
				'time': self.time[previous_beginning:beginning]
			}

			self.passages.append(passage)
			previous_beginning = beginning


	# detecting start of passages to .passages[]
	# speed < 22.2 km/h
	# or
	# time > 1h
	def detect_passages(self):

		# 1h
		DT_LIMIT = 3600*2

		# count dt to previous observation > speed
		dt = []
		beginnings = []

		for i in range(1, len(self.x)):
			dt.append(self.time[i] - self.time[i-1])
			
			if dt[-1] >= DT_LIMIT:
				beginnings.append(i)
				#print(dt[-1]//60//60)


		beginnings.append(len(self.x)-1)
		#print("dt",beginnings)
		return beginnings


	def get_route(self, start_time = 0, end_time = 253385798400000):
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

	def get_range_by_time(self, start_time = 0, end_time = 253385798400000):

		range_start = -1
		range_end = len(self.x)-1

		for i in range(0, len(self.x)):
			#print(self.time[i], "vs.")
			#print(end_time)

			if start_time > self.time[i]:
				continue
			elif end_time < self.time[i]:
				#print("Range ends", i)
				range_end = i-1
				break
			elif range_start == -1:
				#print("Range starts", i)
				range_start = i

		return [range_start, range_end]
