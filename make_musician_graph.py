#%% 
import pandas as pd
import networkx as nx
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

#%%
print('reading in data...')
base = f'./data/musician-graph'
nodes = pd.read_csv(f'{base}/nodes.csv')
edges = pd.read_csv(f'{base}/edges.csv')

# %%
G = nx.DiGraph()
G.add_edges_from([[a1,a2]for id1,a1,id2,a2,sid,s in tqdm(edges.values,desc='adding edges to graph..')])
nx.set_node_attributes(G,dict(zip(nodes.name,nodes.popularity.replace(np.nan,0).apply(int))),'popularity')
nx.set_node_attributes(G,dict(zip(nodes.name,nodes.followers.replace(np.nan,0).apply(int))),'followers')
#%%
def plot_degree_dist(G):
    degrees = [G.degree(n) for n in G.nodes()]
    plt.hist(degrees)
    plt.show()

# %%
nx.write_gml(G,f'{base}/test.gml')
nx.write_gexf(G,f'{base}/test.gexf')
# %%
