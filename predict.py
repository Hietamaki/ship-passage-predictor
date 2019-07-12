from datetime import datetime, timedelta
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix

from map import Map
from ship import Ship
import util

def normalize_features(train_data, test_data):

	scaler = StandardScaler()
	scaler.fit(train_data)

	train_data = scaler.transform(train_data)
	test_data = scaler.transform(test_data)

	return train_data, test_data

# test case:
print("Loading test case...")
#map = Map()
Ship.load_all()

# preprocess
print("# preprocess")

attributes, labels = Ship.get_passages_as_table()

print(attributes.shape)
print(len(attributes), len(labels))

# train test split
print("# train test split")

x_train, x_test, y_train, y_test = train_test_split(
	attributes, labels, test_size=0.2)

print(x_train.shape)

# feature scaling
print("# feature scaling")
x_train, x_test = normalize_features(x_train, x_test)

# training and predictions
print("# training and predictions")
classifier = KNeighborsClassifier(n_neighbors=11)
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

# evaluating the algorithm
print("# evaluating the algorithm")

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

