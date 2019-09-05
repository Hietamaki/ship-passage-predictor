from functools import partial
import sys

from aisparser import convert_all_data
from nodegeneration import generate_nodes

from constants import (
	AIS_DATA_PATH, SHIPS_FILENAME, NODES_FILENAME,
	TEST_DATA_PATH, TEST_NODES_FILENAME, TEST_SHIPS_FILENAME)

print = partial(print, flush=True)

job = ""

if len(sys.argv) > 1:
	job = sys.argv[1]

if job == "ships":
	print("Pre-processing train data from", AIS_DATA_PATH)
	convert_all_data(AIS_DATA_PATH, SHIPS_FILENAME)
	generate_nodes(SHIPS_FILENAME, NODES_FILENAME)

elif job == "nodes":
	generate_nodes(SHIPS_FILENAME, NODES_FILENAME)

elif job == "testships":
	print("Pre-processing test data from", TEST_DATA_PATH)
	convert_all_data(TEST_DATA_PATH, TEST_SHIPS_FILENAME)
	generate_nodes(TEST_SHIPS_FILENAME, TEST_NODES_FILENAME)

elif job == "testnodes":
	generate_nodes(TEST_SHIPS_FILENAME, TEST_NODES_FILENAME)
else:
	print("Available commands: convert, testdata")
