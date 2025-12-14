import gensim.downloader as api
import pandas as pd
import os
import sys
import seaborn as sns
from functools import partial
sys.path.append('..')
from package.country_name import get_babel, get_country_name

class gensim_model:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        if not os.path.exists(f"../data/{self.dictionary}"):
            os.mkdir(f"../data/{self.dictionary}")
        self.model = api.load(dictionary)
        self.index = self.ETL_index()
        print("init complete!")

    def get_model(self):
        return self.model

    def ETL_index(self):
        index = self.model.index_to_key
        index_series = pd.Series(index)
        index_series.to_csv(f"../data/{self.dictionary}/index.csv")
        return index_series

    def ETL_similar(self, word):
        dict_path = f"../data/{self.dictionary}/similar"
        if not os.path.exists(dict_path):
            os.mkdir(dict_path)
        
        similar = self.model.most_similar(word, topn=None)
        df = pd.Series(similar, index=self.index, name=word)

        csv_path = f"../data/{self.dictionary}/similar/{word}.csv"
        df.to_csv(csv_path)
        return df

    def ETL_vector(self, word) -> pd.DataFrame:
        dict_path = f"../data/{self.dictionary}/vector"
        if not os.path.exists(dict_path):
            os.mkdir(dict_path)
        vector = self.model.get_vector(word)
        df = pd.Series(vector, name=word)
        csv_path = f"../data/{self.dictionary}/vector/{word}.csv"
        df.to_csv(csv_path)
        return df
    
    def get_csv(self, ETL_func, csv_path):
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path, index_col=0)
        else:
            df = ETL_func()
        return df
    
    def get_index(self):
        df = self.get_csv(self.ETL_index, f"../data/{self.dictionary}/index.csv")
        return df
    
    def get_similar(self, word):
        df = self.get_csv(self.ETL_similar, f"../data/{self.dictionary}/similar/{word}.csv")
        return df

    def get_vector(self, word):
        ETL_func = partial(self.ETL_vector, word)
        df = self.get_csv(ETL_func, f"../data/{self.dictionary}/vector/{word}.csv")
        return df
    
    def get_country_vector(self, lang, country_code):
        series = get_babel(lang, country_code)
        vector_list = []
        column = lang + '_' + country_code
        for word in series[column]:
            if word in self.model:
                vector_list.append(self.get_vector(word))
        df = pd.concat(vector_list, axis=1)
        return df
    
    def show_country_corr(self, lang, country_code):
        EN_df = self.get_country_vector(lang, country_code)
        sns.heatmap(EN_df.corr())

