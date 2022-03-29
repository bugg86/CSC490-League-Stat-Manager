from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('win_perc_calculator/', views.win_perc_calculator, name='win_perc_calculator'),
    path('summoner_info/', views.search_summoner, name='summoner_info'),
]