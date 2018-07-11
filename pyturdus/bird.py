import os

import numpy as np
import pandas as pd
import seaborn as sb
import librosa as lr
import librosa.display
import matplotlib.pyplot as plt


class Bird:
    def __init__(self, id: int, name: str, country: str = None, quality: str = None):
        self.id = id
        self.name = name
        self.country = country
        self.quality = quality

        self.waveform_: np.array = None
        self.sample_rate_: int = None

    def passport(self) -> str:
        return f'{self.name} from {self.country}'

    def load_call(self, callpath: os.PathLike, **kwargs):
        kwargs.setdefault('sr', None)
        self.waveform_, self.sample_rate_ = lr.load(callpath, **kwargs)

    def plot_waveform(self):
        wf = pd.Series(self.waveform_)
        wf.index = wf.index / self.sample_rate_
        sb.set()
        sb.set_style('darkgrid')
        plt.figure(figsize=(12, 4))
        wf.plot()
        plt.xticks(size=10)
        plt.yticks(size=10)
        plt.xlabel('sec', weight='bold', size=13)
        plt.ylabel('dB', weight='bold', size=13)
        plt.title(f'Waveform of {self.passport()}', style='italic', size=14)
        plt.tight_layout()
        plt.show()

    def plot_spectrogram(self):
        sg = lr.feature.melspectrogram(y=self.waveform_, sr=self.sample_rate_)
        sg = lr.power_to_db(sg, ref=np.max)
        sb.set()
        sb.set_style('darkgrid')
        plt.figure(figsize=(12, 4))
        librosa.display.specshow(sg, sr=self.sample_rate_, x_axis='time', y_axis='mel')
        plt.xlabel('sec', weight='bold', size=13)
        plt.ylabel('Hz', weight='bold', size=13)
        plt.title(f'Spectrogram of {self.passport()}', style='italic', size=14)
        plt.colorbar(format='%+02.0f dB')
        plt.tight_layout()
        plt.show()
