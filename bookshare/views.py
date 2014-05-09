# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms


class UserValidationForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(max_length=128, min_length=4)

def index(request):
    return render(request, 'bookshare/index.html')

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')
        
class SignInView(TemplateView):
    template_name = "bookshare/signin.html"
    error_msg = u"없는 아이디 이거나 비밀번호가 잘못되었습니다."

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = UserValidationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.check_password(password):
                    login(request, user)
                    return HttpResponseRedirect('/')
        return render(request, self.template_name, {'error_msg':self.error_msg})


class SignUpValidationForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(max_length=128, min_length=4)
    email = forms.EmailField(max_length=255)

class SignUpView(TemplateView):
    template_name = "bookshare/signup.html"
    error_msg = u"알수없는 오류가 발생하였습니다."
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = SignUpValidationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password']
            email = form.cleaned_data['email']            

            if password != password_confirm:
                error_msg = u"비밀번호가 서로 다릅니다."                
                return render(request, self.template_name, {'error_msg':self.error_msg})

            User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.check_password(password):
                    login(request, user)
                    return HttpResponseRedirect('/')
        else:
            error_msg = u"잘못 입력하신 값이 있습니다."                            
        return render(request, self.template_name, {'error_msg':self.error_msg})


class MyPageView(View):
    # need login required
    def get(self, request):
        data = dict(
            user = request.user,
        )

        return render(request, 'bookshare/mypage.html', data)

    def post(self, request):
        return HttpResponseForbidden()


def how_it_works(request):
    if request.method == 'GET' :
        return render(request, 'how_it_works.html')
    else :
        return HttpResponseForbidden()
