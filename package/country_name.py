import pycountry
import pandas as pd
from babel import Locale
from pathlib import Path
import os
from functools import partial
from pathlib import Path

current_file = Path(__file__)
current_dir = Path(__file__).parent
parent_dir = Path(__file__).parent.parent
data_dir = parent_dir / Path(f"data")

def ETL_pycountry():
    df_list = []
    for country in pycountry.countries:
        country_df = pd.DataFrame(country)
        country_df = country_df.set_index(0)
        country_df = country_df.T
        df_list.append(country_df)
    df = pd.concat(df_list, ignore_index=True)
    df = df.set_index("numeric")
    pycountry_path = data_dir / Path("pycountry.csv")
    df.to_csv(pycountry_path)
    return df

def ETL_country_code():
    df = ETL_pycountry()
    df = df.drop(columns=["name", "flag", "official_name", "common_name"])
    country_code_path = data_dir / Path("country_code.csv")
    df.to_csv(country_code_path)
    return df

def ETL_babel(locale):
    locale = Locale.parse(locale)
    territories = locale.territories
    country_dict = {}
    for alpha_2, name in territories.items():
        if alpha_2.isalpha():
            country_dict[alpha_2] = name
    series = pd.Series(country_dict, name=locale)
    csv_path = data_dir / Path(f"babel/{locale}.csv")
    series.to_csv(csv_path)
    return series

def ETL_country_name():
    pycountry_path = data_dir / Path("pycountry.csv")
    pycountry_df = pd.read_csv(pycountry_path, index_col=0)

    babel = data_dir / Path("babel")
    csv_files = list(babel.glob("*.csv"))
    print(csv_files)

    country_name_df = pycountry_df.copy()
    country_name_df = country_name_df.drop(columns=["name", "flag", "official_name", "common_name"])

    for file in csv_files:
        df = pd.read_csv(file, index_col=0)
        country_name_df = pd.merge(country_name_df, df, left_on="alpha_2", right_index=True)

    country_name_path = data_dir / Path("country_name.csv")
    country_name_df.to_csv(country_name_path)
    return country_name_df

def get_csv(ETL_func, csv_path):
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, index_col=0)
    else:
        df = ETL_func()
    return df

def get_pycountry():
    pycountry_path = data_dir / Path("pycountry.csv")
    df = get_csv(ETL_pycountry, pycountry_path)
    return df

def get_country_code():
    country_code_path = data_dir / Path("country_code.csv")
    df = get_csv(ETL_country_code, country_code_path)
    return df

def get_babel(locale):
    csv_path = data_dir / Path(f"babel/{locale}.csv")
    ETL_func = partial(ETL_babel, locale)
    df = get_csv(ETL_func, csv_path)
    return df

def get_country_name():
    country_name_path = data_dir / Path("country_name.csv")
    df = get_csv(ETL_country_name, country_name_path)
    return df

if __name__ == "__main__":
    ETL_pycountry()
    ETL_country_code()
    US_series = ETL_babel("en_US")
    UK_series = ETL_babel("en_UK")
    CN_series = ETL_babel("zh_CN")
    TW_series = ETL_babel("zh_TW")
    ETL_country_name()
    print(US_series)
