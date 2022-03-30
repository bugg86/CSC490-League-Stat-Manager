from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Summoner
from django.db.models import Q
import requests as req
import json
from .forms import SummonerSearchForm
from riotapiutilities.api import RiotApi
from riotapiutilities.consts import REGIONS

# Create your views here.

RESRAPI_KEY = 'Token a7cb48f9a0645e2eb18ea44795907fb7be41dc58'
RESTAPI_SEARCH_BY_NAME_URL = 'https://csc490-lsm-rest-api.azurewebsites.net/api/summoners/?name='
RESTAPI_SEARCH_BY_CHAMPID_URL = 'https://csc490-lsm-rest-api.azurewebsites.net/api/champions/?championid='
RIOT_KEY = 'RGAPI-ef3247df-953a-4361-80f7-f3f2c255b5d0'

def home(request):
    if request.method == "GET":
        form = SummonerSearchForm(request.GET)

        if form.is_valid():

            summoner_name = form.cleaned_data['summoner_name']

            summoners = search_summoner(summoner_name)
            
            summoner_matches = load_summoner_matches(summoners['puuid'])
            
            league = load_league(summoners['id'])
            
            mastery = load_champion_mastery(summoners['id'])
            
            return render(request, 'main/summoner_info.html', {'summoner': summoners, 'matches': summoner_matches})

    return render(request, 'main/home.html', {'form': form})


def user_profile(request):
    return render(request, 'main/user_profile.html')


def win_perc_calculator(request):
    return HttpResponse("Win percentage calculator page")


def search_summoner(summoner_name):
    url = RESTAPI_SEARCH_BY_NAME_URL + summoner_name
    print("=====requesting REST API for summoner=====")
    rest_response = req.get(url, headers={'Authorization': RESRAPI_KEY})
    print(rest_response.json())
    summoners_json = json.loads(rest_response.text)
    # print("printing json")
    # print(summoners_json[0]['name'])

    # summoner does not exist in OUR database
    if len(rest_response.json()) == 0:
        
        print("summoner not in database")

        print("=====requesting RIOT API for summoner name=====")
        
        # request RIOT API for summoner info
        riot = RiotApi(RIOT_KEY, REGIONS['north_america'])

        riot_response = riot.get_summoner_by_name(summoner_name)

        # if summoner is not found anywhere, return error
        # the status key only appears when the summoner is not found
        if 'status' in riot_response:
            return riot_response

        # lowercase keys because REST API needs lowercase keys (For now. Soon to be changed)
        riot_response = {k.lower(): v for k, v in riot_response.items()}
      
        # store the summoner object in our database
        rest_response = req.post(url, data=riot_response, headers={'Authorization': RESRAPI_KEY})

        if rest_response.status_code != 201:
            print("Something went wrong while saving the sommoner to the database", rest_response.status_code)
            
        return riot_response
    
    # summoner exists in our database    
    return summoners_json[0]

# champion mastery
def load_champion_mastery(summoner_id):
    
    riot = RiotApi(RIOT_KEY, REGIONS['north_america'])
    
    print('=====requesting RIOT API for champion masteries=====')
    riot_response = riot.get_champ_mastery_by_summoner_id(summoner_id)
    # print(riot_response)
    masteries = riot_response
        
    # sort champions by champion points
    mastery_points = sorted(masteries, key=lambda x: x['championPoints'], reverse=True)
    
    # return top 5 champions
    return mastery_points[:5]

# league rank
def load_league(summoner_id):
    
    riot = RiotApi(RIOT_KEY, REGIONS['north_america'])
    
    print('=====requesting RIOT API for league=====')
    riot_response = riot.get_league_by_summoner_id(summoner_id)
    # print(riot_response)
    
    return riot_response

def load_summoner_matches(puuid):
    # request RIOT API for summoner matches
    # REGIONS['americas'] used because matches url does not have the same region parameter values as the summoner
    riot = RiotApi(RIOT_KEY, REGIONS['americas'])
    
    print('=====requesting RIOT API for match ids=====')
    riot_response = riot.get_match_list_by_summoner_id(puuid, 0, 10)
    # print(riot_response)
    matches = dict()
    for match in riot_response:
        # print("=====requesting RIOT API for match data=====")
        print("=====requesting RIOT API for match data for id: ", match, "=====", sep='')
        matches[match] = riot.get_match_by_match_id(match)
    
    return matches
    
def summoner_info(request):
    return render(request, 'main/summoner_info.html')
