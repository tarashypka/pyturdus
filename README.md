# rubecula

Recognize local birds from their calls

![erithacus rubecula](https://github.com/tarashypka/rubecula/blob/master/rubecula.png?raw=true)

## Data

Bird records and calls are taken from [xeno-canto](https://www.xeno-canto.org/)

## Structure

- Data loaders
  - [Records loader](https://github.com/tarashypka/rubecula/blob/master/main/load_records.py)
  - [Calls loader](https://github.com/tarashypka/rubecula/blob/master/main/load_calls.py)
- Notebooks
  - [Records analysis](https://github.com/tarashypka/rubecula/blob/master/ipynb/analyze_records.ipynb)
  - [Local birds](https://github.com/tarashypka/rubecula/blob/master/ipynb/local_birds.ipynb)
  
## Reproduce

```
$ bash install.sh --env=/path/to/python/env
$ source activate env
$ python main/load_records.py
$ python main/load_calls.py
```

## References

- [Who's singing? Automatic bird sound recognition with machine learning - Dan Stowell](https://www.youtube.com/watch?v=pzmdOETnhI0)
- [Птахи Києва та Київщини](http://www.dom-prirody.com.ua/priroda-kieva/ptahi)
