#%%
import pandas as pd
from pypika import Query, Tables, Table
import psycopg2
import pandas as pd
import os
import numpy as np
from tqdm.auto import tqdm

#%%
conn = psycopg2.connect(host='localhost',dbname='musicbrainz_db', port=5432, user='musicbrainz', password='musicbrainz')
cur = conn.cursor()
# %%
top1000 = pd.read_csv('data/original_top_1000.csv')

#%%
artist,artist_credit_name,release_group,release,release_label,label = Tables('artist','artist_credit_name','release_group','release','release_label','label')

#%%
final = pd.read_csv('data/crawl_data/round18.csv')
# %%
count = 0
for id in tqdm(final.id.values):
    feats = pd.read_csv(f'data/artist_songs/{final.id.values[0]}/features.csv')
    count += len(feats)
# %%

final = pd.read_csv('data/data_w_spotify.csv')
count = 0
for id in tqdm(final.id.values):
    feats = pd.read_csv(f'data/artist_songs/{final.id.values[0]}/features.csv')
    count += len(feats)
    
print(f'artists: {len(final)} releases: {count}')