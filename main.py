#%%

from utils import get_relaease_genres
#%%

import argparse

OPERATIONS = {
    'get_release_trends':get_release_trends
}

parser = argparse.ArgumentParser()
parser.add_argument('operation',action='store')