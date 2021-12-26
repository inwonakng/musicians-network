#%% parse the artist relations into a graph relationship

from glob import glob
import pandas as pd
from tqdm import tqdm
import os
import numpy as np
import argparse
from itertools import combinations

round_i = 14
#%%
parser = argparse.ArgumentParser()
parser.add_argument('-r','--round',default=-1)
args = parser.parse_args()

round_i = int(args.round)
# latest mode
if round_i == -1: round_i = len(glob('./data/fromtop1000/SPO_*.csv'))
#%%
MODE = 'fromtop1000'
base = f'./data/{MODE}/artist_songs'


mus_nodes = pd.read_csv(f'./data/{MODE}/SPO_round{round_i}.csv')
mus_edges = []

songs = []
label_info = []

#%%
for a_id,a_name in tqdm(mus_nodes[['id','name']].values,desc='making song network...'):
    f = pd.read_csv(f'{base}/{a_id}/features.csv')
    label_relations = f[['id','name','labelid','label']]
    label_relations = label_relations[~label_relations.label.isnull()]
    label_info += label_relations.values.tolist()
    mus_edges+= f[['id','name','songid','song']].values.tolist()

mus_edges = pd.DataFrame(mus_edges,columns=['id_1','name_1','id_2','name_2','songid','song']).drop_duplicates()
mus_edges.reset_index(drop=True,inplace=True)
label_info = pd.DataFrame(label_info,columns=['id','name','labelid','label']).drop_duplicates()
label_info.reset_index(drop=True,inplace=True)
#%%
label_nodes = label_info[['labelid','label']].drop_duplicates()
label_nodes.reset_index(drop=True,inplace=True)
label_edges = []
for (aid,aname),data in tqdm(label_info.groupby(['id','name']),desc='making label network...'): 
    for (lid1,lname1),(lid2,lname2) in combinations(data[['labelid','label']].values,2):
        label_edges.append([lid1,lname1,lid2,lname2,aid,aname])
label_edges = pd.DataFrame(label_edges,columns=['id_1','name_1','id_2','name_2','artistid','artist'])
#%%
if not os.path.exists(f'./data/{MODE}/musician-graph'): 
    os.mkdir(f'./data/{MODE}/musician-graph')
if not os.path.exists(f'./data/{MODE}/musician-graph/round{round_i}'): 
    os.mkdir(f'./data/{MODE}/musician-graph/round{round_i}')
mus_nodes.to_csv(f'./data/{MODE}/musician-graph/round{round_i}/nodes.csv',index=False)
mus_edges.to_csv(f'./data/{MODE}/musician-graph/round{round_i}/edges.csv',index=False)

# %%
if not os.path.exists(f'./data/{MODE}/label-graph'): 
    os.mkdir(f'./data/{MODE}/label-graph')
if not os.path.exists(f'./data/{MODE}/label-graph/round{round_i}'): 
    os.mkdir(f'./data/{MODE}/label-graph/round{round_i}')
label_nodes.to_csv(f'./data/{MODE}/label-graph/round{round_i}/nodes.csv',index=False)
label_edges.to_csv(f'./data/{MODE}/label-graph/round{round_i}/edges.csv',index=False)


# first establish the node indexes
