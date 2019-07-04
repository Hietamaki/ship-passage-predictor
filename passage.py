from map import Map

class Passage:

	def __init__(self, x, y, time):
		self.x = x
		self.y = y
		self.time = time

		self.interpolate()
		self.save_node_indexes()

	def interpolate(self, minutes_limit=10):

		previous_time = self.time[0]
		INTERPOLATION_LIMIT = 60 * minutes_limit

		indexes = []

		#find out indexes
		for i in range(0, len(self.time)):
			time_difference = self.time[i] - previous_time
			if time_difference > INTERPOLATION_LIMIT:
				amount_to_interpolate = (time_difference // INTERPOLATION_LIMIT)
				indexes.append((i, amount_to_interpolate, time_difference))

			previous_time = self.time[i]

		index_offset = 0

		# inserting entries to list
		for i in indexes:
			index = i[0] + index_offset
			amount_to_interpolate = i[1]
			index_offset += amount_to_interpolate

			#print("Interpoloidaan ", amount_to_interpolate)
			#print("Pointsit tulee ", i[2] / (1 + amount_to_interpolate) // 60, " min välein")
			self.interpolate_coords(index, amount_to_interpolate)

	# interpolates at coords at index and previous index
	# by amount_of_points
	#
	def interpolate_coords(self, index, amount_of_points):

		if index < 1:
			print("Error, index too small", index)

		self.interpol(self.x, index, amount_of_points)
		self.interpol(self.y, index, amount_of_points)
		self.interpol(self.time, index, amount_of_points)

	def interpol(self, list, index, amount_of_points):
		base_value = list[index]
		distance = (base_value - list[index - 1]) // amount_of_points

		for i in range(0, amount_of_points):
			new_value = base_value + (distance * (i + 1))
			#print(i, amount_of_points, new_value)
			list.insert(index + i, new_value)

	def save_node_indexes(self):

		NODE_SPACING_M = 10000

		area_boundaries = Map().get_area_boundaries()
		x_maximum_cells = (area_boundaries[1] // NODE_SPACING_M)

		node_ids = []

		for i in range(0, len(self.x)):
			node_x = self.x[i] // NODE_SPACING_M
			node_y = (self.y[i] - area_boundaries[2]) // NODE_SPACING_M
			node_id = node_x + (node_y * x_maximum_cells)

			#print(node_x, node_y, node_id)

			if node_id not in node_ids:
				node_ids.append(node_id)

		self.nodes = node_ids



