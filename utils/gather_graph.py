
import pandas as pd
from tqdm.auto import tqdm
from itertools import combinations
import os

def construct():
    mus_nodes = pd.read_csv(f'./data/data_w_spotify.csv')
    mus_edges = []
    label_info = []

    # features to save along with artist info
    feature_cols = ['genres','popularity','followers']

    for vals in tqdm(mus_nodes[['id','name']+feature_cols].values,desc='making song network...'):
        a_id,a_name = vals[:2]
        features = vals[2:]
        f = pd.read_csv(f'./data/artist_songs/{a_id}/features.csv')
        f['owner_id'] = a_id
        f['owner_name'] = a_name
        label_relations = f[['owner_id','owner_name','labelid','label']]
        label_relations = label_relations[(~label_relations.label.isnull()) & (label_relations.label!='[no label]')]
        label_relations[feature_cols] = features
        label_info += label_relations.values.tolist()
        mus_edges+= f[['owner_id','owner_name','id','name','songid','song']].values.tolist()
        
    mus_edges = pd.DataFrame(mus_edges,columns=['id_1','name_1','id_2','name_2','songid','song']).drop_duplicates()
    mus_edges.reset_index(drop=True,inplace=True)

    label_info = pd.DataFrame(label_info,
                    columns=['id','name','labelid','label']+feature_cols).drop_duplicates()
    label_info.reset_index(drop=True,inplace=True)

    if not os.path.exists(f'./data/musician-graph'): 
        os.mkdir(f'./data/musician-graph')
    mus_nodes.to_csv(f'./data/musician-graph/raw_nodes.csv',index=False)
    mus_edges.to_csv(f'./data/musician-graph/raw_edges.csv',index=False)

    label_nodes = label_info[['labelid','label']].drop_duplicates()
    label_nodes.reset_index(drop=True,inplace=True)
    label_edges = []

    for (aid,aname),data in tqdm(label_info.groupby(['id','name']),desc='making label network...'): 
        if aid == 1: continue
        artist_features = data[feature_cols].values[0].tolist()
        for (lid1,lname1),(lid2,lname2) in combinations(data[['labelid','label']].values,2):
            label_edges.append([lid1,lname1,lid2,lname2,aid,aname]+artist_features)

    label_edges = pd.DataFrame(label_edges,
                            columns=['id_1',
                                        'name_1',
                                        'id_2',
                                        'name_2',
                                        'artistid',
                                        'artist']+[f'artist_{f}' for f in feature_cols])

    if not os.path.exists(f'./data/label-graph'): 
        os.mkdir(f'./data/label-graph')
    label_nodes.to_csv(f'./data/label-graph/raw_nodes.csv',index=False)
    label_edges.to_csv(f'./data/label-graph/raw_edges.csv',index=False)