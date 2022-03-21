from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_data/', views.user_data, name='user_data'),
    path('win_perc_calculator/', views.win_perc_calculator, name='win_perc_calculator'),
    path('summoner_info/', views.search_summoner, name='summoner_info'),
]
