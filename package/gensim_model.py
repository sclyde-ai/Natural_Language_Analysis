import gensim.downloader as api
import pandas as pd
import numpy as np
import os
import sys
import seaborn as sns
from functools import partial
import tensorflow as tf
from pathlib import Path
sys.path.append('..')
from country_name import get_babel, get_country_name

current_file = Path(__file__)
current_dir = Path(__file__).parent
parent_dir = Path(__file__).parent.parent
data_dir = parent_dir / Path(f"data")

class gensim_model:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.dict_path = data_dir / Path(self.dictionary)
        if not os.path.exists(self.dict_path):
            os.mkdir(self.dict_path)
        self.model = api.load(dictionary)
        self.index = self.get_index()
        print("init complete!")

    def get_model(self):
        return self.model

    def ETL_index(self):
        index = self.model.index_to_key
        index_series = pd.Series(index)
        index_path = self.dict_path / Path("index.csv")
        index_series.to_csv(index_path)
        return index_series

    def ETL_similar(self, word):
        similar_path = self.dict_path / Path("similar")
        if not os.path.exists(similar_path):
            os.mkdir(similar_path)
        
        similar = self.model.most_similar(word, topn=None)
        df = pd.Series(similar, index=self.index, name=word)

        csv_path = similar_path / Path(f"{word}.csv")
        df.to_csv(csv_path)
        return df

    def ETL_vector(self, word) -> pd.DataFrame:
        vector_path = self.dict_path / Path("vector")
        if not os.path.exists(vector_path):
            os.mkdir(vector_path)
        vector = self.model.get_vector(word)
        df = pd.Series(vector, name=word)
        csv_path = vector_path / Path(f"{word}.csv")
        df.to_csv(csv_path)
        return df
    
    def get_csv(self, ETL_func, csv_path):
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path, index_col=0)
        else:
            df = ETL_func()
        return df
    
    def get_index(self):
        csv_path = self.dict_path / Path("index.csv")
        df = self.get_csv(self.ETL_index, csv_path)
        return df
    
    def get_similar(self, word):
        csv_path = self.dict_path / Path(f"similar/{word}.csv")
        df = self.get_csv(self.ETL_similar, csv_path)
        return df

    def get_vector(self, word):
        csv_path = self.dict_path / Path(f"vector/{word}.csv")
        ETL_func = partial(self.ETL_vector, word)
        df = self.get_csv(ETL_func, csv_path)
        return df
    
    def get_locale_vector(self, locale):
        series = get_babel(locale)
        vector_list = []
        size = self.model.vector_size
        for word in series[locale]:
            if word in self.model:
                vector_list.append(self.get_vector(word))
            else:
                vector_list.append(pd.Series(np.full((size, ), np.nan), name=word))
        df = pd.concat(vector_list, axis=1)
        return df
    
    def get_locale_corr(self, locale):
        df = self.get_locale_vector(locale)
        return df

    def show_locale_heatmap(self, locale):
        df = self.get_locale_corr(locale)
        sns.heatmap(df.corr())

    def get_all_locale(self, locale_func):
        country_name_df = get_country_name()
        locales = country_name_df.drop(['alpha_2', "alpha_3"], axis=1).columns
        df_list = []
        for locale in locales:
            df = locale_func(locale)
            babel_df = get_babel(locale)
            outliner_df = babel_df[babel_df.index=='CQ']
            if not outliner_df.empty:
                outliner = outliner_df.iloc[0, 0]
                df = df.drop(columns=outliner)
            df_list.append(df.values)
        tensor = tf.stack(df_list)
        return tensor
    
    def get_all_locale_tensor(self):
        tensor = self.get_all_locale(self.get_locale_vector)
        return tensor
    
if __name__ == "__main__":
    model = gensim_model("word2vec-google-news-300")
    print(model.get_all_locale_tensor())
        


