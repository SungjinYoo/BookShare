from django.contrib.auth import get_user_model
from django import forms

import models

from bookshare.apps import books

class RentRequestForm(forms.Form):
    actor = forms.ModelChoiceField(queryset=get_user_model().objects.all())
    stock = forms.ModelChoiceField(queryset=models.Stock.objects.available())

class StockDeliverForm(forms.Form):
    actor = forms.ModelChoiceField(queryset=get_user_model().objects.all())
    book = forms.ModelChoiceField(queryset=books.models.Book.objects.all())
    condition = forms.ChoiceField(choices=models.Stock.CONDITIONS)

class RentRequestProcessForm(forms.Form):
    request = forms.ModelChoiceField(queryset=models.RentRequest.objects.pending())
