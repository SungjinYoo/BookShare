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
