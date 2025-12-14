# gensim model
1. model作成
```
import sys
sys.path.append('..')
from package.gensim_model import gensim_model

# 辞書の名前を指定する
dictionary = "word2vec-google-news-300"
model = gensim_model(dictionary)
```

- vector取得
```
locale = "en_US"
model.get_locale_vector(locale)
```
- 相関行列取得
```
locale = "en_US"
model.get_locale_corr(locale)
```
- heatmap取得
```
locale = "en_US"
model.show_locale_heatmap(locale)
```

- 中国語対応
```
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Noto Sans CJK SC', 'Arial Unicode MS']
```

# country name
localeを指定して対応する言語と地域のdataを追加することができる
```
import sys
sys.path.append('..')
from package.country_name import ETL_country_name, ETL_country_code, ETL_babel, ETL_pycountry

ETL_pycountry()
ETL_country_code()
en_US_series = ETL_babel("en_US")
en_UK_series = ETL_babel("en_UK")
zh_CN_series = ETL_babel("zh_CN")
zh_TW_series = ETL_babel("zh_TW")
ETL_country_name()
```

- get locale list
```
from babel import localedata
all_locales = localedata.locale_identifiers()
all_locales
```

# link
- google ngram
    https://books.google.com/ngrams/

- English Corpora
    https://www.english-corpora.org/

- MICASE
    https://quod.lib.umich.edu/cgi/c/corpus/corpus?c=micase;page=simple

- corpus
    https://app.sketchengine.eu/#open