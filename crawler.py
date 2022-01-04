#%%
from docker_query import get_features
import argparse
import pandas as pd
from tqdm import tqdm
from spotify_id import get_spotify_id,get_spotify_data

round_i = 1
#%%
parser = argparse.ArgumentParser()
parser.add_argument('-r','--round',default=1)
args = parser.parse_args()

round_i = int(args.round)

#%%
ids = pd.read_csv(f'./data/crawl_data/round{round_i-1}.csv')
newids = ids[['id','name']]
for id,name,_,_ in tqdm(ids[~ids.isdone].values,desc='querying database...'):
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
newids = get_spotify_id(newids,round_i)
newids.to_csv(f'./data/round{round_i}.csv',index=False)

#%%

# We'll just run this once later to gather all the data at once
just_spotify = get_spotify_data(newids,round_i)
# %%
