from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from .data_organize import state_deaths
from .data_organize import states_comfirmed
from datetime import datetime

# Create your views here.

class NewTaskForm(forms.Form):
    search = forms.CharField(label="Search for your state")

def index(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            request.session["search"] = search
            return HttpResponseRedirect(reverse("pages:states"))
        else:
            return render(request, "pages/index.html", {
                "form": form
            })
    return render(request, 'pages/index.html', {
        'form': NewTaskForm()      
    })

def State(request):
    if "search" not in request.session:
        request.session["search"] = ''
    states = str(request.session['search']) # state in string

    print(f"{datetime.now().time()} Finish Get search result")
    print("wtf")
    # get dicts
    deathDict = state_deaths.States(states)
    comfirmDict = states_comfirmed.States(states)

    print(f"{datetime.now().time()} Finish get dictionaries")
    # get tables
    deathTable = deathDict['deathTable']
    comfirmTable = comfirmDict['comfirmTable']
    # turn tables into html
    deathTable_html = deathTable.to_html()
    comfirmTable_html = comfirmTable.to_html()

    print(f"{datetime.now().time()} Finish get tables and turn into html")
    # get graphs 
    deathfig = deathDict['deathGraph']
    comfirmfig = comfirmDict['comfirmGraph']

    print(f"{datetime.now().time()} Finish get graphs")
    # get total numbers 
    deathTotal = deathDict['deathTotal']
    comfirmTotal = comfirmDict['comfirmTotal']

    print(f"{datetime.now().time()} Finish get total numbers")
    # get daily numbers
    deathNum = deathDict['dailyDeath']
    comfirmNum = comfirmDict['dailyComfirm']

    print(f"{datetime.now().time()} Finish get daily numbers")

    return render(request, 'pages/layout.html', {
        'DeathTable':deathTable_html, 'ComfirmTable':comfirmTable_html,'state':states, 
        'Deathfig':deathfig, 'Comfirmfig':comfirmfig, 'DeathTotal':deathTotal, 
        'ComfirmTotal':comfirmTotal, 'DeathNum':deathNum, 'ComfirmNum':comfirmNum
    })

def render_by_map(request, state):
    states = state # state in string

    print(f"{datetime.now().time()} Finish Get search result")
    # get dicts
    deathDict = state_deaths.States(states)
    comfirmDict = states_comfirmed.States(states)

    print(f"{datetime.now().time()} Finish get dictionaries")
    # get tables
    deathTable = deathDict['deathTable']
    comfirmTable = comfirmDict['comfirmTable']
    # turn tables into html
    deathTable_html = deathTable.to_html()
    comfirmTable_html = comfirmTable.to_html()

    print(f"{datetime.now().time()} Finish get tables and turn into html")
    # get graphs 
    deathfig = deathDict['deathGraph']
    comfirmfig = comfirmDict['comfirmGraph']

    print(f"{datetime.now().time()} Finish get graphs")
    # get total numbers 
    deathTotal = deathDict['deathTotal']
    comfirmTotal = comfirmDict['comfirmTotal']

    print(f"{datetime.now().time()} Finish get total numbers")
    # get daily numbers
    deathNum = deathDict['dailyDeath']
    comfirmNum = comfirmDict['dailyComfirm']

    print(f"{datetime.now().time()} Finish get daily numbers")

    return render(request, 'pages/layout.html', {
        'DeathTable':deathTable_html, 'ComfirmTable':comfirmTable_html,'state':states, 
        'Deathfig':deathfig, 'Comfirmfig':comfirmfig, 'DeathTotal':deathTotal, 
        'ComfirmTotal':comfirmTotal, 'DeathNum':deathNum, 'ComfirmNum':comfirmNum
    })

    
