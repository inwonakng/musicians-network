#%% 
import pandas as pd
import networkx as nx
import numpy as np
from tqdm import tqdm
from glob import glob
from spotify_id import get_spotify_id
import argparse
import matplotlib.pyplot as plt

round_i = 14
#%%
parser = argparse.ArgumentParser()
parser.add_argument('-r','--round',default=-1)
args = parser.parse_args()
round_i = int(args.round)
# latest mode
if round_i == -1: round_i = len(glob('./data/fromtop1000/SPO_*.csv'))
# %%
print('reading in data...')
base = f'./data/fromtop1000/musician-graph/round{round_i}'
nodes = pd.read_csv(f'{base}/nodes.csv')
edges = pd.read_csv(f'{base}/edges.csv')

# %%
G = nx.DiGraph()
G.add_edges_from([[a1,a2]for id1,a1,id2,a2,sid,s in tqdm(edges.values,desc='adding edges to graph..')])
nx.set_node_attributes(G,dict(zip(nodes.name,nodes.popularity.replace(np.nan,0).apply(int))),'popularity')
# dict(zip(nodes.name,nodes.popularity.values.apply(int)))
# dict(nodes[['name','popularity']].values.astype(str))
#%%
def plot_degree_dist(G):
    degrees = [G.degree(n) for n in G.nodes()]
    plt.hist(degrees)
    plt.show()

# %%
nx.write_gml(G,f'{base}/test.gml')
nx.write_gexf(G,f'{base}/test.gexf')
# %%
