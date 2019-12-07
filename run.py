from functools import partial
import sys
from time import time
import warnings
warnings.filterwarnings('once')

from aisparser import convert_all_data
from nodegeneration import generate_nodes

from constants import (
	AIS_DATA_PATH, SHIPS_FILENAME, NODES_FILENAME,
	TEST_DATA_PATH, TEST_NODES_FILENAME, TEST_SHIPS_FILENAME)

from util import readable_time

start_time = time()

print = partial(print, flush=True)

job = ""
optimize_k = True

if len(sys.argv) > 1:
	job = sys.argv[1]

if len(sys.argv) > 2:
	if sys.argv[2] == "skipk":
		print("No K optimization")
		optimize_k = False

if job == "train" or job == "all":
	print("Pre-processing train data from", AIS_DATA_PATH)
	convert_all_data(AIS_DATA_PATH, SHIPS_FILENAME)
	generate_nodes(SHIPS_FILENAME, NODES_FILENAME, optimize_k)

elif job == "train-nodes":
	generate_nodes(SHIPS_FILENAME, NODES_FILENAME, optimize_k)

if job == "test" or job == "all":
	# k optimization is not necessary for test data
	print("Pre-processing test data from", TEST_DATA_PATH)
	convert_all_data(TEST_DATA_PATH, TEST_SHIPS_FILENAME)
	generate_nodes(TEST_SHIPS_FILENAME, TEST_NODES_FILENAME, optimize=False)
elif job == "test-nodes":
	generate_nodes(TEST_SHIPS_FILENAME, TEST_NODES_FILENAME, optimize=False)

if int(start_time) == int(time()):
	print("Available commands: <all, train, test, train-nodes, test-nodes> <(optional) skipk>")
else:
	print("Compiling took", readable_time(time() - start_time))
