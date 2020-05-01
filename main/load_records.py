import requests
from typing import Dict

import pandas as pd
from tqdm import tqdm

from pysimple.io import from_tsv, to_tsv, ensure_filedir, ensure_dir, format_path


RECORDS_API = 'http://www.xeno-canto.org/api/2/recordings?query=nr:0-10000000&page={page}'

DATA_DIR = ensure_dir('/mnt/storage/tas/data/xeno-canto')
RECORDS_DIR = ensure_dir(DATA_DIR / 'records')
RECORDS_PATH = RECORDS_DIR / 'records.tsv'
PAGE_RECORDS_PATH = RECORDS_DIR / 'pages' / '{page}.tsv'

# Load records from limited number of pages
MAX_PAGES = 2048


def get_records(page: int) -> Dict:
    """Get bird record data from xeno-canto API"""
    return requests.get(RECORDS_API.format(page=page)).json()


def load_records():
    """
    Download bird records data from xeno-canto API.
    Download only new data, while keeping previously downloaded.
    """
    pages = int(get_records(page=1)['numPages'])
    pages = min(pages, MAX_PAGES)

    print(f'Load bird records from {pages} pages at xeno-canto ...')
    records = []
    for page in tqdm(range(1, pages+1)):
        page_records_path = ensure_filedir(format_path(PAGE_RECORDS_PATH, page=page))
        if page_records_path.exists():
            page_records = from_tsv(page_records_path)
        else:
            try:
                page_records = pd.DataFrame(get_records(page=page)['recordings'])
            except Exception as err:
                print(err)
                continue
            else:
                to_tsv(filepath=page_records_path, data=page_records)
        records.append(page_records)
    records = pd.concat(records)
    to_tsv(RECORDS_PATH, data=records)
    records = from_tsv(filepath=RECORDS_PATH)
    print(f'Loaded {len(records)} bird records!')


def main():
    load_records()


if __name__ == '__main__':
    main()
