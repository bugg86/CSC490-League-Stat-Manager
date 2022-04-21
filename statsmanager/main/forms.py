from django import forms
from .models import Summoner


class SummonerSearchForm(forms.Form):
    summoner_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': "Enter a Summoner's name here"}), max_length=300)

    class Meta:
        model = Summoner
        fields = ['summoner_name']
