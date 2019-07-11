from datetime import datetime, timedelta
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix

from map import Map
from ship import Ship
import util

# test case:
print("Loading test case...")
map = Map()
Ship.load()

attributes = []
labels = []
x = []
y = []

# preprocess
print("# preprocess")

for ship in Ship.list:
	for passage in ship.passages:
		#attributes.append([passage.x, passage.y])
		x += passage.x
		y += passage.y

		labels += [passage.id] *  len(passage.x)

attributes = np.array([x,y])
attributes = np.reshape(attributes, (-1, 2))
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

