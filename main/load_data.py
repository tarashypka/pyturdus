import requests
import sys
from pathlib import Path
from typing import Dict

import pandas as pd
from tqdm import tqdm

sys.path.insert(0, '/home/tas/Workspace/python/pysimple/src')
from pysimple.io import from_tsv, to_tsv, ensure_filedir, ensure_dir


RECORDS_API = 'http://www.xeno-canto.org/api/2/recordings?query=nr:0-10000000&page={page}'
CALLS_API = 'https://www.xeno-canto.org/{call_id}/download'

DATA_DIR = ensure_dir('/mnt/storage/tas/data/xeno-canto')
RECORDS_DIR = ensure_dir(DATA_DIR / 'records')
RECORDS_PATH = RECORDS_DIR / 'records.tsv'
PAGE_RECORDS_PATH = RECORDS_DIR / 'pages' / '{page}.tsv'
GEN_RECORDS_PATH = RECORDS_DIR / 'gens' / '{gen}' / 'records.tsv'
CALLS_DIR = ensure_dir(DATA_DIR / 'calls')
GEN_CALL_PATH = CALLS_DIR / 'gens' / '{gen}' / '{call_id}.mp3'

# Load records from limited number of pages
MAX_PAGES = 2048
# Load records and calls only for most popular species
MAX_GENS = 32
# Load limited number of calls for every specie
MAX_CALLS = 4096
# Load only high quality calls
QUALITY = ['A']


def format_path(path: Path, **kwargs) -> Path:
    """Format placeholders in path"""
    return Path(str(path).format(**kwargs))


def get_records(page: int) -> Dict:
    """Using xeno-canto API get records"""
    return requests.get(RECORDS_API.format(page=page)).json()


def download_call(id: int):
    """Download call from xeno-canto"""
    return requests.get(CALLS_API.format(call_id=id)).content


def load_gens() -> pd.DataFrame:
    """Load records for most popular species"""
    records = from_tsv(RECORDS_PATH, usecols=['q', 'gen', 'id'])
    # Get only best quality records
    records = records[records['q'].isin(QUALITY)]
    # Get only most popular birds
    gens = records['gen'].value_counts().index[:MAX_GENS]
    return records[records['gen'].isin(gens)]


def load_records():
    pages = int(get_records(page=1)['numPages'])
    pages = min(pages, MAX_PAGES)

    print(f'Load records from {pages} pages ...')
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
    print(f'Loaded {len(records)} records!')

    for gen, _ in load_gens().groupby('gen'):
        print(f'Load records for gen {gen} ...')
        gen_records_path = ensure_filedir(format_path(GEN_RECORDS_PATH, gen=gen))
        if gen_records_path.exists():
            continue
        gen_records = records[records['gen'].eq(gen)]
        to_tsv(filepath=gen_records_path, data=gen_records)


def load_calls():
    print(f'Load calls for {MAX_GENS} gens ...')
    for gen, gen_records in load_gens().groupby('gen'):
        gen_record_ids = gen_records['id'].values[:MAX_CALLS]
        print(f'Load {len(gen_record_ids)} calls for gen {gen} ...')
        for call_id in tqdm(gen_record_ids):
            gen_call_path = ensure_filedir(format_path(GEN_CALL_PATH, gen=gen, call_id=call_id))
            if gen_call_path.exists():
                continue
            try:
                call = download_call(id=call_id)
            except Exception as err:
                print(err)
                continue
            else:
                gen_call_path.write_bytes(data=call)


def main():
    load_records()
    load_calls()


if __name__ == '__main__':
    main()
