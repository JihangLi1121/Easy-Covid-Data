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
    return render(request, 'pages/layout.html', {
        'html': html, 'html2':html2, 'deathgraph':Deaths_graph(states), 'comfirmgraph':Comfirmed_graph(states)
    })
def Deaths_graph(states):
    #death graph
    deathgraph = state_deaths.Death_graphs(states)
    encoded1 = state_deaths.Death_fig_to_base64(deathgraph)
    my_html1 = "data:deathgraph/png;base64, {}".format(encoded1.decode('utf-8'))
    return my_html1

def Comfirmed_graph(states):
    #comfirm graph
    comfirmgraph = states_comfirmed.Comfirmed_graphs(states)
    encoded2 = states_comfirmed.Comfirm_fig_to_base64(comfirmgraph)
    my_html2 = "data:comfirmgraph/png;base64, {}".format(encoded2.decode('utf-8'))
    return my_html2
