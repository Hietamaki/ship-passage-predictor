# helper functions to handle routes
# uses np.array(x, y, time)

#etrs xx yy
MEAS_AREA = [340000, 380000, 6620000, 6650000]
AREA_BOUNDARIES = [0, 700000, 6100000, 6750000] # 6450, 6750

# interpolates entered route to minute intervals
# move to seperate route.py?
def get_minute_interpolation():

	start, end = route_in_area(self.x, self.y)
	
	return self.x[start:end], self.y[start:end], self.time[start:end]

# return enters_i and end_i when in area or False if doesn't cross area
def route_in_area(x, y):

	enters_i = False

	if len(x) == 0:
		return False

	for i in range(0, len(x) - 1):
		if (x[i] > MEAS_AREA[0] and x[i] < MEAS_AREA[1] and
			y[i] > MEAS_AREA[2] and y[i] < MEAS_AREA[3]):

			if enters_i is False:
				enters_i = i

		elif enters_i:
			return enters_i, i

	if enters_i is not False:
		return enters_i, len(x) - 1
	else:
		return False

def is_in_area(x, y):
	return (
		x > MEAS_AREA[0] and x < MEAS_AREA[1] and
		y > MEAS_AREA[2] and y < MEAS_AREA[3])

