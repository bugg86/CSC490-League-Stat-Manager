from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .models import CustomUser

class RegistrationForm(UserCreationForm):
    # username = forms.CharField()
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']