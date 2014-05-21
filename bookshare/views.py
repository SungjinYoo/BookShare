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

from bookshare.apps.books.forms import CancelRentRequestForm, ReturnRequestForm

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

    def get_context_data(self, **kwargs):
        context = super(SignInView, self).get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', self.default_next_url)
        return context

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
    user_id = forms.CharField(max_length=15, min_length=4)
    name = forms.CharField(max_length=15, min_length=4)
    password = forms.CharField(max_length=128, min_length=4)
    password_confirm = forms.CharField(max_length=128, min_length=4)
    email = forms.EmailField(max_length=255)

class SignUpView(TemplateView):
    template_name = "bookshare/signup.html"
    error_msg = u"알수없는 오류가 발생하였습니다."

    def post(self, request, *args, **kwargs):
        form = SignUpValidationForm(request.POST)
        print form
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']
            email = form.cleaned_data['email']            

            if password != password_confirm:
                self.error_msg = u"비밀번호가 서로 다릅니다."                
                return render(request, self.template_name, {'error_msg':self.error_msg})

            User.objects.create_user(user_id=user_id, name = name, email=email, password=password)
            user = authenticate(user_id=user_id, password=password)
            if user is not None:
                if user.check_password(password):
                    login(request, user)
                    return HttpResponseRedirect('/')
        else:
            self.error_msg = u"잘못 입력하신 값이 있습니다."                            
        return render(request, self.template_name, {'error_msg':self.error_msg})

class LoginRequiredViewMixin(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredViewMixin, self).dispatch(request, *args, **kwargs)

class MyPageView(LoginRequiredViewMixin, TemplateView):
    template_name = 'bookshare/mypage.html'
    def get(self, request):
        if request.user.is_anonymous() :
            return render(request, 'bookshare/signin.html')
        data = dict(
                userid = request.user.user_id,
                name = request.user.name,
                sex = request.user.sex,
                email = request.user.email,
        )
        return render(request, 'bookshare/mypage.html', data)

    
    
class ModifyValidationForm(forms.Form):
    user_id = forms.CharField(max_length=15)
    password = forms.CharField(max_length=128, min_length=4)
    password_modify = forms.CharField(max_length=128, min_length=4);
    password_modify_confirm = forms.CharField(max_length=128, min_length=4);
    email = forms.EmailField(max_length=255)
    
class MyPageViewModify(LoginRequiredViewMixin, TemplateView):
    template_name = 'bookshare/mypagemodify.html'
    error_msg = ""
    
    def get(self, request):
        if request.user.is_anonymous() :
            return render(request, 'bookshare/signin.html')
        data = dict(
                userid = request.user.user_id,
                name = request.user.name,
                sex = request.user.sex,
                email = request.user.email,
        )
        return render(request, self.template_name, data)

    def post(self, request, *args, **kwargs):
        form = ModifyValidationForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            password_modify = form.cleaned_data['password_modify']
            password_modify_confirm = form.cleaned_data['password_modify_confirm']
            email = form.cleaned_data['email']
                            
            user = authenticate(user_id=user_id, password=password)
            print "0"
            
            if user is not None:
                if not user.check_password(password):
                    self.error_msg = u"* 비밀번호가 잘못되었습니다."
            else:
                self.error_msg = u"* 비밀번호가 잘못되었습니다."
                                
            if password_modify != password_modify_confirm:
                self.error_msg = u"* 비밀번호가 서로 다릅니다."

            if self.error_msg:
                return render(request, self.template_name, {'error_msg':self.error_msg})

            user.password = password_modify
            user.email = email
            user.save();
            data = dict(
                    userid = request.user.user_id,
                    name = request.user.name,
                    sex = request.user.sex,
                    email = request.user.email,
            )
            return render(request, self.template_name, data)
        
        else : 
            self.error_msg = u"* 입력정보가 잘못 되었습니다."
        return render(request, self.template_name, {'error_msg':self.error_msg})

class MyRentRequestListView(ListView, LoginRequiredViewMixin):
    template_name = 'bookshare/my_rent_requests.html'
    
    @method_decorator(login_required)
    def get(self, request):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        context['cancel_rent_request_form'] = CancelRentRequestForm()

        return render(request, self.template_name, context)
            
    def get_queryset(self):
        return self.request.user.rentrequest_set.all()

class MyRentListView(ListView, LoginRequiredViewMixin):
    template_name = 'bookshare/my_rents.html'

    @method_decorator(login_required)
    def get(self, request):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        context['return_request_form'] = ReturnRequestForm()
        return render(request, self.template_name, context)
    
    def get_queryset(self):
        return self.request.user.stock_set.rented()

class MyDonateListView(ListView, LoginRequiredViewMixin):
    template_name = 'bookshare/my_donates.html'

    @method_decorator(login_required)
    def get(self, request):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)

        return render(request, self.template_name, context)

    def get_queryset(self):
        return self.request.user.stock_set.all()


def how_it_works(request):
    if request.method == 'GET' :
        return render(request, 'how_it_works.html')
    else :
        return HttpResponseForbidden()

