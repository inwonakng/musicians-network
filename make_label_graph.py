#%% 
import pandas as pd
import networkx as nx
import numpy as np
from tqdm import tqdm
from spotify_id import get_spotify_id
import argparse
from glob import glob

round_i = 1
#%%
parser = argparse.ArgumentParser()
parser.add_argument('-r','--round',default=-1)
args = parser.parse_args()
round_i = int(args.round)
# latest mode
if round_i == -1: round_i = len(glob('./data/fromtop1000/SPO_*.csv'))

# %%
print('reading in data...')
base = f'./data/fromtop1000/label-graph/round{round_i}'
nodes = pd.read_csv(f'{base}/nodes.csv')
edges = pd.read_csv(f'{base}/edges.csv')

# %%
G = nx.Graph()
G.add_edges_from([[n1,id2]for id1,n1,id2,n2,aid,a in tqdm(edges.values,desc='adding edges to graph..')])

# %%
nx.write_gml(G,f'{base}/test.gml')
nx.write_gexf(G,f'{base}/test.gexf')
# %%
