from django.http import HttpResponse
from django.shortcuts import render
from .models import Summoner
from django.db.models import QuerySet

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def player_data(request):
    return render(request, 'main/player_data.html')

def win_perc_calculator(request):
    return HttpResponse("Win percentage calculator page")

def search_summoner(request):
    if request.method == "POST":
        summoner = Summoner.objects.filter(name__iexact=request.POST['summoner_name'])
        
        return render(request,'main/search_summoner.html', {'summoner': summoner})