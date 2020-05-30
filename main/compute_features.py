import os
from pathlib import Path

import librosa
import numpy as np
from tqdm import tqdm

from pysimple.io import from_tsv, dump_pickle


N_FFT = 2048
HOP_LENGTH = 512

birds_path = Path(os.environ['DATA_DIR']) / 'birds' / 'birds.tsv'
birds = from_tsv(birds_path)
birds['gen_sp'] = birds['gen'] + '_' + birds['sp']
birds = birds.drop(columns=['gen', 'sp'])

records_path = Path(os.environ['DATA_DIR']) / 'records' / 'records.tsv'
records = from_tsv(records_path, usecols=['id', 'gen', 'sp'])
records['gen_sp'] = records['gen'].str.lower() + '_' + records['sp'].str.lower()
records = records.drop(columns=['gen', 'sp'])
records = records.merge(birds, how='inner', on=['gen_sp'])

calls_dir = Path(os.environ['DATA_DIR']) / 'calls'
features_dir = Path(os.environ['DATA_DIR']) / 'features'

for i, (bird, bird_records) in enumerate(records.groupby('gen_sp')):
    print(f'There are {len(bird_records)} records for bird "{bird}"')

    S_mean = []
    S_std = []

    if (features_dir / bird).exists():
        print('Skip since already computed ...')
        continue

    for _, record in tqdm(list(bird_records.iterrows())):
        record_id = record['id']
        call_path = calls_dir / bird / f'{record_id}.wav'

        try:
            call, sr = librosa.load(call_path, sr=44100)
        except FileNotFoundError:
            continue

        # Trim silent edges
        call, _ = librosa.effects.trim(call)

        # Compute FFT
        S = np.abs(librosa.stft(call, n_fft=N_FFT, hop_length=HOP_LENGTH))

        S_mean.append(S.mean(axis=1).tolist())
        S_std.append(S.std(axis=1).tolist())

    S_mean = np.array(S_mean)
    S_std = np.array(S_std)

    dump_pickle(filepath=features_dir / bird / 'S_mean.bin', obj=S_mean)
    dump_pickle(filepath=features_dir / bird / 'S_std.bin', obj=S_std)
