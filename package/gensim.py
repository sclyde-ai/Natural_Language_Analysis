import gensim.downloader as api
import pandas as pd
import os

class gensim_model:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.model = api.load(dictionary)
        if not os.path.exists(f"../data/{self.dictionary}"):
            os.mkdir(f"../data/{self.dictionary}")
        self.index = self.load_index()
    
    def get_model(self):
        return self.model
    
    def get_index(self):
        index = self.model.index_to_key
        index_series = pd.Series(index)
        return index_series

    def load_index(self):
        index_series = self.get_index()
        index_series.to_csv(f"../data/{self.dictionary}/index.csv")
        return index_series

    def get_similar(self, word):
        similar = self.model.most_similar(word, topn=None)
        df = pd.Series(similar, index=self.index, name=word)
        return df

    def load_similar(self, word):
        if not os.path.exists(f"../data/{self.dictionary}/similar"):
            os.mkdir(f"../data/{self.dictionary}/similar")
        df = self.get_similar(word)
        df.to_csv(f"../data/{self.dictionary}/similar/{word}.csv")
        return df
    

    def load_vector(self, word):
        pass

