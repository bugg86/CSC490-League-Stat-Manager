from django import forms
from .models import Summoner


class SummonerSearchForm(forms.Form):
    summoner_name = forms.CharField(label="Summoner Name", max_length=300)

    class Meta:
        model = Summoner
        fields = ['summoner_name']
