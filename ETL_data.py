import pandas as pd
from google_pygram import GooglePyGram as gpg

def load_time_series(limit=None):
    word_freq = pd.read_csv("data/unigram_freq.csv")
    series_list = []
    if limit is None:
        limit = len(word_freq)
    for word in word_freq['word'][:limit]:
        pygram = gpg(
            corpus='English',
            case_sensitive=False,
            phrases=[word]
        )
        series = pygram.to_df()
        series_list.append(series)
    df = pd.concat(series_list)
    df.to_csv(f"data/time_series.csv")

if __name__ == "__main__":
    load_time_series(limit=512)