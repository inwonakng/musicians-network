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
'''
THIS FUNCTION SHOULD ONLY BE RAN AFTER THE CRAWLER HAS CONVERGED
'''

def crawl_spotify():
    # first locate the latest crawl
    latest = len(glob('data/crawl_data/round*.csv'))-1
    latest_data = pd.read_csv(f'data/crawl_data/round{latest}.csv')

    spo_data = get_spotify_data(latest_data)
    spo_data = spo_data.rename(columns={'followers.total':'followers'})

    spo_data.to_csv('data/data_w_spotify.csv',index=False)


#%%
'''
Must provide original file to start crawling from
'''

def crawl_db(start_file):
    while True:
    
        latest = sorted(glob(f'./data/crawl_data/*.csv'))
        if latest: 
            latest = latest[-1]
            round_i = int(latest.split('/')[-1].split('.')[0])
        else: 
            latest = start_file
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
        newids.to_csv(f'./data/crawl_data/round{round_i}.csv',index=False)

    # finally return spotify data
    crawl_spotify()

    # building rudimentary network first
    construct()
    
    # grabbing us only data
    get_release_trends(prefix='us_release')
    
    make_graph.musicians(prefix='us_release')
    
    

