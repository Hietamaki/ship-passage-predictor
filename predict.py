from ships import Ships
from datetime import datetime

import cartopy.crs as ccrs

def format_date(ts):
	return datetime.fromtimestamp(int(ts)/1000).strftime('%Y-%m-%d %H:%M:%S')

LIMIT_TO_DATE = datetime(2018, 5, 2).timestamp() * 1000

ships = Ships()
ships.load_data("../ship-docs/AIS_2018-05_1.txt", LIMIT_TO_DATE)

# test case:

print("Amount of ship entries: ", len(ships.list_ships()))

SHIP_KEY = ships.list_ships()[15]

print(f"Details of ship (id: {SHIP_KEY})")

y = []
x = []

for i in ships.data[SHIP_KEY]:
	y.append(i[1])
	x.append(i[0])
	print (format_date(i[2]) +" // " +str(i[0:2]))

plt = ships.draw_map()
plt.plot(x, y, color='red', linewidth=1, transform=ccrs.Geodetic())


plt.show()


#for x in ships.transform(y):
#	pass
	#print("", x[0:2], format_date(x[2]))
