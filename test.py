import node

clsNode = node.Node

clsNode.load_all()

for node in clsNode.list:

	l = len(node.passages)

	if l > 100:
		print(node.id, l)
