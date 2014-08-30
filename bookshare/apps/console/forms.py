#encoding=utf8

from django.contrib.auth import get_user_model
from django import forms

from bookshare.apps.core import models
from bookshare.apps.users import models as users_models
from bookshare.apps import books

class StockDeliverForm(forms.Form):
    actor = forms.ModelChoiceField(queryset=get_user_model().objects.all())
    book = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                  queryset=books.models.Book.objects.all())
    condition = forms.ChoiceField(choices=models.Stock.CONDITIONS)

class RentRequestProcessForm(forms.Form):
    request = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                     queryset=models.RentRequest.objects.all())

class ReturnProcessForm(forms.Form):
    user = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                  queryset=users_models.User.objects.all())
    stock = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                   queryset=models.Stock.objects.all())
    condition = forms.ChoiceField(choices=models.Stock.CONDITIONS)


class BookAddForm(forms.Form):
    isbn = forms.CharField(label="ISBN")
    title = forms.CharField(label="제목")
    cover_url = forms.URLField(label="표지 이미지 URL")

class BookRentForm(forms.Form):
    book = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                  queryset=books.models.Book.objects.all())
    user = forms.ModelChoiceField(label="대여자",
                                  queryset=users_models.User.objects.all())

class SignUpValidationForm(forms.Form):
    user_id = forms.CharField(label="학번", max_length=15, min_length=4)
    name = forms.CharField(label="이름", max_length=15, min_length=1)
    email = forms.EmailField(label="이메일", max_length=255)
    phone_number = forms.CharField(label="연락처", max_length=20)

    def clean(self):
        cleaned_data = super(SignUpValidationForm, self).clean()
        user_id = cleaned_data.get("user_id")
        name = cleaned_data.get("name")
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

class BulkAddForm(forms.Form):
    file = forms.FileField()
