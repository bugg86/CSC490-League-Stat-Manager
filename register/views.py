from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from register.forms import RegistrationForm
# import forms


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        return redirect("/")
        
    return render(request, 'register/register.html', {"form": form})