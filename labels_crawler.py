#%%
from wikidata_search import wikisearch
import pandas as pd
import argparse
from tqdm import tqdm

round_i = 1


# %%
parser = argparse.ArgumentParser()
parser.add_argument('-r','--round',default=1)
args = parser.parse_args()
round_i = int(args.round)
#%%
labels = []
ids = pd.read_csv(f'./data/fromtop1000/round{round_i}.csv')
for i in tqdm(ids.gid.values):
    labels.append(wikisearch(i))
# %%
