#%%

from utils import crawl_db
#%%

import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_crawl = subparsers.add_parser('crawl_db',help='craw the database')
parser_crawl.set_defaults(func=crawl_db)
parser.add_argument('operation',action='store')


operation = parser.parse_args()
operation.func()