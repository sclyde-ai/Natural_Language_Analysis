import pycountry
import pandas as pd
from babel import Locale
from pathlib import Path
import os
from functools import partial

def ETL_pycountry():
    df_list = []
    for country in pycountry.countries:
        country_df = pd.DataFrame(country)
        country_df = country_df.set_index(0)
        country_df = country_df.T
        df_list.append(country_df)
    df = pd.concat(df_list, ignore_index=True)
    df = df.set_index("numeric")
    df.to_csv("../data/pycountry.csv")
    return df

def ETL_country_code():
    df = ETL_pycountry()
    df = df.drop(columns=["name", "flag", "official_name", "common_name"])
    df.to_csv("../data/country_code.csv")
    return df

def ETL_babel(lang, country_code):
    code = lang + '_' + country_code
    locale = Locale.parse(code)
    territories = locale.territories
    country_dict = {}
    for alpha_2, name in territories.items():
        if alpha_2.isalpha():
            country_dict[alpha_2] = name
    series = pd.Series(country_dict, name=code)
    series.to_csv(f"../data/babel/{lang}_{country_code}.csv")
    return series

def ETL_country_name():
    pycountry_df = pd.read_csv("../data/pycountry.csv", index_col=0)
    babel = Path("../data/babel")
    csv_files = list(babel.glob("*.csv"))

    country_name_df = pycountry_df.copy()
    country_name_df = country_name_df.drop(columns=["name", "flag", "official_name", "common_name"])

    for file in csv_files:
        df = pd.read_csv(file, index_col=0)
        country_name_df = pd.merge(country_name_df, df, left_on="alpha_2", right_index=True)

    country_name_df.to_csv("../data/country_name.csv")
    return country_name_df

def get_csv(ETL_func, csv_path):
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, index_col=0)
    else:
        df = ETL_func()
    return df

def get_pycountry():
    df = get_csv(ETL_pycountry, "../data/pycountry.csv")
    return df

def get_country_code():
    df = get_csv(ETL_country_code, "../data/country_code.csv")
    return df

def get_babel(lang, country_code):
    ETL_func = partial(ETL_babel, lang, country_code)
    df = get_csv(ETL_func, f"../data/babel/{lang}_{country_code}.csv")
    return df

def get_country_name():
    df = get_csv(ETL_country_name, "../data/babel/country_name.csv")
    return df

if __name__ == "__main__":
    ETL_pycountry()
    ETL_country_code()
    ETL_babel("en", "US")
    ETL_babel("en", "UK")
    ETL_babel("zh", "CN")
    ETL_babel("zh", "TW")
    ETL_country_name()