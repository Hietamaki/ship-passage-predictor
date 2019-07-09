#%matplotlib inline
from datetime import datetime, timedelta
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix

from map import Map
from ship import Ship
import util
#%pylab inline
#LIMIT_TO_DATE = datetime(2018, 5, 8).timestamp()


# test case:
print("Loading test case...")
map = Map()
Ship.load()

attributes = []
labels = []

# preprocess
print("# preprocess")

for ship in Ship.list:
	for passage in ship.passages:
		attributes.append([passage.x, passage.y])
		#attributes[0].append(passage.x)
		#attributes[1].append(passage.y)
		labels.append(np.repeat(passage.id, len(passage.x)))

attributes = np.array(attributes)
labels = np.array(labels)

print(attributes.shape)

print(len(attributes), len(attributes[1]), len(labels))
# train test split
print("# train test split")

x_train, x_test, y_train, y_test = train_test_split(
	attributes, labels, test_size=0.2)

print(x_train.shape)
# feature scaling
print("# feature scaling")

scaler = StandardScaler()
scaler.fit(x_train)

x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

# training and predictions
print("# training and predictions")
classifier = KNeighborsClassifier(n_neighbors=11)
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

# evaluating the algorithm
print("# evaluating the algorithm")

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))


#for p in Ship.list[0].passages:
#	p.plot(util.random_color())

#plt = map.draw_map()

#map.draw_reach_area("2018-05-01", "2018-05-20")

#plt.show()


'''
for i in ships[0].time:
	print (util.format_date(i))

route = ships[13].get_route(
	datetime(2018, 5, 8).timestamp(),
	datetime(2018, 6, 8).timestamp())
map.plot_route(route["x"], route["y"])
print(route)

ships[13].create_passages()
'''
'''
for p in ships[2].passages:
	map.plot_route(p['x'], p['y'], util.random_color())
for passage in range(0, len(ships[13].passages)):

	map.plot_route(ship.x[passage, ])

	passage
'''
#from_whence = datetime(2018, 5, 2, 0).timestamp()
'''
for ship in ships:
	r = ship.get_route(from_whence)

	if len(r['x']) > 0:
		starting_points.append([r['x'][0], r['y'][0]])
'''