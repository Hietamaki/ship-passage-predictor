import random

import constants as c
from database import load_list
from predict import predict_going, calculate_arrival
from map import Map
from util import format_date, random_color

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import (brier_score_loss, precision_score, recall_score,
                             f1_score, matthews_corrcoef)

def pick_random_passage(node, n):

	labeleds = [i for i in range(0, len(node.label))]
	size = len(labeleds) if len(labeleds) < n else n

	return random.sample(labeleds, size)


n_train = load_list(c.NODES_FILENAME)
n_test = load_list(c.TEST_NODES_FILENAME)

actuals = []
predictions = []

cmap = cm.get_cmap('coolwarm')

NUM_PASSAGES = 50

for n in n_test:
	correct = 0
	total = 0

	# do not include nodes that are out of reach area
	if n.reach_percentage() < 0.01 or len(n.passages) < 200:
		continue
	labels = n.get_labels()
	for i in pick_random_passage(n, NUM_PASSAGES):
		passage = n.passages[i]
		route = n.get_route(i)
		if len(route) < 2:
			print("Empty route")
			continue

		# pick random spot from passage.route
		# use 2 data points for calculation
		spot = random.randint(0, len(route) - 2)
		prediction = predict_going(n_train, route[spot], route[spot + 1])[0]

		'''
		if abs(t) > 13:
			n.add_passage(passage, n.passage_i[i])
			#print("Already visited area")
			c = random_color()
			passage.plot(c)
			n.draw(c)
			Map.draw_circle(route[spot + 1][0], route[spot + 1][1], 2000, "red")
			#print(n.label[i])
			print(
				predict_t / 3600, real_arrival / 3600, "(",
				format_date(route[spot + 1][2]),
				format_date(passage.enters_meas_area()), ")")
		'''
		actuals.append(labels[i])
		predictions.append(prediction)

		correct += labels[i] == prediction

		#if labels[i] != prediction:
		#	passage.plot(random_color())
		#total += 1

	#if n.reach_acc < 1:
	#hmmp = np.bincount(np.array(labels[i]) == np.array(predictions))[1]
	hmmp = correct / NUM_PASSAGES
	print(correct, NUM_PASSAGES, hmmp)
	n.draw(cmap(np.round(hmmp, 1)))


# do confusion matrix
matrix = confusion_matrix(actuals, predictions)
text = "x"
print(matrix)
print("\tPrecision: %1.3f" % precision_score(actuals, predictions))
print("\tRecall: %1.3f" % recall_score(actuals, predictions))
print("\tF1: %1.3f\n" % f1_score(actuals, predictions))
print("\tMatthew's: %1.3f\n" % matthews_corrcoef(actuals, predictions))
#print("Average time delta", np.mean(td))
#text = "Correct predictions {0}%\n".format(int((1) / len(actuals) * 100))
#text += "n=" + str(len(td))
#print(text)
Map.draw("Prediction accuracy", cbar=1, cbar_steps=11)

def draw_chart(values):
	plt.hist(values, np.arange(-5, 5, step=0.5), density=True)
	plt.xlabel("correct predictions")
	plt.ylabel("propability")
	plt.xticks(np.arange(2, 0, step=-1))
	#plt.yticks(np.arange(0, 1, step=0.2))
	plt.ticklabel_format(axis='x')
	plt.gca().set_aspect('auto', adjustable='datalim')
	#plt.text(0, .025, r'$\mu=100,\ \sigma=15$')
	# xy scale is dependant on data, bad practice
	plt.text(-5.2, 1.45, text)
	plt.show()

def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    #classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax

plot_confusion_matrix(
	actuals, predictions, ["Yes", "No"], True,
	"Prediction accuracy for ships going to measurement area"
	)
plt.show()


#draw_chart(td)

#Map.draw()


# draw nn-passages for debug

# find testpassage from n_test and calculate real time of arrival
