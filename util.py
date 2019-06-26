from datetime import datetime
import random

def format_date(ts):
	return datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')

def random_color():
	return (random.random(),random.random(),random.random())
