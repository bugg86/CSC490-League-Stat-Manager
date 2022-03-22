from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Summoner
from django.db.models import Q
import requests as req
from .forms import SummonerSearchForm

# Create your views here.


def home(request):
    if request.method == "GET":
        form = SummonerSearchForm(request.GET)

        if form.is_valid():

            summoner_name = form.cleaned_data['summoner_name']

            url = 'https://csc490-lsm-rest-api.azurewebsites.net/api/summoners?name=' + summoner_name
            #summoner_object = {'id' : 'hm1cW5bx1BUJd9S2dtv2El1C-RQlwM9Y9pAZ0e5f_FFMahc', 'accountId' : 'EX9vUwqVSNWPpL167jKmlD1RH47HNy5-76bslHMFLD-JTKQ', 'puuid' : 'jYHjDC1WFC_1YqNldzBESxEzERwh0wZq9gE58ccUHcAFKYmdS5BYSvHS_uLp8uIzMnLN6PxjrWIV8g', 'name' : 'FunnyBug', 'profileIconId' : 5091, 'revisionDate' : 1647237960000, 'summonerLevel': 108}
            print("=====requesting=====")
            summoners = req.get(url)
            print(summoners.json())
            if len(summoners.json()) == 0:
                # request RIOT API for summoner info
                print("summoner not in database")
                return render(request, 'main/summoner_info.html', {'summoner': "No summoner found in our database :("})
            
            return render(request, 'main/summoner_info.html', {'summoner': summoners.json()})
        
    return render(request, 'main/home.html', {'form': form})


def user_data(request):
    return render(request, 'main/user_data.html')


def win_perc_calculator(request):
    return HttpResponse("Win percentage calculator page")


def search_summoner(request):
    return render(request, 'main/summoner_info.html')
    # if request.method == "GET":

    #     url = 'https://csc490-lsm-rest-api.azurewebsites.net/api/summoners'
    #     # url = 'https://csc490-lsm-rest-api.azurewebsites.net/api/summoners?name='
    #     #summoner_object = {'id' : 'hm1cW5bx1BUJd9S2dtv2El1C-RQlwM9Y9pAZ0e5f_FFMahc', 'accountId' : 'EX9vUwqVSNWPpL167jKmlD1RH47HNy5-76bslHMFLD-JTKQ', 'puuid' : 'jYHjDC1WFC_1YqNldzBESxEzERwh0wZq9gE58ccUHcAFKYmdS5BYSvHS_uLp8uIzMnLN6PxjrWIV8g', 'name' : 'FunnyBug', 'profileIconId' : 5091, 'revisionDate' : 1647237960000, 'summonerLevel': 108}
    #     print("=====requesting=====")
    #     summoners = req.get(url)
    #     print(summoners.json())
    #     if summoners.json() == '[]':
    #         # request RIOT API for summoner info
    #         return
    #     # This is hard coded. The View needs to bring in the summoner info based on the search value.
    #     return render(request, 'main/summoner_info.html', {'summoner': summoners.json()[0]})
    # else:
    #     print("=====returning null=====")
    #     return render(request, 'main/summoner_info.html', {})
