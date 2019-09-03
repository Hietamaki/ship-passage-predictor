import sys

from aisparser import convert_all_data
from nodegeneration import generate_nodes


print(sys.argv)
print("Pre-processing all AIS data.")

convert_all_data()
generate_nodes()
#load_data(AIS_DATA_PATH + "AIS_2018-05_1.txt")
