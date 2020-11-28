from . import data_organize_comfirm as comfirm
import pandas as pd
import mpld3
import matplotlib.pyplot as plt 
from datetime import timedelta

def States(state):
    df = comfirm.load_df()
    df = comfirm.organize_df(df)
    df = comfirm.get_states(state, df) 
    rightnow = comfirm.get_time()
    try: 
        day = df.loc[:,rightnow.strftime("%m/%d/%y")]
    except KeyError:
        extra_day = (rightnow - timedelta(days=6)).strftime("%m/%d/%y")
        fiveday = (rightnow - timedelta(days=5)).strftime("%m/%d/%y")
        fourday = (rightnow - timedelta(days=4)).strftime("%m/%d/%y")
        threeday = (rightnow - timedelta(days=3)).strftime("%m/%d/%y")
        twoday = (rightnow - timedelta(days=2)).strftime("%m/%d/%y")
        rightnow = (rightnow - timedelta(days=1)).strftime("%m/%d/%y")
    else:
        extra_day = (rightnow - timedelta(days=5)).strftime("%m/%d/%y")
        fiveday = (rightnow - timedelta(days=4)).strftime("%m/%d/%y")
        fourday = (rightnow - timedelta(days=3)).strftime("%m/%d/%y")
        threeday = (rightnow - timedelta(days=2)).strftime("%m/%d/%y")
        twoday = (rightnow - timedelta(days=1)).strftime("%m/%d/%y")
        rightnow = rightnow.strftime("%m/%d/%y")
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
    df = States(state)
    
    rightnow = comfirm.get_time()
    df = df.loc[:, 'Population':]
    try: 
        day = df.loc[:,rightnow.strftime("%m/%d/%y")]
    except KeyError:
        fiveday = (rightnow - timedelta(days=5)).strftime("%m/%d/%y")
        fourday = (rightnow - timedelta(days=4)).strftime("%m/%d/%y")
        threeday = (rightnow - timedelta(days=3)).strftime("%m/%d/%y")
        twoday = (rightnow - timedelta(days=2)).strftime("%m/%d/%y")
        rightnow = (rightnow - timedelta(days=1)).strftime("%m/%d/%y")
    else:
        fiveday = (rightnow - timedelta(days=4)).strftime("%m/%d/%y")
        fourday = (rightnow - timedelta(days=3)).strftime("%m/%d/%y")
        threeday = (rightnow - timedelta(days=2)).strftime("%m/%d/%y")
        twoday = (rightnow - timedelta(days=1)).strftime("%m/%d/%y")
        rightnow = rightnow.strftime("%m/%d/%y")

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
    d1 = [str(fiveday), str(fourday), str(threeday), str(twoday), str(rightnow)]
    d2 = [total5, total4, total3, total2, total1]
    x = [0,1,2,3,4]

    fig = plt.figure()
    plt.xticks(x, d1)
    plt.plot(d1, d2)
    plt.ylabel(column1)
    plt.xlabel('Date')  
    plothtml2 = mpld3.fig_to_html(fig)
    return plothtml2

def ComfirmTotal(state):
    time = comfirm.get_time()
    timeformat = time.strftime("%m/%d/%y")
    df = comfirm.load_df()
    df = comfirm.organize_df(df)
    df = comfirm.get_states(state, df)
    total_comfirm = 0

    for i in range(len(df.index)):
        try: 
            temp = df.loc[i, timeformat]
        except KeyError:
            yesterday = time - timedelta(days=1)
            yesterday = yesterday.strftime("%m/%d/%y")
            temp = df.loc[i, yesterday]
        
        total_comfirm = total_comfirm + temp
    return total_comfirm
    
def ComfirmNum(state):
    df = States(state)
    time = comfirm.get_time()
    comfirm_num = 0

    for i in range(len(df.index)):
        try:
            temp = df.loc[i, time.strftime("%m/%d/%y")]
        except KeyError:
            yesterday = time - timedelta(days=1)
            yesterday = yesterday.strftime("%m/%d/%y")
            temp = df.loc[i, yesterday]

        comfirm_num = comfirm_num + temp
    
    return comfirm_num
    

