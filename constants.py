#import numpy as np

# file structure
AIS_DATA_PATH = "ship-data/"
SHIPS_FILENAME = 'ships.h5'
NODES_FILENAME = 'nodes.h5'
TEST_DATA_PATH = "test-data/"
TEST_SHIPS_FILENAME = 'ships-test.h5'
TEST_NODES_FILENAME = 'nodes-test.h5'

# map specifications
# etrs xx yy

# Define MEAS AREA [x1, x2, y1, y2]
#MEAS_AREA = []
AREA_BOUNDARIES = [0, 700000, 6100000, 6750000]  # 6450, 6750

# nodes spacing
SPACING_M = 10000
NODES_IN_ROW = (AREA_BOUNDARIES[1] // SPACING_M)

MAX_K = 25
