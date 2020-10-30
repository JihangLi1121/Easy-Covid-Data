import pandas as pd
import datetime
import pytz

def get_states(state, df):
    return (df.loc[lambda df: df['Province_State'] == state]).reset_index(drop=True)

def get_time():
    pacific = pytz.timezone('US/Pacific')
    now = datetime.datetime.now(tz=pacific)
    time = f'{now.month}' + '/' + f'{now.day}' + '/' + f'{str(now.year)[2:]}'
    return time

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

    time = get_time()

    for i in range(len(df.index)):
        try: 
            total_deaths = df.loc[i,time]
        except KeyError:
            pacific = pytz.timezone('US/Pacific')
            now = datetime.datetime.now(tz=pacific)
            time = f'{now.month}' + '/' + f'{now.day-1}' + '/' + f'{str(now.year)[2:]}'
            total_deaths = df.loc[i,time]
        f = pd.Series([((total_deaths/df.loc[i,'Population']) * 100).__round__(4)])
        series = series.append(f, ignore_index=True)

    df.insert(2, 'Percent_Death', series)
    df_new = df.rename(columns={'Admin2':'County/Province'})
    return df_new

