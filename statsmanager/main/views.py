from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Summoner
from django.db.models import Q
import requests as req
from .forms import SummonerSearchForm
from main.riot import RiotApi
import main.consts as consts

# Create your views here.


def home(request):
    if request.method == "GET":
        form = SummonerSearchForm(request.GET)

        if form.is_valid():

            summoner_name = form.cleaned_data['summoner_name']

            url = 'https://csc490-lsm-rest-api.azurewebsites.net/api/summoners/?name=' + summoner_name
            print("=====requesting REST API=====")
            summoners = req.get(
                url, headers={'Authorization': consts.RESTAPI['key']})
            print(summoners.json())

            # summoner does not exist in OUR database
            if len(summoners.json()) == 0:
                # request RIOT API for summoner info
                print("summoner not in database")

                print("=====requesting RIOT API=====")

                api = RiotApi(consts.RIOTAPI['key'],
                              consts.REGIONS['north_america'])

                summoner_object = api.get_summoner_by_name(summoner_name)
                print(summoner_object)

                # if summoner is not found anywhere, return error
                if 'status' in summoner_object:
                    return render(request, 'main/summoner_info.html', {'summoner': summoner_object})

                # store the summoner object in our database
                summoner_object = {
                    k.lower(): v for k, v in summoner_object.items()}

                print(summoner_object)

                rest_response = req.post(url, data=summoner_object, headers={
                                         'Authorization': consts.RESTAPI['key']})

                if rest_response.status_code != 201:
                    print(
                        "Something went wrong while saving the sommoner to the database")

                return render(request, 'main/summoner_info.html', {'summoner': summoner_object})

            return render(request, 'main/summoner_info.html', {'summoner': summoners.json()})

    return render(request, 'main/home.html', {'form': form})


def user_data(request):
    return render(request, 'main/user_data.html')


def win_perc_calculator(request):
    return HttpResponse("Win percentage calculator page")


def search_summoner(request):
    return render(request, 'main/summoner_info.html')
