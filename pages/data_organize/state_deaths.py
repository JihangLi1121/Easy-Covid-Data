from . import data_organize_deaths as deaths
import pandas as pd
import mpld3
import matplotlib.pyplot as plt
from datetime import timedelta

def States(state):
    # load and organize dataframe
    df = deaths.load_df()
    df = deaths.organize_df(df)
    df = deaths.get_states(state, df)
    # get time 
    rightnow = deaths.get_time()
    # ------------------------------------------------------------------------
    # START OF TABLE 
    # get all 5 days 
    try: 
        day = df.loc[:,rightnow.strftime("%m/%d/%y")]
    except KeyError:
        extra_day = (rightnow - timedelta(days=6)).strftime("%m/%d/%y")
        fiveday = (rightnow - timedelta(days=5)).strftime("%m/%d/%y")
        fourday = (rightnow - timedelta(days=4)).strftime("%m/%d/%y")
        threeday = (rightnow - timedelta(days=3)).strftime("%m/%d/%y")
        twoday = (rightnow - timedelta(days=2)).strftime("%m/%d/%y")
        today = (rightnow - timedelta(days=1)).strftime("%m/%d/%y")
    else:
        extra_day = (rightnow - timedelta(days=5)).strftime("%m/%d/%y")
        fiveday = (rightnow - timedelta(days=4)).strftime("%m/%d/%y")
        fourday = (rightnow - timedelta(days=3)).strftime("%m/%d/%y")
        threeday = (rightnow - timedelta(days=2)).strftime("%m/%d/%y")
        twoday = (rightnow - timedelta(days=1)).strftime("%m/%d/%y")
        today = rightnow.strftime("%m/%d/%y")
    five_day = df.loc[:,extra_day:]
    for element in range(0, len(five_day.index-1)):
        extra = five_day.loc[element, extra_day]
        five = five_day.loc[element, fiveday]
        four = five_day.loc[element, fourday]
        three = five_day.loc[element, threeday]
        two = five_day.loc[element, twoday]
        one = five_day.loc[element, today]
        five_day.loc[element, fiveday] = five - extra
        five_day.loc[element, fourday] = four - five
        five_day.loc[element, threeday] = three - four
        five_day.loc[element, twoday] = two - three
        five_day.loc[element, today] = one - two
    # get the data of the five days 
    five_day = five_day.loc[:, fiveday:]
    for i in range(0, len(five_day.index-1)):
        for element in five_day.columns:
            day = five_day.loc[i, element]
            if day < 0:
                five_day.loc[i, element] = 0
    # get the names before Population without the numbers 
    fiveBefore = df.loc[:,:'Population']
    # join fivedays of numbers to fiveBefore to create table
    fiveFinal = fiveBefore.join(five_day) # return for table 
    # FINISH OF TABLE 
    # ------------------------------------------------------------------------
    # START OF GRAPH
    # get total number of death for each day based on table from five_day
    total5 = 0
    total4 = 0
    total3 = 0
    total2 = 0
    total1 = 0

    for i in range(0, len(five_day.index-1)):
        total5 = total5 + five_day.loc[i, fiveday]
        total4 = total4 + five_day.loc[i, fourday]
        total3 = total3 + five_day.loc[i, threeday]
        total2 = total2 + five_day.loc[i, twoday]
        total1 = total1 + five_day.loc[i, today]
    
    # Create labels and lists for graph 
    column = 'Death per day in ' + f'{state}'
    d1 = [str(fiveday), str(fourday), str(threeday), str(twoday), str(today)]
    d2 = [total5, total4, total3, total2, total1]
    x = [0,1,2,3,4]
    # Create graph 
    fig = plt.figure()
    plt.xlabel('Date')  
    plt.ylabel(column)
    plt.xticks(x, d1)
    plt.plot(d1, d2)
    plothtml1 = mpld3.fig_to_html(fig) # return for graph 
    print(plothtml1)
    # FINISH OF GRAPH
    # ------------------------------------------------------------------------
    # START OF TOTAL NUMBER OF DEATH
    total_death = 0
    # adding every number reported from state df into total_death
    for i in range(len(df.index)):
        try: 
            temp = df.loc[i, rightnow.strftime("%m/%d/%y")]
        except KeyError:
            yesterday = rightnow - timedelta(days=1)
            temp = df.loc[i, yesterday.strftime("%m/%d/%y")]
        
        total_death = total_death + temp # return for Total Death 
    # FINISH OF TOTAL DEATH
    # ------------------------------------------------------------------------
    # START OF DAILY NUMBER
    death_num = 0
    # adding reports of today or yesterday's number from fiveFinal
    for i in range(len(fiveFinal.index)):
        try:
            temp = fiveFinal.loc[i, rightnow.strftime("%m/%d/%y")]
        except KeyError:
            yesterday = rightnow - timedelta(days=1)
            temp = fiveFinal.loc[i, yesterday.strftime("%m/%d/%y")]

        death_num = death_num + temp # return for daily number of Death
    # FINISH OF DAILY NUMBER
    # ------------------------------------------------------------------------
    # START OF FINAL RETURN 
    # create dict contain all data
    finalDeath = {'deathTable':fiveFinal, 'deathGraph':plothtml1, 
        'deathTotal':total_death, 'dailyDeath':death_num}

    return finalDeath

    
    
    
    
            
        
        