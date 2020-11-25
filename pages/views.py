from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from .data_organize import state_deaths
from .data_organize import states_comfirmed

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
    states = str(request.session['search'])
    df = state_deaths.States(states)
    df2 = states_comfirmed.States(states)
    #tables
    html = df.to_html()
    html2 = df2.to_html()
    fig = state_deaths.Death_graphs(states)
    fig2 = states_comfirmed.Comfirmed_graphs(states)
    ComfirmTotal = states_comfirmed.ComfirmTotal(states)
    DeathTotal = state_deaths.DeathTotal(states)
    ComfirmNum = states_comfirmed.ComfirmNum(states)
    DeathNum = state_deaths.DeathNum(states)
    return render(request, 'pages/layout.html', {
        'html': html, 'html2':html2,'state':states, 'Deathfig':fig, 'Comfirmfig':fig2,
        'ComfirmTotal': ComfirmTotal, 'DeathTotal': DeathTotal, 'ComfirmNum': ComfirmNum,
        'DeathNum': DeathNum
    })
    