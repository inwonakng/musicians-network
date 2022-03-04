import pandas as pd
import networkx as nx
import numpy as np
from tqdm.auto import tqdm

def musicians():
    print('reading in data...')
    base = f'./data/musician-graph'
    nodes = pd.read_csv(f'{base}/nodes.csv')
    edges = pd.read_csv(f'{base}/edges.csv')

    G = nx.DiGraph()
    G.add_edges_from([[a1,a2]for id1,a1,id2,a2,sid,s in tqdm(edges.values,desc='adding edges to graph..')])


    # add extra features from spotify!
    for feature in ['popularity','followers','genres']:    
        if nodes[feature].dtype == float:
            nodes[feature] = nodes[feature].replace(np.nan,0)
        vals = dict(nodes[['name',feature]].values)
        nx.set_node_attributes(G,vals,feature)

    # print('adding betweenness..')
    # bc = nx.betweenness_centrality(G,normalized=True,endpoints=True)
    # nx.set_node_attributes(G,bc,'betweenness')

    print('adding eigenvector..')
    ec = nx.eigenvector_centrality(G)
    nx.set_node_attributes(G,ec,'eigenvector')

    nx.write_gml(G,f'{base}/graph.gml')
#     nx.write_gexf(G,f'{base}/test.gexf')

def labels(prefix=''):
    if prefix: prefix += '_'
    print('reading in data...')
    base = f'./data/label-graph'
    nodes = pd.read_csv(f'{base}/nodes.csv')
    edges = pd.read_csv(f'{base}/edges.csv')

    G = nx.Graph()
    G.add_edges_from([[n1,n2]for n1,n2 in tqdm(edges[['name_1','name_2']].values,desc='adding edges to graph..')])

    # add extra features from spotify!
    for feature in edges.columns[edges.columns.str.contains('artist')]:    
        if edges[feature].dtype == float:
            edges[feature] = edges[feature].replace(np.nan,0)
        vals = dict(zip(edges[['name_1','name_2']].to_records(index=False).tolist(),edges[feature].values))

        nx.set_edge_attributes(G,vals,feature)
        
    # .... TODO!