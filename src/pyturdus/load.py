import requests
import sys
from typing import Dict, List

import pandas as pd

sys.path.insert(0, '/home/tas/Workspace/python/pysimple')
from pysimple.io import from_tsv, to_tsv, ensure_filedir, ensure_dir


XC_API = 'http://www.xeno-canto.org/api/2/recordings?query=nr:0-10000000&page={page}'
DATA_DIR = ensure_dir('/mnt/storage/tas/data/xeno-canto')
RECORDS_DIR = ensure_dir(DATA_DIR / 'records')
CALLS_DIR = ensure_dir(DATA_DIR / 'calls')
PAGE_RECORDS_PATH = RECORDS_DIR / 'pages' / '{page}.tsv'
ALL_RECORDS_PATH = RECORDS_DIR / 'records.tsv'
GEN_RECORDS_PATH = RECORDS_DIR / 'gens' / '{gen}' / 'records.tsv'
CALL_URL = 'https://www.xeno-canto.org/{call_id}/download'
GEN_CALL_PATH = CALLS_DIR / 'gens' / '{gen}' / '{call_id}.mp3'
QUALITY = ['A']
MAX_PAGES = 1024
MAX_GENS = 32
MAX_CALLS = 4096


def get_records(page: int) -> Dict:
    return requests.get(XC_API.format(page=page)).json()


def get_call(id: int):
    return requests.get(CALL_URL.format(call_id=id)).content


def load_gens() -> pd.DataFrame:
    """Load records for most popular species"""
    rr = from_tsv(ALL_RECORDS_PATH, usecols=['q', 'gen', 'id'])
    # Get only best quality records
    rr = rr[rr['q'].isin(QUALITY)]
    # Get only most popular birds
    gens = rr['gen'].value_counts().index[:MAX_GENS]
    return rr[rr['gen'].isin(gens)]


def load_records():
    pages = int(get_records(page=1)['numPages'])
    pages = min(pages, MAX_PAGES)

    print(f'Load records from {pages} pages ...')
    records = []
    for page in range(1, pages+1):
        print(f'Load records from page {page} ...')
        page_records_path = ensure_filedir(str(PAGE_RECORDS_PATH).format(page=page))
        if page_records_path.exists():
            rr = from_tsv(page_records_path)
        else:
            try:
                rr = pd.DataFrame(get_records(page=page)['recordings'])
            except Exception as err:
                print(err)
                continue
            else:
                to_tsv(filepath=page_records_path, data=rr)
        records.append(rr)
    records = pd.concat(records)
    to_tsv(ALL_RECORDS_PATH, data=records)
    print(f'Loaded {len(records)} records!')

    for gen, _ in load_gens().groupby('gen'):
        print(f'Load records for gen {gen} ...')
        gen_records_path = ensure_filedir(str(GEN_RECORDS_PATH).format(gen=gen))
        if gen_records_path.exists():
            continue
        gen_records = records[records['gen'].eq(gen)]
        to_tsv(filepath=gen_records_path, data=gen_records)


def load_calls():
    print(f'Load calls for {MAX_GENS} gens ...')
    for gen, gen_records in load_gens().groupby('gen'):
        gen_record_ids = gen_records['id'].values[:MAX_CALLS]
        print(f'Load {len(gen_record_ids)} calls for gen {gen} ...')
        for call_id in gen_record_ids:
            gen_call_path = ensure_filedir(str(GEN_CALL_PATH).format(gen=gen, call_id=call_id))
            if gen_call_path.exists():
                continue
            try:
                c = get_call(id=call_id)
            except Exception as err:
                print(err)
                continue
            else:
                gen_call_path.write_bytes(data=c)


def main():
    load_records()
    load_calls()


if __name__ == '__main__':
    main()
