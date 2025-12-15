# usefull code
```
def high_corr_pairs(threshold = 1/2):
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
    corr_pairs = corr_matrix.where(mask).stack()
    high_corr_pairs = corr_pairs[corr_pairs.abs() > threshold]
    return high_corr_pairs
```


# folderの役割
- data
    dataを格納する
- model
    modelを格納する
- package
    package


# gensim model
1. model作成
```
import sys
sys.path.append('..')
from package.gensim_model import gensim_model

# modelの名前を指定する
model_name = "word2vec-google-news-300"
model = gensim_model(model_name)
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
    
- presentation slide
    
    https://tusedu-my.sharepoint.com/:p:/r/personal/8723112_ed_tus_ac_jp/_layouts/15/Doc.aspx?sourcedoc=%7B0E304FF3-9737-4C52-AE39-5130F8B5D78D%7D&file=%25u8a00%25u8a9e%25u3068%25u6587%25u5316%25u30d7%25u30ec%25u30bc%25u30f3.pptx&openShare=true&fromShare=true&action=edit&mobileredirect=true