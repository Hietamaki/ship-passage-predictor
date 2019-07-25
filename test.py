from node import Node
import node as nd
import pandas as pd

NODES_FILE_NAME = 'nodes.h5'

nd.generate_nodes()
df = pd.Series(Node.list)
df.to_hdf(NODES_FILE_NAME, 'df', mode='w')
print("Saving", len(Node.list), "nodes to database.")