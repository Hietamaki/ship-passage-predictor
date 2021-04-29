import numpy as np

from map import Map
from route import route_in_area

#MEASUREMENT_START_HOUR = 8
#MEASURMENT_END_HOUR = 17


class Passage:

	next_id = 0

	def __init__(self, ship, xyt):
		Passage.next_id += 1
		self.id = Passage.next_id
		self.ship = ship
		self.interpolate(xyt[0], xyt[1], xyt[2])

		# saves index when in meas area
		self.reaches = self.reaches_measurement_area()
		# maybe seperating concerns of reach_index and reaches y/n
		# would be good practice

	# returns time when enters measurement area
	# or time to measurement area from time_delta, if time_delta > 0
	def enters_meas_area(self, time_delta=0):
		return self.time[self.reaches[0]] - time_delta

	def interpolate(self, x, y, time):

		# interpolate with 10 minute interval
		self.time = np.arange(time[0], time[-1], 600)
		self.x = np.interp(self.time, time, x).astype(np.int32)
		self.y = np.interp(self.time, time, y).astype(np.int32)

	def reaches_measurement_area(self):
		return route_in_area(np.vstack((self.x, self.y)))
		
		# check if time is between 8.00-16.00
		#time_window = False

		#if in_area is not False:
		#	for i in range(in_area[0], in_area[1]):
		#		ts = self.time[i]
		#		hour = datetime.fromtimestamp(int(ts)).hour
		#		if hour >= MEASUREMENT_START_HOUR and hour < MEASURMENT_END_HOUR:
		#			time_window = True

		#if time_window:
		#	return in_area
		#else:
		#	return False

		#return in_area

	def plot(self, color="red", timelimit=-1, timelimit2=-1):

		x = self.x
		y = self.y

		if timelimit > 0:
			times = (self.time >= timelimit) & (self.time <= timelimit2)
			#print(times)
			x = x[times]
			y = y[times]
			#nz = np.nonzero(times)[0]
			Map.draw_circle(x[0], y[0], 2000, "orange")

		Map.plot_route(x, y, color=color)

	# return the part of route that is in measurement area
	
	def route_in_meas_area(self):

		route = self.reaches

		# if route is not in measurement area
		if route is False:
			return ([], [], [])

		#	+1 timecoord in each direction
		start = route[0]
		end = route[1]

		if start > 0:
			start -= 1

		if end < len(self.x):
			end += 1

		if start:
			return (
				self.x[start:end],
				self.y[start:end],
				self.time[start:end])
