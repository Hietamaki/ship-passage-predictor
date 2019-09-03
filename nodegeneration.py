from node import Node
import ship
import pandas as pd

from constants import NODES_FILE_NAME, AREA_BOUNDARIES, NODES_IN_ROW, SPACING_M


# Generate nodes and find optimal k value for each
def generate_nodes(optimize_k=True):

	ship.Ship.load_all()
	for shp in ship.Ship.list:
		for passage in shp.passages:
			extract_passage_to_nodes(passage)

	# Remove if node has fewer than x samples
	removed_nodes = []
	for key, val in Node.list.items():
		if len(val.passages) < 20:
			#print("Del", key, len(val.passages))
			removed_nodes.append(key)

	for key in removed_nodes:
		del Node.list[key]

	# Optimize K
	if optimize_k:
		for n in Node.list.values():
			n.optimal_k, n.accuracy_score = n.find_optimal_k()
			#print("Scaling before & after:", n.find_optimal_k(False), n.optimal_k)

	print("Saving", len(Node.list), "nodes to local disk...")
	df = pd.Series(Node.list)
	df.to_hdf(NODES_FILE_NAME, 'df', mode='w')


def extract_passage_to_nodes(passage):

	nodes = {}
	prev_id = get_node_id(passage.x[0], passage.y[0])

	# associate every xy coordinate in passage to correct node
	for i in range(0, len(passage.x) - 1):
		node_id = get_node_id(passage.x[i], passage.y[i])

		if (node_id < 0):
			#print("Discarding node, node_id out of bounds: ", node_id)
			continue

		if node_id not in nodes:
			nodes[node_id] = []

		# add timecoord to specific node
		nodes[node_id].append((passage.x[i], passage.y[i], passage.time[i]))

		# in case there is only datapoint in previous node, add the next one
		if prev_id != node_id and prev_id != -1:

			if prev_id not in nodes:
				print("Prev id missing", prev_id, node_id)
				nodes[prev_id] = []

			# add timecoord to specific node
			nodes[prev_id].append((passage.x[i], passage.y[i], passage.time[i]))

		# if second last, add the last one
		if i == len(passage.x) - 2:
			nodes[node_id].append(
				(passage.x[i + 1], passage.y[i + 1], passage.time[i + 1]))

		prev_id = node_id

	# add passages to nodes
	for key in nodes:
		if key not in Node.list:
			Node.list[key] = Node(key)

		Node.list[key].add_passage(passage, nodes[key])


# return node_id based on coordinates
def get_node_id(x, y):

	max_x = NODES_IN_ROW

	if x < 0:
		return -1

	if y < AREA_BOUNDARIES[2]:
		#print("Discarding node, y-coord out of bounds: ", passage.y[i])
		return -1

	node_x = x // SPACING_M
	node_y = (y - AREA_BOUNDARIES[2]) // SPACING_M

	node_id = node_x + (node_y * max_x)

	return node_id
