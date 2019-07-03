class Passage:

	def __init__(self, x, y, time):
		self.x = x
		self.y = y
		self.time = time

	def interpolate_passages(self):

		previous_time = self.time[0]
		INTERPOLATION_LIMIT = 60 * 10

		for i in range(0, len(self.time)):
			if previous_time + INTERPOLATION_LIMIT < self.time[i]:
				print(
					"Interpoloitavia pisteitä ",
					self.time[i] - previous_time % INTERPOLATION_LIMIT)

			previous_time = self.time
