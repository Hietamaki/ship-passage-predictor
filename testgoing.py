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

UNCERTAINTY_ANALYSIS = 1;
PERMUTATION_TEST = 2;
# 1 = varmat menevät, 0 = varmat ei menevät, -1 = confidence interval on both sides
MAP_TYPE = 1
NUM_PASSAGES = 100

MAP_CMAP = 'coolwarm'

def pick_random_passage(node, n, analysis_type):

	if UNCERTAINTY_ANALYSIS == analysis_type:
		ids = node.uncertainty == MAP_TYPE
		passages = [i for i, x in enumerate(ids) if x]

		size = len(passages) if len(passages) < n else n

		return random.sample(passages, size)
	else:
		# Accuracy analysis:
		passages = [i for i in range(0, len(node.label))]
		size = len(passages) if len(passages) < n else n

		return random.sample(passages, size)

		# Accuracy analysis:
		# Do stratification so that at least 20%
#		positive_passages = [i for i, x in enumerate(np.array(node.label) == True) if x]
#		negative_passages = [i for i, x in enumerate(np.array(node.label) == False) if x]

		#passages = [i for i in range(0, len(node.label))]
#		size = len(positive_passages) if len(positive_passages) < int(n/2) else int(n/2)
#		pos_arr = random.sample(positive_passages, size)
#		size = len(negative_passages) if len(negative_passages) < int(n/2) else int(n/2)
#		neg_arr = random.sample(negative_passages, size)

		return pos_arr + neg_arr

def do_analysis(n_train, n, actuals, predictions, num_passages, analysis_type):

	correct = 0
	count = 0
	labels = n.get_labels()

	for i in pick_random_passage(n, num_passages, analysis_type):
			if analysis_type == UNCERTAINTY_ANALYSIS and n.uncertainty[i] != MAP_TYPE:
				continue

			passage = n.passages[i]
			route = n.get_route(i)
			if len(route) < 2:
				print("Empty route")
				continue

			# pick random spot from passage.route
			# use 2 data points for calculation
			spot = random.randint(0, len(route) - 2)
			prediction = predict_going(n_train,
				route[spot], route[spot + 1],
				k=-1,
				alpha=True,
				permutate=(analysis_type == PERMUTATION_TEST))[0]

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
			count += 1

			#if labels[i] != prediction:
			#	passage.plot(random_color())
			#total += 1
	return correct, count, actuals, predictions

def do_uncertainty(n_train, n, actuals, predictions, num_passages, analysis_type):

	labels = n.get_labels()
	#print(labels)
	#print(actuals)
	actuals = labels.tolist() + actuals
	predictions = (n.uncertainty_pred >= 0.5).tolist() + predictions
	#predictions = predict_going + np.asarray(labels)
	#print(n.uncertainty)
	return np.sum(n.uncertainty != -1), n.uncertainty.shape[0], actuals, predictions

def test_going(n_train, n_test, analysis_type = 0, num_passages = NUM_PASSAGES):
	#n_train = load_list(c.NODES_FILENAME)
	#n_test = load_list(c.TEST_NODES_FILENAME)

	actuals = []
	predictions = []

	total = 0
	total2 = 0
	cmap = cm.get_cmap(MAP_CMAP)
	Map.init()

	for n in n_test:
		
		#total = 0

		# do not include nodes that are out of reach area
		# n.reach_percentage() > 0.95 or 
		if n.reach_percentage() < 0.01 or len(n.passages) < NUM_PASSAGES:
			#print("skipping: "+str(n.reach_percentage()) + " (len "+str(len(n.passages))+")")
			continue

		if analysis_type == UNCERTAINTY_ANALYSIS:
			if not hasattr(n, 'uncertainty_pred'):
				print("Voi ei", n.uncertainty)
				continue
			correct, count, actuals, predictions = do_uncertainty(n_train, n, actuals, predictions, num_passages, analysis_type)

			total += np.sum(n.uncertainty != -1)
			total2 += n.uncertainty.shape[0]
		else:
			correct, count, actuals, predictions = do_analysis(n_train, n, actuals, predictions, num_passages, analysis_type)

		if count >= 5:
			#if n.reach_acc < 1:
			#hmmp = np.bincount(np.array(labels[i]) == np.array(predictions))[1]
			hmmp = correct / count
			#print(correct, count, hmmp, np.round(hmmp, 1))
			n.draw(cmap(np.round(hmmp, 1) - 0.05))

	label = "Uncertainty analysis" if analysis_type else "Prediction accuracy"
	if analysis_type == PERMUTATION_TEST:
		label = "Permutation test"

	Map.draw(cbar=True, cbar_steps=10, cmap=MAP_CMAP)
	print("Uncertainty: total, total2")
	print(total, total2, total / total2)
	actuals = np.array(actuals)
	predictions = np.array(predictions)
	print("actuals & predictions:")
	print(actuals)
	print(predictions)

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
	
	label = "Prediction accuracy for ships going to measurement area"

	if analysis_type == PERMUTATION_TEST:
		label = "Permutation test for ships going to measurement area"

	plot_confusion_matrix(
		actuals, predictions, ["Yes", "No"], True,
		label
		)
	plt.show()

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



#draw_chart(td)

#Map.draw()


# draw nn-passages for debug

# find testpassage from n_test and calculate real time of arrival
