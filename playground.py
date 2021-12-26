# %%

import pandas as pd
base = 'https://musicbrainz.org/ws/2/'
import os 
from data.collection import *
import multiprocessing
from pathvalidate import sanitize_filepath
from glob import glob
import argparse

MODE = 'fromtop1000'
round_i = 1
#%%

parser = argparse.ArgumentParser(description='run a round of gathering data from given list')
parser.add_argument('-r','--round',type=int,default=1)
parser.add_argument('-m','--mode',type=str,default='top')

args = parser.parse_args()


if args.mode != 'top': MODE = 'SOMETHING'
round_i = args.round
# %%
top1000artists = pd.read_json(f'./data/{MODE}/seed.json')
idfile = f'./data/{MODE}/round{round_i-1}.csv'
if not os.path.exists(idfile):
    ids,trys = get_artist_ids(top1000artists)
    # examine mismatches
    ids[(ids.original_name!=ids.name) | (ids.name_match < 0)].to_csv(idfile,index=False)
    ids.to_csv(idfile,index=False)
else:
    ids = pd.read_csv(idfile)

if len(ids.columns) > 2:
    c = ids.columns
    df1 = ids[c[:2]].dropna().rename(columns=dict(zip(c[:2],['artist_id','artist'])))
    df2 = ids[c[2:4]].dropna().rename(columns=dict(zip(c[2:4],['artist_id','artist'])))
    df3 = ids[c[4:]].dropna().rename(columns=dict(zip(c[4:],['artist_id','artist'])))
    ids = pd.concat([df1,df2,df3])
#%%
testid = '89aa5ecb-59ad-46f5-b3eb-2d424e941f19'
release_id = 'eb68ecd6-fb1e-483a-9cda-b595fb4664a7'
songbase = f'./data/{MODE}/artist-songs'
graphbase = f'./data/{MODE}/graph'
# %%
if not os.path.exists(songbase): os.mkdir(songbase)
if not os.path.exists(graphbase): os.mkdir(graphbase)

def crawl_artist(arr):
    id,name = arr
    name = name.replace('/','')

    if os.path.exists(f'{songbase}/{name}/song-rels.csv'): return
    print(f'{arr} -- {len(glob(f"{songbase}/*"))}/{len(ids)}')

    songs = artist_songs(id)
    if not songs: return
    if not os.path.exists(f'{songbase}/{name}'): os.mkdir(f'{songbase}/{name}')

    songs.to_csv(f'{songbase}/{name}/song-rels.csv')

    features = songs[['artist_id','artist']].drop_duplicates()
    features.to_csv(f'{songbase}/{name}/features.csv')
    sleep(0.5)

def update_known(oldids):
    for new in glob(f'{songbase}/*/features.csv'):
        df = pd.read_csv(new)[oldids.columns]
        oldids = pd.concat([oldids,df])
        if len(oldids.columns) > 2: 
            print("something screwed up!")
            return None
    return oldids

p = multiprocessing.Pool(10)
p.map(crawl_artist,ids.values.tolist())
p.close()

# %%
newids = update_known(ids)
newids.to_csv(f'./data/{MODE}/round{round_i}.csv',index=False)

# %%
