# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms

class UserValidationForm(forms.Form):
    user_id = forms.CharField(max_length=15)
    password = forms.CharField(max_length=128, min_length=4)

def index(request):
    return render(request, 'bookshare/index.html')

# def signin(request):
#     if request.method == 'GET' :
#         return render(request, 'bookshare/signin.html')
#     elif request.method == 'POST' :
#         return render(request, 'bookshare/signin.html')
#     else :
#         return HttpResponseForbidden()

def signout(request):
    if request.method == 'GET' :
        return render(request, 'bookshare/signout.html')
    elif request.method == 'POST' :
        return render(request, 'bookshare/signout.html')
    else :
        return HttpResponseForbidden()

class SignInView(TemplateView):
    template_name = "bookshare/signin.html"
    error_msg = u"아이디와 비밀번호를 입력하세요"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = UserValidationForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']

            user = authenticate(user_id=user_id, password=password)
            if user is not None:
                if user.check_password(password):
                    login(request, user)
                    return HttpResponseRedirect('/')
        return render(request, self.template_name, {'error_msg':self.error_msg})

    
def signup(request):
    if request.method == 'GET' :
        return render(request, 'bookshare/signup.html')
    elif request.method == 'POST' :
        return render(request, 'bookshare/signup.html')
    else :
        return HttpResponseForbidden()
