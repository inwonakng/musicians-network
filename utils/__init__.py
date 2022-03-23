
from utils.spotify_id import get_spotify_data
from utils.docker_query import get_features
from utils.spotify_id import get_spotify_id
from utils.get_release_trends import get_release_trends
from utils.gather_graph import construct
from utils import make_graph

import json
from glob import glob
import pandas as pd
from tqdm import tqdm
import os
from itertools import combinations
import networkx as nx
from ast import literal_eval
'''
THIS FUNCTION SHOULD ONLY BE RAN AFTER THE CRAWLER HAS CONVERGED
'''

CRAWL_FINAL = 'final.csv'
CRAWL_START = './crawl_start.csv'
CACHE_DIR = './data/cache'

class MusicDataLoader:
    def __init__(self,crawl_start=CRAWL_START,crawl_final=CRAWL_FINAL,cache=CACHE_DIR):
        self.cache_dir = cache
        self.crawl_start = crawl_start
        self.crawl_final = f'{self.cache_dir}/crawl_data/{crawl_final}'
        # print(self.crawl_final)
        self.load()
        pass

    def load(self):
        if not os.path.exists(self.crawl_final):
            self.crawl_db()
        return pd.read_csv(self.crawl_final)
        

    def crawl_spotify(self):
        filename = f'{self.cache_dir}/crawl_data/data_w_spotify.csv'       
        if not os.path.exists(filename):
            # first locate the latest crawl
            latest_data = pd.read_csv(CRAWL_FINAL)

            spo_data = get_spotify_data(latest_data)
            spo_data = spo_data.rename(columns={'followers.total':'followers'})

            spo_data.to_csv(filename,index=False)
        
        construct(filename,
                  './data/musician-graph'
                  './data/label-graph',
                  )

    #%%
    '''
    Must provide original file to start crawling from
    '''

    def crawl_db(self):
        if not os.path.exists(f'{self.cache_dir}/crawl_data'):
            os.makedirs(f'{self.cache_dir}/crawl_data')
        while True:
            latest = sorted(glob(f'{self.cache_dir}crawl_data/*.csv'))
            if latest: 
                latest = latest[-1]
                round_i = int(latest.split('/')[-1].split('.')[0]) + 1
            else: 
                latest = self.crawl_start
                round_i = 0
            ids = pd.read_csv(latest)
            newids = ids[['id','name']]
            
            if ids[~ids.isdone].empty: break
            
            
            for id,name,_,_ in tqdm(ids[~ids.isdone].values,desc=f'round {round_i}...'):
                features = get_features(id)
                newids = newids.append(
                            features[['id','name']]
                        ).drop_duplicates(
                            subset='id'
                        ).reset_index(drop=True)
                features.to_csv(
                    f'./data/artist_songs/{id}/features.csv',
                    index=False)

            newids = newids.drop_duplicates(subset='id').reset_index(drop=True)
            newids['isdone'] = [i in ids.id.values for i in newids.id.values]
            newids = get_spotify_id(newids)
            newids.to_csv(f'{self.cache_dir}/crawl_data/{round_i:04}.csv',index=False)

        for p in glob(f'{self.cache_dir}/crawl_data/*.csv'): os.remove(p)
        
        newids.to_csv(CRAWL_FINAL,index=False)
        # finally return spotify data
        self.crawl_spotify()
        # building rudimentary network first


    def release_trends(self,n_bins = 100):
        # grabbing us only data
        get_release_trends(n_bins=n_bins)

    def music_graph(self,n_bins=100):
        make_graph.musicians(n_bins)
        

    def get_features(self,n_release_bins=100):
        self.release_trends(n_release_bins)
        self.music_graph(n_release_bins)
        cachedir = f'data/feature_corel_{n_release_bins}.csv'
        if not os.path.exists(cachedir):
            mus_nodes = pd.read_csv(f'./data/musician-graph/nodes_{n_release_bins}.csv',
                                    converters={'genres':literal_eval}
                                    )
            # mus_edges = pd.read_csv('./data/musician-graph/edges.csv')
            # lab_nodes = pd.read_csv('./data/label-graph/nodes.csv')
            # lab_edges = pd.read_csv('./data/label-graph/edges.csv')

            mus_G = nx.read_gml(f'data/musician-graph/graph_{n_release_bins}.gml')
            
            mus_nodes['network_rank'] = mus_nodes.name.map(nx.get_node_attributes(mus_G,'eigenvector'))
            mus_nodes['in_edges'] = mus_nodes.name.map(lambda n: len(mus_G.in_edges(n)))
            mus_nodes['out_edges'] = mus_nodes.name.map(lambda n: len(mus_G.out_edges(n)))

            mus_nodes = mus_nodes[(~mus_nodes.followers.isnull()) & (~mus_nodes.popularity.isnull())]
            mus_nodes.to_csv(cachedir,index=False)
            # lab_G = nx.read_gml('data/label-graph/test.gml')
        else:
            mus_nodes = pd.read_csv(cachedir,converters={'genres':literal_eval})
        
        return mus_nodes
