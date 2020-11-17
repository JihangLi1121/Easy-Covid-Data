from . import data_organize_comfirm as comfirm
import pandas as pd
import datetime
import pytz
import seaborn as sns
import io
import base64

def Comfirm_fig_to_base64(fig):
    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue())

def States(state):
    df = comfirm.load_df()
    df = comfirm.organize_df(df)
    df = comfirm.get_states(state, df) 
    pacific = pytz.timezone('US/Pacific')
    now = datetime.datetime.now(tz=pacific)
    rightnow = comfirm.get_time()
    try: 
        day = df.loc[:,rightnow]
    except KeyError:
        extra_day = f'{now.month}' + '/' + f'{now.day-6}' + '/' + f'{str(now.year)[2:]}' 
        fiveday = f'{now.month}' + '/' + f'{now.day-5}' + '/' + f'{str(now.year)[2:]}' 
        fourday = f'{now.month}' + '/' + f'{now.day-4}' + '/' + f'{str(now.year)[2:]}' 
        threeday = f'{now.month}' + '/' + f'{now.day-3}' + '/' + f'{str(now.year)[2:]}' 
        twoday = f'{now.month}' + '/' + f'{now.day-2}' + '/' + f'{str(now.year)[2:]}' 
        rightnow = f'{now.month}' + '/' + f'{now.day-1}' + '/' + f'{str(now.year)[2:]}' 
    else:
        extra_day = f'{now.month}' + '/' + f'{now.day-5}' + '/' + f'{str(now.year)[2:]}' 
        fiveday = f'{now.month}' + '/' + f'{now.day-4}' + '/' + f'{str(now.year)[2:]}' 
        fourday = f'{now.month}' + '/' + f'{now.day-3}' + '/' + f'{str(now.year)[2:]}' 
        threeday = f'{now.month}' + '/' + f'{now.day-2}' + '/' + f'{str(now.year)[2:]}' 
        twoday = f'{now.month}' + '/' + f'{now.day-1}' + '/' + f'{str(now.year)[2:]}' 
    five_day = df.loc[:,extra_day:]
    for element in range(0, len(five_day.index-1)):
        extra = five_day.loc[element, extra_day]
        five = five_day.loc[element, fiveday]
        four = five_day.loc[element, fourday]
        three = five_day.loc[element, threeday]
        two = five_day.loc[element, twoday]
        one = five_day.loc[element, rightnow] 
        five_day.loc[element, fiveday] = five - extra
        five_day.loc[element, fourday] = four - five
        five_day.loc[element, threeday] = three - four
        five_day.loc[element, twoday] = two - three
        five_day.loc[element, rightnow] = one - two
    five_day = five_day.loc[:, fiveday:]
    for i in range(0, len(five_day.index-1)):
        for element in five_day.columns:
            day = five_day.loc[i, element]
            if day < 0:
                five_day.loc[i, element] = 0

    df = df.loc[:,:'Population'] 
    return df.join(five_day)

def Comfirmed_graphs(state):
    pacific = pytz.timezone('US/Pacific')
    now = datetime.datetime.now(tz=pacific)
    
    df = States(state)
    
    rightnow = comfirm.get_time()
    df = df.loc[:, 'Population':]
    try: 
        day = df.loc[:,rightnow]
    except KeyError:
        fiveday = f'{now.month}' + '/' + f'{now.day-5}' + '/' + f'{str(now.year)[2:]}' 
        fourday = f'{now.month}' + '/' + f'{now.day-4}' + '/' + f'{str(now.year)[2:]}' 
        threeday = f'{now.month}' + '/' + f'{now.day-3}' + '/' + f'{str(now.year)[2:]}' 
        twoday = f'{now.month}' + '/' + f'{now.day-2}' + '/' + f'{str(now.year)[2:]}' 
        rightnow = f'{now.month}' + '/' + f'{now.day-1}' + '/' + f'{str(now.year)[2:]}' 
    else:
        fiveday = f'{now.month}' + '/' + f'{now.day-4}' + '/' + f'{str(now.year)[2:]}' 
        fourday = f'{now.month}' + '/' + f'{now.day-3}' + '/' + f'{str(now.year)[2:]}' 
        threeday = f'{now.month}' + '/' + f'{now.day-2}' + '/' + f'{str(now.year)[2:]}' 
        twoday = f'{now.month}' + '/' + f'{now.day-1}' + '/' + f'{str(now.year)[2:]}' 

    total5 = 0
    total4 = 0
    total3 = 0
    total2 = 0
    total1 = 0

    for i in range(0, len(df.index-1)):
        total5 = total5 + df.loc[i, fiveday]
        total4 = total4 + df.loc[i, fourday]
        total3 = total3 + df.loc[i, threeday]
        total2 = total2 + df.loc[i, twoday]
        total1 = total1 + df.loc[i, rightnow]

    column1 = 'Comfirm per day in ' + f'{state}'
    d1 = {'Date':[fiveday, fourday, threeday, twoday, rightnow], column1:[total5, total4, total3, total2, total1]}
    dataset2 = pd.DataFrame(data=d1)

    plot2 = sns.lineplot(data=dataset2, x='Date', y=column1)
    return plot2.get_figure()