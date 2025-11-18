from google_pygram import GooglePyGram as gpg

pygram = gpg(
    corpus='English',
    corpus_year=2019,
    start_year=1800,
    end_year=2000,
    smoothing=3,
    case_sensitive=False,
    phrases=['hello', 'world']
)

print(pygram.to_df())
