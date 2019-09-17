from node import Node

from constants import AREA_BOUNDARIES, NODES_IN_ROW, SPACING_M
from database import load_list, save_list


# Generate nodes and find optimal k value for each
def generate_nodes(filename, nodes_filename, optimize_k=True):

	print("Generating nodes to", nodes_filename)
	node_list = {}

	for shp in load_list(filename):
		for passage in shp.passages:

			for key, value in split_passage(passage).items():
				if key not in node_list:
					node_list[key] = Node(key, node_list)

				node_list[key].add_passage(passage, value)

	# Remove if node has fewer than x samples
	removed_nodes = []
	for key, val in node_list.items():
		if len(val.passages) < 20:
			#print("Del", key, len(val.passages))
			removed_nodes.append(key)

	for key in removed_nodes:
		del node_list[key]

	# Optimize K
	if optimize_k:
		for n in range(0, len(node_list)):
			node = node_list.values()[i]
			print("Finding K for node (xy", n.x, n.y, ")", i, "of", len(node_list))
			n.time_k, n.time_k_acc = n.find_time_k()
			n.area_k, n.reach_k_acc = (5, 1)
			#print("Scaling before & after:", n.find_optimal_k(False), n.optimal_k)

	print("Saving", len(node_list), "nodes to local disk...")
	save_list(nodes_filename, node_list, 'w')


# split passage into nodes
def split_passage(passage):

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
		nodes[node_id].append(i)

		# in case there is only datapoint in previous node, add the next one
		if prev_id != node_id and prev_id != -1:

			if prev_id not in nodes:
				print("Prev id missing", prev_id, node_id)
				nodes[prev_id] = []

			# add timecoord to specific node
			nodes[prev_id].append(i)

		# if second last, add the last one
		if i == len(passage.x) - 2:
			nodes[node_id].append(i + 1)

		prev_id = node_id

	return nodes


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
