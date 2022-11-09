from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'auth_ok/index.html')

def ask(request):
    return render(request, 'auth_ok/ask.html')

def settings(request):
    return render(request, 'auth_ok/settings.html')

# def question(request, id: int):
#     return render(request, 'auth_ok/question.html')
def question(request):
    return render(request, 'auth_ok/question.html')

def tag(request):
    return render(request, 'auth_ok/tag.html')

def login(request):
    return render(request, 'not_auth/login.html')

def signup(request):
    return render(request, 'not_auth/signup.html')