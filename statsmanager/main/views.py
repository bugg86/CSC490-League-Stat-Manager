from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Summoner
from django.db.models import Q
import requests as req
from .forms import SummonerSearchForm
from riotapiutilities.api import RiotApi
from riotapiutilities.consts import REGIONS

# Create your views here.

RESRAPI_KEY = 'Token a7cb48f9a0645e2eb18ea44795907fb7be41dc58'
RESTAPI_SEARCH_BY_NAME_URL = 'https://csc490-lsm-rest-api.azurewebsites.net/api/summoners/?name='
RIOT_KEY = 'RGAPI-ef3247df-953a-4361-80f7-f3f2c255b5d0'

def home(request):
    if request.method == "GET":
        form = SummonerSearchForm(request.GET)

        if form.is_valid():

            summoner_name = form.cleaned_data['summoner_name']

            summoners = search_summoner(summoner_name)

            return render(request, 'main/summoner_info.html', {'summoner': summoners})

    return render(request, 'main/home.html', {'form': form})


def user_data(request):
    return render(request, 'main/user_data.html')


def win_perc_calculator(request):
    return HttpResponse("Win percentage calculator page")


def search_summoner(summoner_name):
    url = RESTAPI_SEARCH_BY_NAME_URL + summoner_name
    print("=====requesting REST API=====")
    summoners = req.get(url, headers={'Authorization': RESRAPI_KEY})
    print(summoners.json())

    # summoner does not exist in OUR database
    if len(summoners.json()) == 0:
        # request RIOT API for summoner info
        print("summoner not in database")

        print("=====requesting RIOT API=====")

        

        riot = RiotApi(RIOT_KEY, REGIONS['north_america'])

        summoner_object = riot.get_summoner_by_name(summoner_name)
        print(summoner_object)

        # if summoner is not found anywhere, return error
        # the status key only appears when the summoner is not found
        if 'status' in summoner_object:
            return summoner_object
            # return render(request, 'main/summoner_info.html', {'summoner': summoner_object})

        # lowercase keys because REST API needs lowercase keys (For now)
        summoner_object = {
            k.lower(): v for k, v in summoner_object.items()}

        print(summoner_object)
        
        # store the summoner object in our database
        rest_response = req.post(url, data=summoner_object, headers={
            'Authorization': RESRAPI_KEY})

        if rest_response.status_code != 201:
            print("Something went wrong while saving the sommoner to the database")
        return summoner_object
        # return render(request, 'main/summoner_info.html', {'summoner': summoner_object})
        
    # summoner exists in our database    
    return summoners.json()


def summoner_info(request):
    return render(request, 'main/summoner_info.html')
