# %%
import pandas as pd
import json
import psycopg2
from tqdm import tqdm

round_i = 1

conn = psycopg2.connect(host='localhost',dbname='musicbrainz_db', port=5432, user='musicbrainz', password='musicbrainz')
cur = conn.cursor()
# %%
