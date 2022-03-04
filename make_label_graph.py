#%% 
import pandas as pd
import networkx as nx
from tqdm import tqdm

round_i = 1

# %%
print('reading in data...')
base = f'./data/label-graph'
nodes = pd.read_csv(f'{base}/nodes.csv')
edges = pd.read_csv(f'{base}/edges.csv')

# %%
G = nx.Graph()
G.add_edges_from([[n1,id2]for id1,n1,id2,n2,aid,a in tqdm(edges.values,desc='adding edges to graph..')])

# %%
nx.write_gml(G,f'{base}/test.gml')
nx.write_gexf(G,f'{base}/test.gexf')
# %%
