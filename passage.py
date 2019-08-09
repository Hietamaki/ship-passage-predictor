import map
import node


class Passage:

	next_id = 0

	def __init__(self, x, y, time, ship):
		self.x = x
		self.y = y
		self.time = time
		self.id = self.get_id()
		self.ship = ship
		self.interpolate()

		# saves index of when reaches. temporary
		self.reaches = self.reaches_measurement_area()

	@classmethod
	def get_id(cls):
		cls.next_id += 1
		return cls.next_id

	def interpolate(self, minutes_limit=10):

		previous_time = self.time[0]
		INTERPOLATION_LIMIT = 60 * minutes_limit

		indices = []

		#find out indices
		for i in range(0, len(self.time)):
			time_difference = self.time[i] - previous_time
			if time_difference > INTERPOLATION_LIMIT:
				amount_to_interpolate = (time_difference // INTERPOLATION_LIMIT)
				indices.append((i, amount_to_interpolate, time_difference))

			previous_time = self.time[i]

		index_offset = 0

		# inserting entries to list
		for i in indices:
			index = i[0] + index_offset
			amount_to_interpolate = i[1]
			index_offset += amount_to_interpolate

			self.interpolate_coords(index, amount_to_interpolate)

	# interpolates at coords at index and previous index
	# by amount_of_points
	#
	def interpolate_coords(self, index, amount_of_points):

		if index < 1:
			print("Error, index too small", index)

		self.interpolate_list(self.x, index, amount_of_points)
		self.interpolate_list(self.y, index, amount_of_points)
		self.interpolate_list(self.time, index, amount_of_points)

	def interpolate_list(self, list, index, amount_of_points):
		base_value = list[index]
		distance = (list[index - 1] - base_value) // (amount_of_points + 1)

		for i in range(0, amount_of_points):
			new_value = base_value + (distance * (i + 1))
			list.insert(index, new_value)

	def reaches_measurement_area(self):
		# todo if start of passage over 8h from reaching area, return false
		# check also if time is between 8.00-16.00
		return map.route_in_area(self.x, self.y)

	def plot(self, color="red"):
		map.Map.plot_route(self.x, self.y, color=color)
