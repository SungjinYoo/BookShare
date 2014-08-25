# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
from apps.users.models import User
from apps.books.models import Book
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import forms

from bookshare.apps.books.forms import CancelRentRequestForm, ReturnRequestForm



class UserValidationForm(forms.Form):
    user_id = forms.CharField(max_length=15)
    password = forms.CharField(max_length=128, min_length=4)


def index(request):
    context = {
        "recent_books": Book.objects.order_by("-id")[:4]
    }
    return render(request, 'bookshare/index.html', context)

def signout(request):
    logout(request)
    return HttpResponseRedirect("/")

class SignOutView(TemplateView) :
    def get(self, request):
        return signout(request);
    def post(self, request, *args, **kwargs):
        return signout(request);
        
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

        context = {'error_msg': self.error_msg }
        context[self.template_next_var] = next_url
        return render(request, self.template_name, context)


class SignUpValidationForm(forms.Form):
    user_id = forms.CharField(max_length=15, min_length=4)
    name = forms.CharField(max_length=15, min_length=1)
    password = forms.CharField(max_length=128, min_length=4)
    password_confirm = forms.CharField(max_length=128, min_length=4)
    email = forms.EmailField(max_length=255)

    def clean(self):
        cleaned_data = super(SignUpValidationForm, self).clean()
        user_id = cleaned_data.get("user_id")
        name = cleaned_data.get("name")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get('password_confirm')
        email = cleaned_data.get('email')
            
        if not password:
            self._errors["msg"] = '* 패스워드 길이가 잘못되었습니다.'
        elif not user_id : 
            self._errors["msg"] = '* 유저 아이디 길이가 잘못되었습니다.'
        elif not name : 
            self._errors["msg"] = '* 이름 길이는 1자이상 15자 이하가 되어야 합니다.'
        elif not password_confirm : 
            self._errors["msg"] = '* 확인 패스워드 길이가 잘못되었습니다.'
        elif not email : 
            self._errors["msg"] = '* 이메일 형식이 잘못되었습니다.'
    
        return cleaned_data


class SignUpView(TemplateView):
    template_name = "bookshare/signup.html"
    error_msg = u"알수없는 오류가 발생하였습니다."
    def get(self, request):
        return render(request, self.template_name)
    def post(self, request, *args, **kwargs):
        form = SignUpValidationForm(request.POST)
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
        return render(request, self.template_name, {'errors':form.errors })

class LoginRequiredViewMixin(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredViewMixin, self).dispatch(request, *args, **kwargs)

class MyPageView(LoginRequiredViewMixin, TemplateView):
    template_name = 'bookshare/mypage.html'
    def get(self, request):
        if request.user.is_anonymous() :
            return render(request, 'bookshare/signin.html')
        return render(request, 'bookshare/mypage.html')

    
    
class ModifyValidationForm(forms.Form):
    user_id = forms.CharField(max_length=15)
    password = forms.CharField(max_length=128, min_length=4)
    password_modify = forms.CharField(max_length=128, min_length=4);
    password_modify_confirm = forms.CharField(max_length=128, min_length=4);
    email = forms.EmailField(max_length=255)
    
    def clean(self):
        cleaned_data = super(ModifyValidationForm, self).clean()
        password = cleaned_data.get("password")
        password_modify = cleaned_data.get('password_modify')
        password_modify_confirm = cleaned_data.get('password_modify_confirm')
        email = cleaned_data.get('email')
            
        if not password:
            self._errors["msg"] = '* 패스워드 길이가 잘못되었습니다.'
        elif not password_modify : 
            self._errors["msg"] = '* 새로운 패스워드 길이가 잘못되었습니다.'
        elif not password_modify_confirm : 
            self._errors["msg"] = '* 확인 패스워드 길이가 잘못되었습니다.'
        elif not email : 
            self._errors["msg"] = '* 이메일 형식이 잘못되었습니다.'
    
        return cleaned_data
    
class MyPageViewModify(LoginRequiredViewMixin, TemplateView):
    template_name = 'bookshare/mypagemodify.html'
    error_msg = ""
    error_number = ""
    
    def get(self, request):
        if request.user.is_anonymous() :
            return render(request, 'bookshare/signin.html')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = ModifyValidationForm(request.POST)
        if form.is_valid():            
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']
            password_modify = form.cleaned_data['password_modify']
            password_modify_confirm = form.cleaned_data['password_modify_confirm']
            email = form.cleaned_data['email']
                            
            user = authenticate(user_id=user_id, password = password)
            
            if user is not None:
                if not user.check_password(password):
                    self.error_msg = u"* 비밀번호가 잘못되었습니다."
                    self.error_number = 0
                    return render(request, self.template_name, {'error_msg':self.error_msg, 'error_num' : self.error_number})
            else:
                self.error_msg = u"* 비밀번호가 잘못되었습니다."
                self.error_number = 0
                return render(request, self.template_name, {'error_msg':self.error_msg, 'error_num' : self.error_number})
                                
            if password_modify != password_modify_confirm:
                self.error_msg = u"* 비밀번호가 서로 다릅니다."
                self.error_number = 1
                return render(request, self.template_name, {'error_msg':self.error_msg, 'error_num' : self.error_number})


            user.set_password(password_modify)
            user.email = email
            user.save();
            return render(request, self.template_name)            
        return render(request, self.template_name, {'errors':form.errors })
 
class MyRentRequestListView(ListView, LoginRequiredViewMixin):
    template_name = 'bookshare/my_rent_requests.html'
    
    @method_decorator(login_required)
    def get(self, request):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        context['cancel_rent_request_form'] = CancelRentRequestForm()

        return render(request, self.template_name, context)
            
    def get_queryset(self):
        return self.request.user.rentrequest_set.pending()

class MyRentListView(ListView, LoginRequiredViewMixin):
    template_name = 'bookshare/my_rents.html'

    @method_decorator(login_required)
    def get(self, request):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)
        context['return_request_form'] = ReturnRequestForm()
        return render(request, self.template_name, context)
    
    def get_queryset(self):
        return self.request.user.renting_stocks.rented().order_by('-changed_at')

class MyDonateListView(ListView, LoginRequiredViewMixin):
    template_name = 'bookshare/my_donates.html'

    @method_decorator(login_required)
    def get(self, request):
        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)

        return render(request, self.template_name, context)

    def get_queryset(self):
        # if not book is available(reclaimed, destroyed etc...) conditions must be changed
        return self.request.user.stock_set.all().order_by('-added_at')


def how_it_works(request):
    if request.method == 'GET' :
        return render(request, 'how_it_works.html')
    else :
        return HttpResponseForbidden()

