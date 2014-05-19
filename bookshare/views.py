# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from apps.users.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms


class UserValidationForm(forms.Form):
    user_id = forms.CharField(max_length=15)
    password = forms.CharField(max_length=128, min_length=4)

def index(request):
    return render(request, 'bookshare/index.html')

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')
        
class SignInView(TemplateView):
    template_name = "bookshare/signin.html"
    error_msg = u"없는 아이디 이거나 비밀번호가 잘못되었습니다."
    default_next_url = "/"
    template_next_var = "next"

    def get(self, request, *args, **kwargs):
        context = dict(
            next = request.GET.get('next', self.default_next_url),
        )
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserValidationForm(request.POST)
        next_url = form.data.get("next", self.default_next_url)

        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            user = authenticate(user_id=user_id, password=password)
            if user is not None:
                if user.check_password(password):
                    login(request, user)
                    return HttpResponseRedirect(next_url)
        else:
            error_msg = u"형식에 맞지 않는 값을 입력하셨습니다."

        context = {'error_msg': self.error_msg}
        context[self.template_next_var] = next_url
        return render(request, self.template_name, context)


class SignUpValidationForm(forms.Form):
    user_id = forms.CharField(max_length=15)
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
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password']
            email = form.cleaned_data['email']            

            if password != password_confirm:
                error_msg = u"비밀번호가 서로 다릅니다."                
                return render(request, self.template_name, {'error_msg':self.error_msg})

            User.objects.create_user(user_id=user_id, email=email, password=password)
            user = authenticate(user_id=user_id, password=password)
            if user is not None:
                if user.check_password(password):
                    login(request, user)
                    return HttpResponseRedirect('/')
        else:
            error_msg = u"잘못 입력하신 값이 있습니다."                            
        return render(request, self.template_name, {'error_msg':self.error_msg})


class MyPageView(View):
    @method_decorator(login_required)
    def get(self, request):
        context = dict(
            user = request.user,
        )

        return render(request, 'bookshare/mypage.html', context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = SignUpValidationForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id'];
            password_before = form.cleaned_data['password-before'];
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password-confirm']
            email = form.cleaned_data['email']            

            if password != password_confirm:
                error_msg = u"비밀번호가 서로 다릅니다."                
                return render(request, self.template_name, {'error_msg':self.error_msg})

            user = authenticate(user_id=user_id, password=password_before)
            if user is not None:
                if user.check_password(password):
                    # modefy user data
                    # 
                    # 
                    # 
                    return HttpResponseRedirect('/')


class MyRentRequestListView(ListView):
    template_name = 'bookshare/my_rent_requests.html'
    
    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name)

    @method_decorator(login_required)
    def get_queryset(self):
        return self.request.user.rentrequest_set.pending()

class MyRentListView(ListView):
    template_name = 'bookshare/my_rents.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name)
    
    def get_queryset(self):
        return self.request.user.stock_set.rented()

class MyDonateListView(ListView):
    template_name = 'bookshare/my_donates.html'

    @method_decorator(login_required)
    def get(self, request):
        return render(request, self.template_name)

    def get_queryset(self):
        return self.request.user.stock_set.all()



def how_it_works(request):
    if request.method == 'GET' :
        return render(request, 'how_it_works.html')
    else :
        return HttpResponseForbidden()

