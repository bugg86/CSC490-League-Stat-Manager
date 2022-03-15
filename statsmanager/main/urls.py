from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('player_data/', views.player_data, name='player_data'),
    path('win_perc_calculator/', views.win_perc_calculator, name='win_perc_calculator'),
    path('search_summoner/', views.search_summoner, name='search_summoner'),
]
