import pandas as pd
from .data_organize_deaths import get_population
from .data_organize_deaths import get_time
from . import data_organize_deaths as deaths
from datetime import timedelta
import pytz

def get_states(state, df):
    return deaths.get_states(state, df)

def load_df():
    url = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
    return pd.read_csv(url)

def organize_df(df):
    df = df.drop(columns=['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Lat', 'Long_','Country_Region','Combined_Key'], axis=1)
    population = pd.Series(get_population())
    df.insert(2,'Population',population)
    df2 = df
    df2 = df2.drop(columns=['Admin2', 'Province_State'], axis=1)
    for i in range(len(df.index)):
        if df.loc[i, 'Population'] == 0:
            df = df.drop(i, axis=0)
    df = df.reset_index(drop=True)
    df = df.drop([3224])
    
    series = pd.Series(dtype=float)

    today = get_time()

    for i in range(len(df.index)):
        try: 
            total_deaths = df.loc[i,today.strftime("%m/%d/%y")]
        except KeyError:
            yesterday = today - timedelta(days=1)
            yesterday = yesterday.strftime("%m/%d/%y")
            total_deaths = df.loc[i,yesterday]
        f = pd.Series([((total_deaths/df.loc[i,'Population']) * 100).__round__(4)])
        series = series.append(f, ignore_index=True)

    df.insert(2,'Percent_comfirmed',series)
    df_new = df.rename(columns={'Admin2':'County/Province'})

    return df_new