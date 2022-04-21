from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .models import Summoner
from django.db.models import Q
from enum import Enum
from .forms import SummonerSearchForm
from riotapiutilities.api import RiotApi
from riotapiutilities.consts import REGIONS
from lsmrestapiutilities.api import RESTAPI
import threading

# Create your views here.

RESTAPI_KEY = 'Token a7cb48f9a0645e2eb18ea44795907fb7be41dc58'
RESTAPI_SEARCH_BY_NAME_URL = 'https://csc490-lsm-rest-api.azurewebsites.net/api/summoners/?name='
RESTAPI_SEARCH_BY_CHAMPID_URL = 'https://csc490-lsm-rest-api.azurewebsites.net/api/champions/?championid='
RIOT_KEY = 'RGAPI-ef3247df-953a-4361-80f7-f3f2c255b5d0'

class SearchType(Enum):
    SUMMONER = 1
    CHAMPION_MASTERY = 2
    LEAGUE = 3
    MATCHES = 4
    CHAMPION_NAME = 5

class handle_post_match_data(threading.Thread):
    
    def __init__(self, matches):
        self.matches = matches
        threading.Thread.__init__(self)
    
    def run(self):
        rest = RESTAPI(RESTAPI_KEY)
        for match in self.matches.values():
            print("=====storing match data=====")
            rest_response = rest.post_all_match_data(match)
            if rest_response != True:
                print("Something went wrong while saving the sommoner to the database", rest_response)
                

        
def home(request):
    if request.method == "GET":
        form = SummonerSearchForm(request.GET)

        if form.is_valid():

            summoner_name = form.cleaned_data['summoner_name']

            summoners = search_summoner(summoner_name)
            
            try:
                summoner_matches = load_summoner_matches(summoners['puuid'])
                # print(summoner_matches)
                # summoner_matches = "Hello"
            
                league = load_league(summoners['id'])
            
                mastery = load_champion_mastery(summoners['id'])
                # print(mastery)
                
            # if summoner does not exist in RIOT API
            except KeyError:
                summoner_matches = "N/A"
                league = "N/A"
                mastery = "N/A"
            # print(mastery[0]['championid'])
            championslst = []
            for i in range(0, len(mastery)):
                print(i)
                if 'championId' in mastery[i]:
                    championslst.append({mastery[i]['championId']:search_restapi(SearchType.CHAMPION_NAME, mastery[i]['championId'])})
                else:
                    championslst.append({mastery[i]['championid']:search_restapi(SearchType.CHAMPION_NAME, mastery[i]['championid'])})
            # print(championslst)
            # champions = search_restapi(SearchType.CHAMPION_NAME, summoner_name)
            
            return render(request, 'main/summoner_info.html', {'summoner': summoners, 'matches': summoner_matches, 'league': league, 'mastery': mastery, 'championslst': championslst})

    return render(request, 'main/home.html', {'form': form})


def user_profile(request):
    return render(request, 'main/user_profile.html')


def win_perc_calculator(request):
    return HttpResponse("Win percentage calculator page")

def summoner_info(request):
    return render(request, 'main/summoner_info.html')

def favorites(request):
    return render(request, 'main/favorites.html')

def search_summoner(summoner_name):
    '''
    Searches for a summoner
    Keyword arguments:
    summoner_name -- the name of the summoner to search for
    '''
    rest = RESTAPI(RESTAPI_KEY)
    
    print("=====requesting REST API for summoner=====")
    rest_response = rest.get_summoner_by_name(summoner_name)

    # summoner does not exist in OUR database
    if len(rest_response) == 0:
        
        print("summoner not found in database")

        print("=====requesting RIOT API for summoner name=====")
        
        # request RIOT API for summoner info
        riot = RiotApi(RIOT_KEY, REGIONS['north_america'])

        riot_response = riot.get_summoner_by_name(summoner_name)
        # print(riot_response)

        # if there is an error while finding a summoner, return error
        # the status key only appears when there is an error
        if 'status' in riot_response:
            return riot_response

        # lowercase keys because REST API needs lowercase keys (For now. Soon to be changed)
        # riot_response = {k.lower(): v for k, v in riot_response.items()}
        # print(riot_response)
        # print(riot_response['accountid'])
        # riot_response_json = json.loads(riot_response.)
      
        # store the summoner object in our database
        # rest_response = req.post(url, data=riot_response, headers={'Authorization': RESRAPI_KEY})
        rest_response = rest.post_summoner(riot_response)

        if rest_response != True:
            print("Something went wrong while saving the sommoner to the database", rest_response)
            
        return riot_response
    
    # summoner exists in our database
    print("summoner found in database")  
    return rest_response[0]

# champion mastery
def load_champion_mastery(summoner_id):
    '''
    loads the champion mastery of a summoner
    keyword arguments:
    summoner_id -- the summoner id of the summoner to load the champion mastery of
    '''
    
    # print('=====requesting REST API for champion mastery=====')
    rest_response = search_restapi(SearchType.CHAMPION_MASTERY, summoner_id)
    if rest_response != 404:
        return rest_response
    
    print("masteries not found in database")
    
    riot = RiotApi(RIOT_KEY, REGIONS['north_america'])
    
    print('=====requesting RIOT API for champion masteries=====')
    riot_response = riot.get_champ_mastery_by_summoner_id(summoner_id)
    # print(riot_response)
    masteries = riot_response
        
    # sort champions by champion points
    mastery_by_points = sorted(masteries, key=lambda x: x['championPoints'], reverse=True)
    
    rest = RESTAPI(RESTAPI_KEY)
    for mastery in mastery_by_points:
        rest_response = rest.post_championMastery(mastery)
        # if rest_response.status_code != 201:
        #     print("Something went wrong while saving the sommoner to the database", rest_response.status_code)
    
    # return top 5 champions
    
    
    return mastery_by_points[:10]

# league rank
def load_league(summoner_id):
    '''
    loads the league of a summoner
    Keyword arguments:
    summoner_id -- the summoner id of the summoner to load the league of
    '''
    
    riot = RiotApi(RIOT_KEY, REGIONS['north_america'])
    
    print('=====requesting RIOT API for league=====')
    riot_response = riot.get_league_by_summoner_id(summoner_id)
    # print(riot_response)
    # print(riot_response[0])
    
    # rest = RESTAPI(RESRAPI_KEY)
    # rest_response = rest.post_league(riot_response[0])
    # the response returns an array of leagues by game mode, but we're only tracking regular league ranks.
    # we are going to ignore TFT ranks
    return riot_response

def load_summoner_matches(puuid):
    '''
    loads 10 recent matches of a summoner
    Keyword arguments:
    puuid -- the puuid of the summoner to load the matches of
    '''
    
    # check if summoner has matches in our database
    rest_response = search_restapi(SearchType.MATCHES, puuid)
    # print(rest_response)
    if rest_response != 404:
        return rest_response
    
    # request RIOT API for summoner matches
    # REGIONS['americas'] used because matches url does not have the same region parameter values as the summoner
    riot = RiotApi(RIOT_KEY, REGIONS['americas'])
    
    print('=====requesting RIOT API for match ids=====')
    riot_response = riot.get_match_list_by_summoner_id(puuid, 0, 10)
    
    # print(riot_response)
    matches = dict()
    for match in riot_response:
        print("=====requesting RIOT API for match data for id: ", match, "=====", sep='')
        matches[match] = riot.get_match_by_match_id(match)
    
    # rest = RESTAPI(RESTAPI_KEY)
    # for match in matches.values():
    #     print("=====storing match data=====")
    #     rest_response = rest.post_all_match_data(match)
    #     if rest_response != True:
    #         print("Something went wrong while saving the sommoner to the database", rest_response.status_code)
    
    handle_post_match_data(matches).start()
        
    return matches


# Experimenting on optimizing the code
def search_restapi(search_type, search_value):
    '''
    Queries the REST API for a summoner, matches, league, or champion mastery
    Keyword arguments:
    search_type -- the type of search to perform
    search_value -- the value to search for
    '''
    rest = RESTAPI(RESTAPI_KEY)
    if search_type == SearchType.SUMMONER:
        print("=====requesting REST API for summoner=====")
        rest_response = rest.get_summoner_by_name(search_value)
        if len(rest_response) == 0:
            return 404
        else:
            print("summoner found in database")
            return rest_response[0]
    elif search_type == SearchType.MATCHES:
        print('=====requesting REST API for match ids=====')
        # rest_response = rest.get_match_by_id(search_value)
        rest_response = rest.get_matchparticipant_by_puuid(search_value)
        if len(rest_response) == 0:
            print("matches not found in database")
            return 404
        else:
            print("matches found in database")

            matches = dict()
            for i,participant in enumerate(rest_response, start=0):
                if i == 10:
                    break
                print(participant["matchid"])
                # matches[participant] = rest.get_champion_by_id(participant["matchid"])
                match_response = rest.get_match_by_id(participant["matchid"])
                for match_data in match_response:
                    matches[participant["matchid"]] = match_data
                    
            return matches
    elif search_type == SearchType.LEAGUE:
        print('=====requesting REST API for league=====')
        rest_response = rest.get_league_by_summonerid(search_value)
        if len(rest_response) == 0:
            return 404
        else:
            print("league found in database")
            return rest_response[0]
    elif search_type == SearchType.CHAMPION_MASTERY:
        print('=====requesting REST API for champion mastery=====')
        rest_response = rest.get_championmastery_by_summonerid(search_value)
        if len(rest_response) == 0:
            return 404
        else:
            print("champion masteries found in database")
            # masteries = dict()
            masteries = list()
            for i, mastery in enumerate(rest_response, start=0):
                if i == 10:
                    break
                # print(mastery)
                # masteries[mastery["championid"]] = mastery
                masteries.append(mastery)
                # print(masteries)
            # sort champions by champion points
            # mastery_by_points = sorted(masteries, key=lambda x: x['championPoints'], reverse=False)
            # print(mastery_by_points)
            return masteries
    elif search_type == SearchType.CHAMPION_NAME:
        print('=====requesting REST API for champion name=====')
        rest_response = rest.get_champion_name_by_id(search_value)
        if len(rest_response) == 0:
            return 404
        else:
            return rest_response
        
    else:
        print("Invalid search type")
        
# def request_riotapi(search_type, data):
#     riot = RiotApi(RIOT_KEY, REGIONS['north_america'])
#     if search_type == SearchType.SUMMONER:
#         print('=====requesting RIOT API for summoner=====')
#         riot_response = riot.get_summoner_by_name(data)
        
    
def summoner_info(request):
    return render(request, 'main/summoner_info.html')

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "main/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="main/password/password_reset.html", context={"password_reset_form":password_reset_form})
