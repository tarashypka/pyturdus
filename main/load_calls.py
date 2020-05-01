import requests

import pandas as pd
from tqdm import tqdm

from pysimple.io import from_tsv, to_tsv, ensure_filedir, ensure_dir, format_path


CALLS_API = 'https://www.xeno-canto.org/{call_id}/download'

DATA_DIR = ensure_dir('/mnt/storage/tas/data/xeno-canto')
RECORDS_DIR = ensure_dir(DATA_DIR / 'records')
RECORDS_PATH = RECORDS_DIR / 'records.tsv'
GEN_RECORDS_PATH = RECORDS_DIR / 'gens' / '{gen}' / 'records.tsv'
CALLS_DIR = ensure_dir(DATA_DIR / 'calls')
GEN_CALL_PATH = CALLS_DIR / 'gens' / '{gen}' / '{call_id}.mp3'

# Load records and calls only for most popular species
MAX_GENS = 32
# Load limited number of calls for every specie
MAX_CALLS = 4096
# Load only high quality calls
QUALITY = ['A']


def download_call(id: int):
    """Download bird call data from xeno-canto"""
    return requests.get(CALLS_API.format(call_id=id)).content


def load_gens() -> pd.DataFrame:
    """Load records for most popular species that were previously downloaded from xeno-canto API"""
    records = from_tsv(RECORDS_PATH, usecols=['q', 'gen', 'id'])
    # Get only best quality records
    records = records[records['q'].isin(QUALITY)]
    # Get only most popular birds
    gens = records['gen'].value_counts().index[:MAX_GENS]
    return records[records['gen'].isin(gens)]


def load_calls():
    """
    Download bird calls from xeno-canto for most popular species.
    Download only new data, while keeping previously downloaded.
    """

    print('Split loaded records into most popular species ...')
    for gen, gen_records in load_gens().groupby('gen'):
        gen_records_path = ensure_filedir(format_path(GEN_RECORDS_PATH, gen=gen))
        if gen_records_path.exists():
            continue
        to_tsv(filepath=gen_records_path, data=gen_records)

    print(f'Load calls for {MAX_GENS} gens ...')
    for gen, gen_records in load_gens().groupby('gen'):
        gen_record_ids = gen_records['id'].values[:MAX_CALLS]
        print(f'Load {len(gen_record_ids)} bird calls for specie {gen} ...')
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
    load_calls()


if __name__ == '__main__':
    main()
