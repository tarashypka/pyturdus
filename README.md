# rubecula

Recognize local birds from their calls

![erithacus rubecula](https://github.com/tarashypka/rubecula/blob/master/rubecula.png?raw=true)

## Data

Bird records and calls are taken from [xeno-canto](https://www.xeno-canto.org/)

## Structure

- Data loaders
  - [Records loader](https://github.com/tarashypka/rubecula/blob/master/main/load_records.py)
  - [Calls loader](https://github.com/tarashypka/rubecula/blob/master/main/load_calls.py)
- Features
  - [Frequency stats](https://github.com/tarashypka/rubecula/blob/master/main/compute_stats.py)
- Notebooks
  - [Records analysis](https://github.com/tarashypka/rubecula/blob/master/ipynb/analyze_records.ipynb)
  - [Local birds](https://github.com/tarashypka/rubecula/blob/master/ipynb/local_birds.ipynb)
  - [Spectrograms](https://github.com/tarashypka/rubecula/blob/master/ipynb/spectrograms.ipynb)
  - [Bird frequencies](https://github.com/tarashypka/rubecula/blob/master/ipynb/bird_frequencies.ipynb)
  - [Frequency stats](https://github.com/tarashypka/rubecula/blob/master/ipynb/frequency_stats.ipynb)
  
## Reproduce

```
$ bash install.sh --env=/path/to/python/env
$ source activate env
$ export DATA_DIR=/path/to/data
$ python main/load_records.py
$ python main/load_calls.py
$ python main/compute_stats.py
```

## References

- [Who's singing? Automatic bird sound recognition with machine learning - Dan Stowell](https://www.youtube.com/watch?v=pzmdOETnhI0)
- [Two Types of Communication Between Birds: Understanding Bird Language Songs And Calls](https://www.youtube.com/watch?v=4_1zIwEENt8)
- [Bird identification Apps: Q&A with Mario Lasseck](https://www.xeno-canto.org/article/250)
- [Getting to Know the Mel Spectrogram](https://towardsdatascience.com/getting-to-know-the-mel-spectrogram-31bca3e2d9d0)
- [Птахи Києва та Київщини](http://www.dom-prirody.com.ua/priroda-kieva/ptahi)
