from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def player_data(request):
    return render(request, 'main/player_data.html')

def win_perc_calculator(request):
    return HttpResponse("Win percentage calculator page")