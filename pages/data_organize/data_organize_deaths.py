import pandas as pd
from datetime import date
from datetime import timedelta
import datetime
import pytz

def get_states(state, df):
    return (df.loc[lambda df: df['Province_State'] == state]).reset_index(drop=True)

def get_time():
    pacific = pytz.timezone('US/Pacific')
    today = datetime.datetime.now(pacific)
    return today

def load_df():
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
    return pd.read_csv(url)

def get_population():
    df = load_df()
    df = df['Population']
    return df

def organize_df(df):
    df = df.drop(columns=['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Lat', 'Long_','Country_Region','Combined_Key'], axis=1)
    df2 = df
    df2 = df2.drop(columns=['Admin2', 'Province_State', 'Population'], axis=1)
    for i in range(len(df.index)):
        if df.loc[i, 'Population'] == 0:
            df = df.drop(i, axis=0)
    df = df.reset_index(drop=True)

    series = pd.Series(dtype=float)

    today = get_time()

    for i in range(len(df.index)):
        try: 
            total_deaths = df.loc[i,today.strftime("%m/%d/%y")]
        except KeyError:
            yesterday = today - timedelta(days = 1)
            yesterday = yesterday.strftime("%m/%d/%y")
            total_deaths = df.loc[i,yesterday]
        f = pd.Series([((total_deaths/df.loc[i,'Population']) * 100).__round__(4)])
        series = series.append(f, ignore_index=True)

    df.insert(2, 'Percent_Death', series)
    df_new = df.rename(columns={'Admin2':'County/Province'})
    return df_new

