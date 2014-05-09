from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'bookshare/index.html')

def signin(request):
    if request.method == 'GET' :
        return render(request, 'bookshare/signin.html')
    elif request.method == 'POST' :
        return render(request, 'bookshare/signin.html')
    else :
        return HttpResponseForbidden()

def signout(request):
    if request.method == 'GET' :
        return render(request, 'bookshare/signout.html')
    elif request.method == 'POST' :
        return render(request, 'bookshare/signout.html')
    else :
        return HttpResponseForbidden()

def signup(request):
    if request.method == 'GET' :
        return render(request, 'bookshare/signup.html')
    elif request.method == 'POST' :
        return render(request, 'bookshare/signup.html')
    else :
        return HttpResponseForbidden()
