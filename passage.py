import map


class Passage:

	def __init__(self, x, y, time):
		self.x = x
		self.y = y
		self.time = time

		self.interpolate()
		self.save_node_indices()

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

	def save_node_indices(self):

		area_boundaries = map.Map.get_area_boundaries()
		max_x = Nodes.maximum_nodes()

		node_ids = []

		for i in range(0, len(self.x)):
			node_x = self.x[i] // Nodes.SPACING_M
			node_y = (self.y[i] - area_boundaries[2]) // Nodes.SPACING_M
			node_id = node_x + (node_y * max_x)

			#print(node_x, node_y, node_id)

			if node_id not in node_ids:
				node_ids.append(node_id)

		self.nodes = node_ids

	def plot(self, color="red"):
		map.Map.plot_route(self.x, self.y, color=color)
