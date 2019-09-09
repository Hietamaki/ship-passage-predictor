import pandas as pd


def load_list(filename):
	objects = pd.read_hdf(filename, 'df').values
	print("Loaded", len(objects), "objects from", filename)
	return objects


def save_list(filename, list, mode):
	df = pd.Series(list)
	df.to_hdf(filename, 'df', mode=mode)
