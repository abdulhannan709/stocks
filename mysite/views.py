from django.http import HttpResponse
from django.shortcuts import render, redirect
from tradify.forms import NewUserForm
from django.contrib.auth import login
from django.contrib.auth import login, authenticate 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms.widgets import PasswordInput, TextInput

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Email'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))


def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def home2(request):
    return render(request, 'home2.html')

def signup(request):
    if request.method == "POST":
	    form = NewUserForm(request.POST)
	    if form.is_valid():
		    user = form.save()
		    login(request, user)
		    messages.success(request, "Registration successful." )
		    return redirect("login")
	    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="signup.html", context={"register_form":form})

def login_page(request, user=None):
	if request.method == "POST":
		form = CustomAuthForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = CustomAuthForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def recover(request):
    return render(request, 'recover.html')

def contact(request):
    return render(request, 'contact.html')
