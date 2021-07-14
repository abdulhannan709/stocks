from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def recover(request):
    return render(request, 'recover.html')

def contact(request):
    return render(request, 'contact.html')
