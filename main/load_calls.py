import io
import os
import requests
from pathlib import Path

from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from tqdm import tqdm

from pysimple.io import from_tsv, ensure_filedir, ensure_dir, format_path


CALLS_API = 'https://www.xeno-canto.org/{call_id}/download'

DATA_DIR = ensure_dir(os.environ['DATA_DIR'])
BIRDS_PATH = DATA_DIR / 'birds' / 'birds.tsv'
RECORDS_PATH = DATA_DIR / 'records' / 'records.tsv'
CALL_PATH = DATA_DIR / 'calls' / '{gen_sp}' / '{call_id}.wav'


def download_call(id: int) -> bytes:
    """Download bird call data from xeno-canto"""
    return requests.get(CALLS_API.format(call_id=id)).content


def save_call(filepath: Path, data: bytes) -> None:
    """Save call into file in WAV format"""
    with io.BytesIO(data) as f:
        try:
            sound = AudioSegment.from_mp3(f)
        except CouldntDecodeError:
            return
        else:
            sound.export(filepath, format='wav')


def load_calls():
    """
    Download bird calls from xeno-canto for local birds.
    Download only new data, while keeping previously downloaded.
    """

    birds = from_tsv(BIRDS_PATH, usecols=['gen', 'sp'])
    birds['gen_sp'] = birds['gen'].str.lower() + '_' + birds['sp'].str.lower()

    records = from_tsv(RECORDS_PATH, usecols=['gen', 'sp', 'id'])
    records['gen_sp'] = records['gen'].str.lower() + '_' + records['sp'].str.lower()
    records = records[records['gen_sp'].isin(birds['gen_sp'])]

    print(f'Load calls for {len(birds)} species ...')
    for gen_sp, gen_records in records.groupby('gen_sp'):
        print(f'Load {len(gen_records)} bird calls for bird {gen_sp} ...')
        for call_id in tqdm(gen_records['id']):
            call_path = ensure_filedir(format_path(CALL_PATH, gen_sp=gen_sp, call_id=call_id))
            if call_path.exists():
                continue
            try:
                call = download_call(id=call_id)
            except Exception as err:
                print(err)
                continue
            else:
                save_call(filepath=call_path, data=call)


def main():
    load_calls()


if __name__ == '__main__':
    main()
