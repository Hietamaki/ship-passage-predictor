# helper functions to handle routes
# uses np.array(x, y, time)



# interpolates entered route to minute intervals
# move to seperate route.py?
def get_minute_interpolation():

	start, end = route_in_area(self.x, self.y)
	
	return self.x[start:end], self.y[start:end], self.time[start:end]



# return enters_i and end_i when in area or False if doesn't cross area
def route_in_area(x, y):

	area = MEASUREMENT_AREA
	enters_i = False

	if len(x) == 0:
		return False

	for i in range(0, len(x) - 1):
		if x[i] > area[0] and x[i] < area[1] and y[i] > area[2] and y[i] < area[3]:
			if enters_i is False:
				enters_i = i
		elif enters_i:
			return enters_i, i

	if enters_i is not False:
		return enters_i, len(x) - 1
	else:
		return False
