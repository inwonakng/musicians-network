#%%
import pandas as pd
from pypika import Query, Tables, Table
import psycopg2
import pandas as pd
import os
import numpy as np

#%%
conn = psycopg2.connect(host='localhost',dbname='musicbrainz_db', port=5432, user='musicbrainz', password='musicbrainz')
cur = conn.cursor()
# %%
top1000 = pd.read_csv('data/original_top_1000.csv')

#%%
artist,artist_credit_name,release_group,release,release_label,label = Tables('artist','artist_credit_name','release_group','release','release_label','label')

