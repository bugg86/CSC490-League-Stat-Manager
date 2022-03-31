from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Summoner
from django.db.models import Q
import requests as req
import json
from .forms import SummonerSearchForm
from riotapiutilities.api import RiotApi
from riotapiutilities.consts import REGIONS

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
            
            summoner_matches = load_summoner_matches(summoners['puuid'])
            
            return render(request, 'main/summoner_info.html', {'summoner': summoners, 'matches': summoner_matches})

    return render(request, 'main/home.html', {'form': form})


def user_profile(request):
    return render(request, 'main/user_profile.html')


def win_perc_calculator(request):
    return HttpResponse("Win percentage calculator page")


def search_summoner(summoner_name):
    url = RESTAPI_SEARCH_BY_NAME_URL + summoner_name
    print("=====requesting REST API=====")
    rest_response = req.get(url, headers={'Authorization': RESRAPI_KEY})
    print(rest_response.json())
    summoners_json = json.loads(rest_response.text)
    # print("printing json")
    # print(summoners_json[0]['name'])

    # summoner does not exist in OUR database
    if len(rest_response.json()) == 0:
        
        print("summoner not in database")

        print("=====requesting RIOT API=====")
        
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

def load_summoner_matches(puuid):
    # request RIOT API for summoner matches
    # REGIONS['americas'] used because matches url does not have the same region parameter values as the summoner
    riot = RiotApi(RIOT_KEY, REGIONS['americas'])
    
    print('=====requesting RIOT API=====')
    riot_response = riot.get_match_list_by_summoner_id(puuid, 0, 10)
    
    matches = dict()
    for match in riot_response:
        print("=====requesting RIOT API=====")
        matches[match] = riot.get_match_by_match_id(match) 
    
    return matches   
    
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

    