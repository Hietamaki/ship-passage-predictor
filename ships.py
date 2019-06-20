import sys
#from datetime import datetime

class Ships:

	def __init__(self):
		self.data = {}

	# @.output	list of loaded ship ids
	#
	def list_ships(self):
		return list(self.data.keys())

	# @.input	filename of file that holds AIS data
	# @.output	dictionary
	#		{ ship_id: [
	#			[unixtime, lat, lon], [unixtime, lat, lon], ...] } 
	#

	def load_data(self, filename, limit_to_date = sys.maxsize):

		# data is in form:
		# shipid (unixtime lat lon) (unixtime lat lon) (unixtime lat lon) ... \n
		

		with open(filename) as file:

			for raw_line in file.readlines():

				line = raw_line.strip().split(' ')
				ship_id = line[0]

				locations = []

				for x in range(1, len(line), 3):

					if int(line[x]) > limit_to_date:
						#if (line[0] == "230992680"):
						#	print("line[x]:       %s >" % format_date(line[x]))
						#	print("LIMIT_TO_DATE: %s" % format_date(LIMIT_TO_DATE))
						break

					locations.append(line[x:x+3])

				if locations:
					self.data[ship_id] = locations