import pandas as pd
from google_pygram import GooglePyGram as gpg
import time

def load_time_series(start=0, end=None, limit=None):
    word_freq = pd.read_csv("data/unigram_freq.csv")
    print(word_freq)
    series_list = []
    if limit is None:
        limit = len(word_freq)
    if end is None:
        end = start + limit
    for word in word_freq['word'][start:end]:
        print(word)
        try:
            pygram = gpg(
                corpus='English',
                case_sensitive=False,
                phrases=[word]
            )
            series = pygram.to_df()[word]
            series.to_csv(f"data/{word}.csv")
            series_list.append(series)
            time.sleep(1)
        except Exception as e:
            print("ERROR: ", e)
            continue
        
    df = pd.concat(series_list)
    df.to_csv(f"data/time_series.csv")

if __name__ == "__main__":
    load_time_series(limit=512)