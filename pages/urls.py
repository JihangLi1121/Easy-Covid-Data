from django.urls import path
from . import views


app_name = 'pages'
urlpatterns = [
    path('State', views.State, name='states'),
    path('', views.index, name='index')
]