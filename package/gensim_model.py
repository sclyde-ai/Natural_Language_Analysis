import gensim.downloader as api
from gensim.models import KeyedVectors
import pandas as pd
import numpy as np
import os
import sys
import seaborn as sns
from functools import partial
import tensorflow as tf
from pathlib import Path
import matplotlib.pyplot as plt
sys.path.append('..')
from .country_name import get_babel, get_country_name

current_file = Path(__file__)
current_dir = Path(__file__).parent
parent_dir = Path(__file__).parent.parent
data_dir = parent_dir / Path(f"data")

info = api.info()
default_model_list = list(info['models'].keys())

class gensim_model:
    def __init__(self, model_name):
        self.model_name = model_name
        self.dict_path = data_dir / Path(self.model_name)
        if not os.path.exists(self.dict_path):
            os.mkdir(self.dict_path)
        self.load_model(model_name)
        print(self.model)
        self.index = self.get_index()
        print("init complete!")

    def load_model(self, model_name):
        if model_name in default_model_list:
            print(model_name)
            self.model = api.load(model_name)
        else:
            self.model = KeyedVectors.load_word2vec_format(
                model_name,
                binary=True
            )
        return 

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

    def get_vector(self, word, columns=None):
        csv_path = self.dict_path / Path(f"vector/{word}.csv")
        ETL_func = partial(self.ETL_vector, word)
        df = self.get_csv(ETL_func, csv_path)
        if columns:
            return df[columns]
        else:
            return df

    def get_locle_countries(self, locale):
        series = get_babel(locale)
        return series[locale]
    
    def get_locale_vector(self, locale, countries=None):
        size = self.model.vector_size

        if not countries:
            series = get_babel(locale)
            countries = series[locale]
        
        vector_list = []
        for word in countries:
            word = word.replace(' ', '_')
            if word in self.model:
                vector_list.append(self.get_vector(word))
            else:
                vector_list.append(pd.Series(np.full((size, ), np.nan), name=word))
        df = pd.concat(vector_list, axis=1)
        return df
    
    def get_locale_corr(self, locale, countries=None):
        df = self.get_locale_vector(locale, countries=countries)
        return df.dropna().dropna(axis=1)

    def corr_with_creterion(self, locale, countries=None, threshold = 1/2, above=True):
        df = self.get_locale_corr(locale, countries=countries)
        mask = np.triu(np.ones_like(df, dtype=bool), k=1)
        corr_pairs = df.where(mask).stack()
        if above:
            high_corr_pairs = corr_pairs[corr_pairs.abs() > threshold].sort_values(ascending=False)
        else:
            high_corr_pairs = corr_pairs[corr_pairs.abs() < threshold].sort_values()
        
        if high_corr_pairs.empty:
            raise Exception("DataFrame is empty")
        
        return high_corr_pairs

    def show_locale_heatmap(self, locale, countries=None):
        df = self.get_locale_corr(locale, countries=countries)
        width  = df.shape[0]/(3*0.8)
        height = df.shape[1]/3
        plt.figure(figsize=(width, height))
        sns.heatmap(
            df, 
            cmap='coolwarm',
            linewidths=0.5,
            xticklabels=1,
            yticklabels=1,
            )
    
    def show_locale_clustermap(self, locale, countries=None):
        df = self.get_locale_corr(locale, countries=countries)
        width  = df.shape[0]/3
        height = df.shape[1]/3
        plt.figure(figsize=(width, height))
        sns.clustermap(
            df, 
            method='ward', 
            cmap='coolwarm', 
            linewidths=0.5,
            xticklabels=1,
            yticklabels=1,
            )

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
    print(model.get_all_locale)
    print(model.get_all_locale_tensor())
        


