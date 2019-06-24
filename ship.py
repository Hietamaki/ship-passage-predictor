import sys

class Ship:

	def __init__(self, id, x, y, time):
		self.id = id
		self.x = x
		self.y = y
		self.time = time

	# @.output	list of loaded ship ids
	#
	def get_route(self, start_time = 0, end_time = 253385798400000):

		range = self.get_range(start_time, end_time)

		return {
			"x": self.x[range[0]:range[1]],
			"y": self.y[range[0]:range[1]],
			"time": self.time[range[0]:range[1]]
		}

	def get_range(self, start_time = 0, end_time = 253385798400000):

		range_start = -1
		range_end = len(self.x)-1

		for i in range(0, len(self.x)):
			#print(self.time[i], "vs.")
			#print(end_time)

			if start_time > self.time[i]:
				continue
			elif end_time < self.time[i]:
				print("Range ends", i)
				range_end = i-1
				break
			elif range_start == -1:
				print("Range starts", i)
				range_start = i

		return [range_start, range_end]