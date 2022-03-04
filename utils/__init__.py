import json
from utils.spotify_id import get_spotify_data
from glob import glob
import pandas as pd

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


def test():
    json.dump({'test':'hi'},open('./data/test.json','w'))