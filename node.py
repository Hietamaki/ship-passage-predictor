import map


class Nodes:
	SPACING_M = 10000

	@classmethod
	def get_nodes_in_row(cls):
		area_boundaries = map.Map.get_measurement_area()
		return (area_boundaries[1] // cls.SPACING_M)

	# @.output dictionary of nodes {id: [x, y]}

	@classmethod
	def get_nodes(cls):
		return {
			123: [1, 2],
			345: [3, 4]}

		#area = Map.get_measurement_area()

		#for i in len()
		# cl.SPACING_M

	def find_optimal_k(node):
		return 11