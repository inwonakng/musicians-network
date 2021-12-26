#%% 
import pandas as pd
import networkx as nx
import numpy as np
from tqdm import tqdm
from spotify_id import get_spotify_id
import argparse
from glob import glob

round_i = 14
#%%
parser = argparse.ArgumentParser()
parser.add_argument('-r','--round',default=-1)
args = parser.parse_args()
round_i = int(args.round)
#%%
# print('reading in data...')
# LABELS_GRAPH = f'./data/fromtop1000/label-graph/round{round_i}'
# nx.read_gml(f'{LABELS_GRAPH}/test.gml')
# %%
print('reading in label data...')
LAB_FOLDER = f'./data/fromtop1000/label-graph/round{round_i}'
nodes = pd.read_csv(f'{LAB_FOLDER}/nodes.csv')
edges = pd.read_csv(f'{LAB_FOLDER}/edges.csv')

# %%
LAB_G = nx.Graph()
LAB_G.add_edges_from([[id1,id2]for id1,n1,id2,n2,aid,a in tqdm(edges.values,desc='adding edges to graph..')])

# %%
print('reading in musician data...')
MUS_FOLDER = f'./data/fromtop1000/musician-graph/round{round_i}'
nodes = pd.read_csv(f'{MUS_FOLDER}/nodes.csv')
edges = pd.read_csv(f'{MUS_FOLDER}/edges.csv')

# %%
MUS_G = nx.DiGraph()
MUS_G.add_edges_from([[id1,id2]for id1,a1,id2,a2,sid,s in tqdm(edges.values,desc='adding edges to graph..')])

# %%
